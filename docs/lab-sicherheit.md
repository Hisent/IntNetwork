# Sicherheit des Ansible-Labs

Diese Datei beschreibt, was beim Ausführen von Teilnehmer-Playbooks passiert,
welche Grenzen gezogen sind und welche ausdrücklich **nicht**. Sie ist die
Grundlage für die Entscheidung, ob das Lab auf einem Server eingeschaltet wird.

## Was hier eigentlich passiert

Ein Playbook ist ausführbarer Code. Module wie `command`, `shell` und `script`
gehören zum normalen Ansible-Umfang und lassen sich nicht sinnvoll wegfiltern —
eine Sperrliste wäre eine Einladung, sie zu umgehen. Wer ein Playbook schreiben
darf, führt im Runner-Container Code aus. Das ist der Zweck des Labs.

Deshalb ist **der Container die Sicherheitsgrenze**, nicht eine Filterliste.

## Auftragsarten

Der Runner führt nicht mehr nur Ansible aus. Jede Art wird einzeln freigegeben
(`RUNNER_KINDS` beim Runner, `LAB_KINDS` beim Backend, Standard jeweils nur
`ansible`):

- **`ansible`** — Playbook der Teilnehmerin. Das ist der Fall von oben:
  beliebiger Code im Container, der Container ist die Grenze.
- **`openssl`** — bis zu sechs `openssl`-Aufrufe auf mitgeschickten Dateien.
  Kein Netz, keine Shell: Der Runner zerlegt die Zeile mit `shlex.split`, setzt
  das Programm selbst davor und ruft es ohne `shell=True` auf. Keine Pipes,
  keine Umleitungen, keine Verkettung.
- **`git`** — dasselbe mit `git`.

**`git`/`openssl` sind zusätzlich auf eine Allowlist von Unterkommandos
beschränkt (`runner/worker.py`, `_werkzeug_argv_pruefen`).** Das ist neu und
korrigiert eine frühere, zu optimistische Aussage an dieser Stelle: „Kein
Netz, keine Shell" allein reicht NICHT, weil manche Werkzeuge selbst
netz- oder codeausführende Fähigkeiten mitbringen, ganz ohne Shell und ganz
ohne offenes Netzwerk im Container. Konkret ließ sich vor dieser Sperre über
den git-eigenen `ext`-Transport beliebiger Shell-Code ausführen — TROTZ
`network_mode: none`:

```
-c protocol.ext.allow=always clone ext::sh -c 'beliebiger_befehl' /tmp/x
```

Die Sperre hat zwei Schichten:

1. **Allowlist statt Blockliste.** Das erste Nicht-Options-Token einer
   Kommandozeile muss eines von wenigen, bewusst lokalen Unterkommandos sein
   (z. B. `init`, `status`, `add`, `commit`, `checkout`, `merge`, `worktree`,
   `mv` für git; `genrsa`, `req`, `x509`, `verify`, … für openssl). Netz- oder
   codeausführende Unterkommandos (`clone`, `fetch`, `push`, `pull`,
   `remote`, `submodule` bei git; `s_client`/`s_server` bei openssl) stehen
   **nicht** auf der Liste und werden mit `rc=2` und einer Meldung
   zurückgewiesen, bevor überhaupt ein Prozess startet. `git config` steht
   ebenfalls nicht auf der Liste: `git config alias.status '!sh -c ...'`
   könnte sonst einen scheinbar harmlosen späteren Aufruf wie `status` in
   Shell-Code umlenken.
2. **Bestimmte Flags/Muster sind unabhängig von der Position immer
   verboten**, weil sie einen Transport oder Codepfad außerhalb des
   Unterkommandos öffnen: für git `-c` (Konfigurationsinjektion, siehe
   Beispiel oben), `--exec`, `--upload-pack`, `--receive-pack`, `-u`,
   `--git-dir`, `--work-tree`, sowie jedes Argument, das `ext::`, `fd::` oder
   `file://` enthält; für openssl `-engine`, `-provider`, `-provider-path`, `-config`, `-exec`
   (jeweils Wege, eine beliebige Bibliothek nachzuladen oder ein
   Skript/Programm zu übernehmen).

