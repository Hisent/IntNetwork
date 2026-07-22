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
   `file://` enthält; für openssl `-engine`, `-provider`, `-config`, `-exec`
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
- **openssl:** `-in`, `-out`, `-keyout`, `-CAfile`, `-CAkey`, `-extfile`,
  `-signkey`, `-cert`, `-key`, `-CA`. Für `-passin`/`-passout` gilt eine
  eigene Regel: Der Wert ist eine Passwort-*Quelle*, kein Dateiname direkt —
  erlaubt ist nur ein inline `pass:...`, `file:...` und `env:...` (Datei-
  bzw. Umgebungszugriff) werden abgelehnt. Keine Lab-Vorlage braucht diese
  beiden Flags.

Beide Schreibweisen werden geprüft: `-flag wert` (zwei Tokens, so nimmt
openssl Werte immer entgegen) und `--flag=wert` (ein Token, git-typisch).
Bewusst **kein** pauschales „jedes Token mit `/` ablehnen“: Die
Openssl-Vorlagen geben z. B. `-subj /CN=www.nordwind-logistik.de` mit, ein
mit `/` beginnender Wert, der zu keinem Pfad-Flag gehört — eine pauschale
Sperre über alle Token hätte diese Vorlage gebrochen. Die Prüfung bleibt
darum flag-spezifisch: konservativ heißt hier „die bekannten Pfad-Flags
lückenlos geprüft“, nicht „jedes Token geprüft“.

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
- **Missbrauch durch Berechtigte.** Wer sich anmelden darf, darf Code
  ausführen. Der Teilnehmerkreis ist die eigentliche Zugangskontrolle.

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
Runner eingehängt. Ein Token gibt es bewusst nicht mehr: Ohne Netzwerk ist das
Volume die Grenze, ein geteiltes Geheimnis würde daran nichts verbessern.

**Ausschalten:** `LAB_QUEUE_DIR` leeren und neu ausrollen. Die API antwortet
dann mit `503`, das Widget zeigt einen Hinweis, der Kurs läuft weiter.

**Erkennen, ob es aus ist:** Als angemeldeter Teilnehmer `GET /api/lab/status`
aufrufen — die Antwort ist `{"enabled": false}`.

## Betriebshinweise

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