Zusätzlich setzt der Runner für `git` `GIT_ALLOW_PROTOCOL=file` in der
Prozessumgebung — eine zweite, unabhängige Verteidigungsebene, die
Netztransporte (`ext`, `ssh`, `http`, `git`, …) auf Umgebungsebene sperrt,
falls die Allowlist-Prüfung einmal durch einen heute unbekannten Weg umgangen
werden sollte. Sie ersetzt die Allowlist nicht, sie ergänzt sie.

**Dritte Schicht: die WERTE pfadwertiger Argumente sind auf das
Arbeitsverzeichnis beschränkt.** Das ist eine Präzisierung einer früher zu
optimistischen Aussage an dieser Stelle: Subcommand-Allowlist und
verbotene-Flags-Liste prüfen nur, OB ein Unterkommando bzw. Flag vorkommen
darf — nicht, WOHIN ein dabei mitgegebener Pfad zeigt. Ohne diese dritte
Schicht ließ sich trotz beider oberen Schichten beliebiger Dateiinhalt aus
dem Container lesen (`openssl enc -base64 -in /etc/passwd` — `enc` ist
erlaubt, `-in` war ungeprüft) oder beliebig schreiben, auch in das mit dem
Backend GETEILTE, nicht-`read_only` `/queue`-Volume (`git diff
--output=/queue/x`, `openssl req -out /queue/x`) — ein Disk-DoS- bzw.
Warteschlangen-Manipulationsweg.

`runner/worker.py` prüft dafür bei jedem der folgenden Flags den WERT gegen
dieselbe Regel wie für mitgeschickte Dateien (reiner Dateiname, kein `/`,
kein `\`, kein `..`, nicht absolut):

- **git:** `--output`/`-o` sowie — als Sonderfall, weil dort ein Pfad als
  Positionsargument statt als Flag-Wert steht — das erste
  Nicht-Options-Argument nach `worktree add`.
- **openssl:** fail-closed über **alle** Tokens, nicht mehr über eine Liste
  bekannter Pfad-Flags (die war lückenhaft: `-CAserial`, `-writerand`,
  `-untrusted`, `-CApath`, `-kfile`, `-outdir`, Positionsargumente von
  `dgst`/`verify` u. a.). Kein Token darf `/`, `\`, `..` oder Steuerzeichen
  enthalten. Einzige Ausnahme sind die Werte von `-subj` (jedes `/`-Segment
  muss `typ=wert` sein) und `-addext` (muss mit `name=` beginnen, kein `..`).
  `-passin`/`-passout`/`-pass` nehmen nur ein inline `pass:...` an. Optionen
  werden vor dem Vergleich normalisiert, weil openssl auch `--flag` und
  `-flag=wert` akzeptiert (`--config=x.cnf` umging sonst Schicht 2).

- **git:** ebenfalls fail-closed über **alle** Tokens. Jedes Positionsargument
  und jeder `--opt=wert`-Wert muss im Arbeitsverzeichnis bleiben (nicht absolut,
  kein ausbrechendes `..`, kein `\`, keine Steuerzeichen). Anders als bei
  openssl bleiben relative Unterpfade mit `/` erlaubt, weil Zweignamen
  (`feature/x`) und `add src/app.py` sie brauchen. Zusätzlich sind die Optionen
  `-c`/`--config-env` (Konfigurationsinjektion → `core.hooksPath`,
  `core.sshCommand`, `alias.*`, `diff.external`, …), `--exec-path` und `-C`
  (Verzeichniswechsel/Ausbruch) in Schicht 2 verboten. Grenze: lexikalisch,
  also keine Symlink-Ausbrüche erkannt — git kann im Arbeitsverzeichnis
  Symlinks anlegen.

**Das bleibt ausdrücklich eine Allowlist, keine Blockliste, mit allen
Konsequenzen:** Ein neues Unterkommando (auch ein scheinbar harmloses)
funktioniert erst, wenn es bewusst in `runner/worker.py` freigeschaltet wird.
Wer eine neue Lab-Vorlage schreibt, die ein weiteres, lokales Unterkommando
braucht, muss diese Liste erweitern — sonst scheitert die Vorlage mit einer
regulären `rc=2`-Meldung, keinem Absturz.

**Wichtig für die Bewertung:** Die Arten sind nicht gleich mächtig. `ansible`
erlaubt beliebige Codeausführung, `openssl` und `git` erlauben nur Datei-Ein-
und -Ausgabe über eine kleine, geschlossene Liste lokaler Unterkommandos. Ein
Durchlauf, der nur den PKI-Lehrgang fährt, kann deshalb `openssl` freigeben
und `ansible` weglassen — dann ist der Container **kein** Sandkasten für
fremden Code mehr. Das ist strikt weniger Angriffsfläche als der bisherige
Zustand, nicht mehr.

Umgekehrt gilt: Ist `ansible` freigegeben, ändern zusätzliche Werkzeuge im
Image nichts an der Bewertung — wer ein Playbook schreiben darf, kann sie
ohnehin alle aufrufen.

## Wie der Zuschnitt aussieht

- **Das Backend führt nichts aus.** Es kennt `SECRET_KEY` und die Datenbank und
  wäre das falsche Ziel für fremden Code. Es nimmt das Playbook entgegen, legt
  es als Auftrag ab und wartet auf das Ergebnis.
- **Der Runner hat kein Netzwerk.** Der Container läuft mit
  `network_mode: "none"`: keine Adresse, keine Namensauflösung, kein Socket.
  Ein Playbook kann per Netz nichts erreichen, weil kein Netz existiert.
- **Austausch über ein gemeinsames Volume.** Backend schreibt
  `/queue/in/<id>.json`, der Runner antwortet mit `/queue/out/<id>.json`. Beide
  Seiten schreiben zuerst eine temporäre Datei und benennen sie atomar um, damit
  nie eine halbe Datei gelesen wird.

### Warum nicht einfach ein internes Docker-Netz?

Der erste Entwurf war genau das: ein HTTP-Dienst in einem Netz mit
`internal: true`. Auf dem Zielsystem (Coolify) hat sich am 21.07.2026 gezeigt,
dass das **nicht reicht**. Coolify hängt jeden Dienst zusätzlich in das
Projekt-Netz, und dieses ist nicht intern. Gemessen aus dem Runner-Container:

- `1.1.1.1:443` erreichbar, DNS-Auflösung funktionierte,
- Datenbank und Backend lagen im selben Netz.

Die Zusage „kein Weg nach draußen, kein Zugriff auf Daten" war damit falsch.
`network_mode: "none"` ist die strukturelle Antwort: Sie hängt nicht an einer
Firewall-Regel, die jemand später entfernt, und nicht daran, wie eine
Plattform ihre Netze zusammensteckt.

## Welche Maßnahmen greifen

- Kein Netzwerk (siehe oben), kein Port, keine Erreichbarkeit von außen.
- Unprivilegierter Benutzer (`uid 10001`), `cap_drop: ALL`,
  `no-new-privileges`, `read_only` für das Wurzeldateisystem.
- Einziger Schreibort ist ein `tmpfs` mit `noexec` (64 MB) — ein Playbook kann
  dort keine eigene Binärdatei ablegen und ausführen. Dass Ansible auf einem
  `noexec`-Dateisystem trotzdem läuft, wurde geprüft (Module laufen über den
  Python-Interpreter, nicht als eigenständige Programme).
- Zeitgrenze je Lauf (`RUNNER_TIMEOUT`, Standard 30 s), Obergrenze für die
  Ergebnis-Ausgabe und begrenzte Parallelität (`RUNNER_MAX_PARALLEL`, Standard
  2). Die Kindprozess-Ausgabe wird zuerst in einer temporären Datei im ohnehin
  auf 64 MB begrenzten `tmpfs` gesammelt; der Worker liest daraus nur die
  Antwortgrenze. Unbegrenzte Ausgabe kann daher nicht dessen RAM füllen.
- CPU-, Speicher- und Prozessgrenzen am Container.
- Jeder Lauf in einem frischen Verzeichnis, das danach gelöscht wird.
- **Arbeitsverzeichnis je Teilnehmer**: Der Runner erhält vom Backend eine
  undurchsichtige Kennung (HMAC über die Teilnehmer-ID mit dem `SECRET_KEY`) und
  legt darunter ein Verzeichnis an, das zwischen Läufen bestehen bleibt. Es wird
  als `lab_dir` an das Playbook gegeben. Ohne diese Trennung würde der zweite
  Mensch den Zustand des ersten erben — dessen erster Lauf meldete dann schon
  „nichts geändert" und die Idempotenz-Übung wäre wertlos. Verzeichnisse älter
  als 12 Stunden werden aufgeräumt.
- Im Backend: Anmeldepflicht (Teilnehmer-Token) und Rate-Limit (20 Läufe pro
  Minute), Größengrenzen für Playbook, Inventar und Zusatzvariablen.

## Was NICHT abgedeckt ist

- **Ausbruch aus dem Container.** Eine Lücke im Kernel oder in der
  Container-Laufzeit hebelt die Isolierung aus. Wer das im Bedrohungsmodell
  braucht, muss auf VM-Isolierung (eigene Maschine, Firecracker, gVisor)
  wechseln.
- **Rechenzeit.** Angemeldete Teilnehmende können den Runner beschäftigen.
  Zeitgrenze, Parallelitätsgrenze und CPU-Limit bremsen das, verhindern es aber
  nicht vollständig.
- **Böswillig abgekoppelte Prozesse.** Die Zeitgrenze beendet die normale
  Prozessgruppe. Ein Programm kann diese Gruppe mit `setsid()` bewusst
  verlassen; gegen so einen Prozess helfen keine POSIX-Prozessgruppen. Er kann
  den Worker nicht mehr über eine offene Ausgabe-Pipe blockieren, wird aber bis
  zum Container-Limit weiterlaufen. Eine harte Grenze auch dafür braucht einen
  separaten Job-Container oder eine VM/cgroup je Lauf.
- **Alles, was im Runner-Container liegt.** Ein Playbook kann das Image und die
  Arbeitsverzeichnisse anderer Teilnehmender im selben Container lesen. Dort
  liegen keine Geheimnisse und keine Nutzerdaten — aber es ist keine Trennung
  wie zwischen zwei Maschinen.
- **Die gemeinsame Warteschlange.** Dasselbe gilt für `/queue`: Der Runner
  braucht dort Schreibrechte, und ein Playbook läuft mit genau diesen Rechten.
  Ein böswilliger Teilnehmer kann also fremde Aufträge und Ergebnisse lesen,
  verändern oder löschen — und damit fremde Läufe stören oder deren Ausgabe
  fälschen. Nach außen (Backend, Datenbank, Netz) führt von dort weiterhin kein
  Weg; das Volume ist nur zwischen diesen beiden Diensten geteilt. Wer das im
  Bedrohungsmodell nicht tragen will, gibt `ansible` nicht frei: Die Arten
  `openssl` und `git` sind auf eine Allowlist lokaler, nicht netzfähiger
  Unterkommandos beschränkt (siehe „Auftragsarten" oben) — das ist enger als
  „kein frei geschriebener Code", aber keine absolute Garantie: Es bleibt eine
  Allowlist, die von Hand gepflegt wird, kein Beweis, dass jedes zugelassene
  Unterkommando in jeder Argumentkombination harmlos ist.
  Seit v1.43 gibt es dagegen eine **Zwischenstufe, das Ergebnis-Token** (siehe
  eigener Abschnitt unten). Es erschwert das Fälschen, schließt die Lücke aber
  nicht.
- **Missbrauch durch Berechtigte.** Wer sich anmelden darf, darf Code
  ausführen. Der Teilnehmerkreis ist die eigentliche Zugangskontrolle.

## Ergebnis-Token (Zwischenstufe gegen gefälschte Ergebnisse)

Das Backend legt in jeden Auftrag ein Zufalls-Token (`secrets.token_urlsafe(32)`,
`backend/app/routers/lab.py`). Der Runner liest den Auftrag **beim Beanspruchen**
und löscht die Datei sofort (`_auftrag_lesen` in `runner/worker.py`, aufgerufen
aus `_runde`); danach existiert das Token nur noch im Speicher des Workers. Er
legt es dem Ergebnis bei. Das Backend nimmt `out/<id>.json` nur an, wenn das
Token stimmt und alle Felder vorhanden sind — sonst `502` mit klarer Meldung
statt eines ungeprüft durchgereichten Inhalts.

**Was das verhindert:** das „blinde" Fälschen. Ein Playbook, das einfach
`out/<fremde-id>.json` schreibt, wird verworfen; ebenso kaputte oder
unvollständige Ergebnisdateien (vorher `500`).

**Was es NICHT verhindert** — solange Playbook und Worker dieselbe uid haben:

1. **Lesen des Auftrags vor dem Beanspruchen.** `in/<id>.json` liegt lesbar im
   Volume, bis der Worker sie beansprucht: im Normalfall höchstens
   `RUNNER_POLL_SECONDS` (0,2 s), bei voller Warteschlange
   (`RUNNER_MAX_QUEUE_DEPTH`) beliebig lange. Ein Playbook, das `in/` in einer
   Schleife abfragt, liest das Token und kann damit ein gültiges Ergebnis
   schreiben oder den Auftrag gegen einen eigenen austauschen. Die Warteschlange
   kann der Angreifer mit eigenen langen Läufen selbst füllen.
2. **Lesen des Worker-Speichers.** Gleiche uid, gleiche (leere)
   Capability-Menge: `/proc/<pid>/mem` und `ptrace` des Workers sind erlaubt,
   sofern der Host es nicht per Yama unterbindet (`kernel.yama.ptrace_scope`
   ≥ 1 — Ubuntu-Standard 1, Debian-Standard 0; das Playbook ist ein Kind des
   Workers, kein Vorfahre, und fällt bei 1 unter die Sperre). Auf das
   Host-Setting darf sich das Bedrohungsmodell nicht verlassen.
3. **Stören.** Aufträge und Ergebnisse löschen, den Worker per Signal beenden
   (gleiche uid) — das Token ändert daran nichts.

Die Aussage aus „Was NICHT abgedeckt ist" gilt also weiter: Wer `ansible`
freigibt, vertraut dem Teilnehmerkreis. Die Arten `openssl` und `git` kommen an
`/queue` nicht heran (Pfadprüfung im Runner).

**Rollout:** Backend und Runner gemeinsam ausrollen. Ein neuer Runner mit altem
Backend funktioniert (kein Token im Auftrag → keines im Ergebnis); ein **neues
Backend mit altem Runner verwirft jedes Ergebnis mit 502**.

### Echte Trennung: Läufe unter einer zweiten uid (Umsetzungsplan, NICHT umgesetzt)

Nicht umgesetzt, weil es sich ohne Docker/Linux nicht belastbar testen lässt:
`setuid()` braucht Root bzw. Capabilities, und genau deren Zusammenspiel mit
`cap_drop`, `no-new-privileges`, Volume-Rechten und `tmpfs` ist der riskante
Teil. Ein Fehler hier macht das Lab unbenutzbar oder — schlimmer — gibt
Playbooks Root im Container.

Ziel: Worker = uid 0 mit minimalen Capabilities, Läufe = uid 10002 ohne
Capabilities. Dann kann ein Lauf weder `/queue` noch den Worker-Prozess
anfassen; Punkte 1–3 oben entfallen.

1. `runner/Dockerfile` (Z. 28–39): zweiten Benutzer `labjob` (uid/gid 10002)
   anlegen; `USER labrunner` entfernen (Worker startet als root); `/queue/in`
   und `/queue/out` als `root:10001`, Modus `0770` (10001 = uid/gid des
   Backend-Containers, `backend/Dockerfile` Z. 16) — das Backend schreibt über
   die Gruppe, `labjob` kommt nicht hinein. Kein `0777` mehr.
2. `docker-compose.yml`, Dienst `runner` (Z. 120–128): `cap_drop: ALL`
   behalten, dazu `cap_add: [SETUID, SETGID, KILL, CHOWN, DAC_OVERRIDE]`.
   `KILL`: root ohne `CAP_KILL` darf Prozesse einer fremden uid nicht beenden —
   ohne das greift die Zeitgrenze (`os.killpg`, `worker.py` Z. 170) nicht mehr.
   `CHOWN`/`DAC_OVERRIDE`: Arbeitsverzeichnisse an `labjob` übergeben und
   wieder aufräumen. `no-new-privileges` und `read_only` bleiben; `tmpfs`
   bleibt `mode=1777,noexec`.
3. `runner/worker.py`:
   - `_mit_zeitgrenze_ausfuehren` (Z. 162): `subprocess.Popen(..., user=JOB_UID,
     group=JOB_GID, extra_groups=[])` (neue Konstanten aus `RUNNER_JOB_UID`,
     Standard: keine Trennung, damit Tests und lokale Läufe unverändert bleiben).
     Der Wechsel von uid 0 auf 10002 leert die Capability-Mengen des Kindes.
   - `_workspace` (Z. 94–119), `_run_ansible` (Z. 198, `mkdtemp`) und
     `_run_werkzeug`: jedes Verzeichnis, in das der Lauf schreibt
     (`lab_dir`, `HOME`, `ANSIBLE_LOCAL_TEMP`), nach dem Anlegen per
     `os.chown(..., JOB_UID, JOB_GID)` übergeben, Modus `0700`.
   - `_antwort_schreiben` (Z. 725) und `_warteschlange_vorbereiten` (Z. 810):
     `chmod 0o666`/`0o777` durch `0o640`/`0o770` ersetzen und `os.chown(...,
     0, BACKEND_GID)`.
   - Startprüfung in `main()`: läuft der Worker als uid 0 **ohne** gesetzte
     `RUNNER_JOB_UID`, nicht starten (sonst liefen Playbooks als root).
4. Bestehendes Volume: `lab_queue` einmal entfernen (Rechte werden nur in ein
   leeres Volume übernommen, siehe Betriebshinweise).
5. Testschritte (Linux mit Docker, vor dem Merge):
   - `docker compose up runner`; Playbook mit `command: id` → uid=10002, und
     `grep Cap /proc/self/status` → `CapEff: 0000000000000000`.
   - Playbook `command: ls /queue/in` → „Permission denied"; `cat
     /proc/1/environ` und `kill -9 1` → abgelehnt.
   - Playbook `command: sleep 300` → nach `RUNNER_TIMEOUT` beendet
     (`docker top` zeigt keinen `sleep` mehr).
   - Regulärer Lauf zweimal (Idempotenz-Übung), je einmal `openssl` und `git`.
   - Backend-Seite: Auftrag wird angenommen, Ergebnis gelesen und gelöscht
     (kein `PermissionError` im Backend-Log).
   - `docker inspect` → `NetworkMode: none` unverändert.

Das Ergebnis-Token bleibt danach als zweite Schicht sinnvoll.

## Wann man das Lab besser aus lässt

- Wenn der Teilnehmerkreis nicht vertrauenswürdig ist (offene Anmeldung,
  externe Gäste ohne Aufsicht).
- Wenn der Host andere, sensible Dienste trägt und eine Container-Lücke
  entsprechend teuer wäre.
- Wenn niemand die Auslastung im Blick hat.

Das Lab ist **standardmäßig aus**. Ohne Konfiguration bleibt der Kurs
vollständig benutzbar; die Aufgaben lassen sich als Denkaufgaben lösen.

## Ein- und ausschalten

**Einschalten:** In der Umgebung des Backends setzen:

```
LAB_QUEUE_DIR=/queue
```

Dazu die gewünschten Arten, an **beiden** Stellen — sie werden nicht abgeglichen,
weil zwischen Backend und Runner kein Netzweg existiert:

```
LAB_KINDS=ansible,openssl        # Backend: was die Oberflaeche anbietet
RUNNER_KINDS=ansible,openssl     # Runner:  was tatsaechlich ausgefuehrt wird
```

Steht eine Art nur beim Backend, bietet das Widget sie an und der Lauf scheitert
mit einer Meldung des Runners. Steht sie nur beim Runner, bleibt sie ungenutzt.

Das Volume `lab_queue` ist in `docker-compose.yml` bereits bei Backend und
Runner eingehängt. Ein konfiguriertes Zugangs-Token gibt es bewusst nicht mehr:
Ohne Netzwerk ist das Volume die Grenze, ein geteiltes Geheimnis würde daran
nichts verbessern. (Das Ergebnis-Token weiter oben ist etwas anderes: Es wird je
Auftrag erzeugt und braucht keine Konfiguration.)

**Ausschalten:** `LAB_QUEUE_DIR` leeren und neu ausrollen. Die API antwortet
dann mit `503`, das Widget zeigt einen Hinweis, der Kurs läuft weiter.

**Erkennen, ob es aus ist:** Als angemeldeter Teilnehmer `GET /api/lab/status`
aufrufen — die Antwort ist `{"enabled": false}`.

## Betriebshinweise

- **Basis-Image und OpenSSL:** Der Runner baut auf `python:3.12-slim-trixie`
  (Debian 13, in `runner/Dockerfile` ausdrücklich benannt). Das Paket `openssl`
  ist dort **OpenSSL 3.5** (LTS-Zweig; geprüft am 12.10.2026:
  `3.5.7-1~deb13u3`). **Mindestversion: OpenSSL 3.5** — die Vorlage
  „Post-Quanten-Schlüssel“ des OpenSSL-Labs erzeugt ML-KEM-768- und
  ML-DSA-65-Schlüssel (`genpkey -algorithm ML-KEM-768` / `ML-DSA-65`), die es
  erst ab 3.5 gibt; ältere Versionen brechen dort mit „Algorithm … not found“
  ab. Alle übrigen Befehle des PKI-Lehrgangs laufen ab 3.0. Nach einem Wechsel
  des Debian-Release im Container nachprüfen:
  `docker exec <runner-container> openssl version`.

- **Logs:** Der Runner schreibt nach stderr (`docker logs <runner-container>`),
  darunter Startmeldung, unlesbare Aufträge und interne Fehler. Playbook-Inhalte
  landen bewusst nicht im Log.
- **Prüfen, ob der Runner arbeitet:** Es gibt keinen Health-Endpunkt mehr, weil
  es keinen Netzwerkdienst gibt. Stattdessen:

  ```
  docker logs --tail 5 <runner-container>
  ```

  Erwartet wird beim Start eine Zeile `Lab-Runner bereit. Warteschlange: /queue,
  … Netzwerk: keines`. Ob die Kette insgesamt steht, prüft man am ehrlichsten im
  Kurs selbst: ein Playbook zweimal ausführen.
- **Isolierung nachprüfen** (nach jedem größeren Plattform-Update sinnvoll):

  ```
  docker inspect <runner-container> --format '{{.HostConfig.NetworkMode}}'
  ```

  Erwartet: `none`. Steht dort etwas anderes, hat die Plattform die Vorgabe
  überschrieben — dann das Lab abschalten, bis das geklärt ist.
- **`PermissionError: '/queue/in'` im Runner-Log:** Das Volume gehört `root`,
  der Runner läuft unprivilegiert (uid 10001). Das Image legt `/queue/in` und
  `/queue/out` bereits mit passender Eigentümerschaft an; Docker übernimmt sie
  aber nur, wenn das Volume beim ersten Start **leer** ist. Wurde das Volume
  vorher schon von einer älteren Fassung angelegt, einmal entfernen und neu
  ausrollen — es enthält nur Aufträge in Bearbeitung, nichts Bewahrenswertes:

  ```
  docker volume ls | grep lab_queue
  docker volume rm <projekt>_lab_queue
  ```

  Der Runner stirbt in diesem Fall übrigens nicht, sondern meldet die Ursache
  und versucht es alle fünf Sekunden erneut; nach dem Beheben läuft er ohne
  Eingriff weiter.
- **Dauerlast:** `RUNNER_MAX_PARALLEL` senken oder das Lab abschalten. Läufe,
  die regelmäßig in die Zeitgrenze laufen, deuten eher auf zu ambitionierte
  Übungs-Playbooks hin als auf Missbrauch.
- **Speicher:** Das `tmpfs` ist auf 64 MB begrenzt und nach einem Neustart des
  Containers leer. Arbeitsverzeichnisse sind Übungsstände, kein Speicher.
