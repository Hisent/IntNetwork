Stand: v1.43.0 (2026-10-13) · Quelle: docs/lab-sicherheit.md, runner/worker.py, docker-compose.yml, backend/app/routers/lab.py

# IntLab: Sicherheit des Labs

Diese Seite beschreibt, was beim Ausführen von Teilnehmer-Aufträgen im Lab passiert, welche Grenzen gezogen sind und welche ausdrücklich nicht. Sie ist die Grundlage für die Entscheidung, ob das Lab auf einem Server eingeschaltet wird. Das Lab ist standardmäßig aus.

## Kernaussage

Ein Ansible-Playbook ist ausführbarer Code. Module wie `command`, `shell` und `script` gehören zum normalen Umfang und lassen sich nicht sinnvoll wegfiltern; eine Sperrliste wäre eine Einladung, sie zu umgehen. Wer ein Playbook schreiben darf, führt im Runner-Container Code aus. Das ist der Zweck des Labs.

Deshalb ist der Container die Sicherheitsgrenze, nicht eine Filterliste.

## Auftragsarten

Jede Art wird einzeln freigegeben (`RUNNER_KINDS` beim Runner, `LAB_KINDS` beim Backend, Standard jeweils nur `ansible`).

| Art | Was ausgeführt wird | Angriffsfläche |
|---|---|---|
| `ansible` | Playbook des Teilnehmers | beliebiger Code im Container; der Container ist die Grenze |
| `openssl` | bis zu sechs `openssl`-Aufrufe auf mitgeschickten Dateien | geschlossene Liste lokaler Unterkommandos, keine Shell, kein Netz |
| `git` | `git`-Aufrufe im Arbeitsverzeichnis | geschlossene Liste lokaler Unterkommandos, keine Shell, kein Netz |

Bei `openssl` und `git` zerlegt der Runner die Zeile mit `shlex.split`, setzt das Programm selbst davor und ruft es ohne `shell=True` auf. Es gibt keine Pipes, Umleitungen oder Verkettung.

Bewertung: `ansible` erlaubt beliebige Codeausführung, `openssl` und `git` nur Datei-Ein- und -Ausgabe über eine kleine, geschlossene Liste. Ein Durchlauf, der nur den PKI-Lehrgang fährt, kann deshalb `openssl` freigeben und `ansible` weglassen; dann ist der Container kein Sandkasten für fremden Code mehr. Ist `ansible` freigegeben, ändern zusätzliche Werkzeuge im Image nichts an der Bewertung.

## Sandbox-Schichten

### Container und Zuschnitt

- **Das Backend führt nichts aus.** Es kennt `SECRET_KEY` und die Datenbank, nimmt das Playbook entgegen, legt es als Auftrag ab und wartet auf das Ergebnis.
- **Der Runner hat kein Netzwerk:** `network_mode: "none"`, also keine Adresse, keine Namensauflösung, kein Socket.
- **Austausch über ein gemeinsames Volume:** Das Backend schreibt `/queue/in/<id>.json`, der Runner antwortet mit `/queue/out/<id>.json`. Beide Seiten schreiben zuerst eine temporäre Datei und benennen sie atomar um.
- Unprivilegierter Benutzer (uid 10001), `cap_drop: ALL`, `no-new-privileges`, `read_only` für das Wurzeldateisystem.
- Einziger Schreibort ist ein `tmpfs` mit `noexec` (64 MB). Dass Ansible auf einem `noexec`-Dateisystem läuft, wurde geprüft (Module laufen über den Python-Interpreter).
- Zeitgrenze je Lauf (`RUNNER_TIMEOUT`, Standard 30 s), Obergrenze für die Ergebnis-Ausgabe, begrenzte Parallelität (`RUNNER_MAX_PARALLEL`, Standard 2). Die Ausgabe des Kindprozesses wird zuerst in einer temporären Datei im `tmpfs` gesammelt; unbegrenzte Ausgabe kann den RAM des Workers nicht füllen.
- CPU-, Speicher- und Prozessgrenzen am Container.
- Jeder Lauf in einem frischen Verzeichnis, das danach gelöscht wird.
- Arbeitsverzeichnis je Teilnehmer: Der Runner erhält vom Backend eine undurchsichtige Kennung (HMAC über die Teilnehmer-ID mit dem `SECRET_KEY`) und legt darunter ein Verzeichnis an, das zwischen Läufen bestehen bleibt (als `lab_dir` an das Playbook übergeben). Verzeichnisse älter als 12 Stunden werden aufgeräumt.
- Im Backend: Anmeldepflicht (Teilnehmer-Token), Rate-Limit (20 Läufe pro Minute), Größengrenzen für Playbook, Inventar und Zusatzvariablen.

### Warum `network_mode: none` und kein internes Docker-Netz

Der erste Entwurf war ein HTTP-Dienst in einem Netz mit `internal: true`. Am 21.07.2026 zeigte sich auf Coolify, dass das nicht reicht: Coolify hängt jeden Dienst zusätzlich in das Projekt-Netz, das nicht intern ist. Aus dem Runner-Container waren `1.1.1.1:443` erreichbar, DNS funktionierte, und Datenbank und Backend lagen im selben Netz. `network_mode: "none"` ist die strukturelle Antwort; sie hängt nicht an einer Firewall-Regel, die jemand später entfernt.

### Argumentprüfung für `git` und `openssl`

Der Runner prüft die Kommandozeile vor dem Prozessstart (`runner/worker.py`, `_werkzeug_argv_pruefen`). „Kein Netz, keine Shell“ allein reicht nicht: Manche Werkzeuge bringen selbst netz- oder codeausführende Fähigkeiten mit. Vor dieser Sperre ließ sich über den git-eigenen `ext`-Transport beliebiger Shell-Code ausführen, trotz `network_mode: none`:

```text
-c protocol.ext.allow=always clone ext::sh -c 'beliebiger_befehl' /tmp/x
```

Die Prüfung hat drei Schichten.

| Schicht | Regel |
|---|---|
| 1. Allowlist der Unterkommandos | Das erste Nicht-Options-Token muss ein bewusst lokales Unterkommando sein (git: z. B. `init`, `status`, `add`, `commit`, `checkout`, `merge`, `worktree`, `mv`; openssl: z. B. `genrsa`, `req`, `x509`, `verify`). Nicht erlaubt: `clone`, `fetch`, `push`, `pull`, `remote`, `submodule` und `config` (git), `s_client` und `s_server` (openssl). Abweisung mit `rc=2` und Meldung, bevor ein Prozess startet. |
| 2. Immer verbotene Flags und Muster | Unabhängig von der Position. git: `-c`, `--config-env`, `--exec`, `--exec-path`, `--upload-pack`, `--receive-pack`, `-u`, `-C`, `--git-dir`, `--work-tree`, `--template`, `--separate-git-dir` (auch in der von git akzeptierten abgekürzten Form, z. B. `--templ=…`) sowie jedes Argument mit `ext::`, `fd::` oder `file://`. openssl: `-engine`, `-provider`, `-provider-path`, `-config`, `-exec`. |
| 3. Pfadwerte im Arbeitsverzeichnis | Werte pfadwertiger Argumente müssen im Arbeitsverzeichnis bleiben: nicht absolut, kein `..`, kein `\`, keine Steuerzeichen. |

Details zu Schicht 3:

- **openssl:** fail-closed über alle Tokens. Kein Token darf `/`, `\`, `..` oder Steuerzeichen enthalten. Ausnahmen sind die Werte von `-subj` (jedes `/`-Segment muss `typ=wert` sein) und `-addext` (muss mit `name=` beginnen, kein `..`, kein `file:`-URI, kein `@abschnitt`- oder `dirName:`-Verweis in eine Konfigurationsdatei; `email:a@b.de` bleibt erlaubt). `-passin`, `-passout` und `-pass` nehmen nur ein inline `pass:...` an. Optionen werden vor dem Vergleich normalisiert, weil openssl auch `--flag` und `-flag=wert` akzeptiert.
- **git:** fail-closed über alle Tokens. Jedes Positionsargument und jeder `--opt=wert`-Wert muss im Arbeitsverzeichnis bleiben. Relative Unterpfade mit `/` bleiben erlaubt (Zweignamen wie `feature/x`, `add src/app.py`). Grenze: lexikalisch, Symlink-Ausbrüche werden nicht erkannt, und git kann im Arbeitsverzeichnis Symlinks anlegen.
- Warum `--git-dir`, `--work-tree`, `--template` und `--separate-git-dir` gesperrt sind: Sie passierten den Pfadfilter mit einem relativen Pfad; `init --template=<dir>` kopiert zudem Hooks ins neue Repository (Code beim nächsten `commit`).
- Ohne Schicht 3 ließ sich beliebiger Dateiinhalt aus dem Container lesen (`openssl enc -base64 -in /etc/passwd`) oder in das mit dem Backend geteilte `/queue`-Volume schreiben (`git diff --output=/queue/x`, `openssl req -out /queue/x`).

Zusätzlich setzt der Runner für `git` `GIT_ALLOW_PROTOCOL=file` in der Prozessumgebung. Das sperrt Netztransporte (`ext`, `ssh`, `http`, `git`, …) auf Umgebungsebene als zweite, unabhängige Verteidigung. Sie ergänzt die Allowlist und ersetzt sie nicht.

Wichtig für Autoren von Lab-Vorlagen: Es bleibt eine Allowlist, keine Blockliste. Ein neues Unterkommando funktioniert erst, wenn es bewusst in `runner/worker.py` freigeschaltet wird; sonst scheitert die Vorlage mit einer regulären `rc=2`-Meldung, nicht mit einem Absturz.

### Ergebnis-Token (Zwischenstufe gegen gefälschte Ergebnisse, seit v1.43)

- Das Backend legt in jeden Auftrag ein Zufalls-Token (`secrets.token_urlsafe(32)`, `backend/app/routers/lab.py`).
- Der Runner liest den Auftrag beim Beanspruchen und löscht die Datei sofort (`_auftrag_lesen` in `runner/worker.py`). Danach existiert das Token nur noch im Speicher des Workers; er legt es dem Ergebnis bei.
- Das Backend nimmt `out/<id>.json` nur an, wenn das Token stimmt und alle Felder vorhanden sind. Sonst antwortet es mit `502` und klarer Meldung statt eines ungeprüft durchgereichten Inhalts.

Was das verhindert: das „blinde“ Fälschen. Ein Playbook, das einfach `out/<fremde-id>.json` schreibt, wird verworfen; ebenso kaputte oder unvollständige Ergebnisdateien (vorher `500`).

Was es nicht verhindert, solange Playbook und Worker dieselbe uid haben:

1. **Lesen des Auftrags vor dem Beanspruchen.** `in/<id>.json` liegt lesbar im Volume, bis der Worker sie beansprucht (im Normalfall höchstens `RUNNER_POLL_SECONDS`, 0,2 s; bei voller Warteschlange `RUNNER_MAX_QUEUE_DEPTH` beliebig lange, und die Warteschlange kann der Angreifer mit eigenen langen Läufen füllen). Ein Playbook, das `in/` in einer Schleife abfragt, liest das Token und kann damit ein gültiges Ergebnis schreiben oder den Auftrag austauschen.
2. **Lesen des Worker-Speichers.** Gleiche uid und gleiche (leere) Capability-Menge: `/proc/<pid>/mem` und `ptrace` des Workers sind erlaubt, sofern der Host es nicht per Yama unterbindet (`kernel.yama.ptrace_scope` ≥ 1; Ubuntu-Standard 1, Debian-Standard 0). Auf das Host-Setting darf sich das Bedrohungsmodell nicht verlassen.
3. **Stören.** Aufträge und Ergebnisse löschen, den Worker per Signal beenden (gleiche uid).

Rollout: Backend und Runner gemeinsam ausrollen. Ein neuer Runner mit altem Backend funktioniert (kein Token im Auftrag, keines im Ergebnis). Ein neues Backend mit altem Runner verwirft jedes Ergebnis mit `502`.

## Bekannte Restrisiken (nicht abgedeckt)

- **Ausbruch aus dem Container.** Eine Lücke im Kernel oder in der Container-Laufzeit hebelt die Isolierung aus. Wer das im Bedrohungsmodell braucht, muss auf VM-Isolierung wechseln (eigene Maschine, Firecracker, gVisor).
- **Rechenzeit.** Angemeldete Teilnehmer können den Runner beschäftigen. Zeitgrenze, Parallelitätsgrenze und CPU-Limit bremsen das, verhindern es aber nicht vollständig.
- **Böswillig abgekoppelte Prozesse.** Ein Programm kann die Prozessgruppe mit `setsid()` verlassen. Es blockiert den Worker nicht mehr über eine offene Ausgabe-Pipe, läuft aber bis zum Container-Limit weiter. Eine harte Grenze braucht einen separaten Job-Container oder eine VM/cgroup je Lauf.
- **Alles im Runner-Container.** Ein Playbook kann das Image und die Arbeitsverzeichnisse anderer Teilnehmer im selben Container lesen. Dort liegen keine Geheimnisse und keine Nutzerdaten, aber es ist keine Trennung wie zwischen zwei Maschinen.
- **Die gemeinsame Warteschlange `/queue`.** Der Runner braucht dort Schreibrechte, und ein Playbook läuft mit genau diesen Rechten. Ein böswilliger Teilnehmer kann fremde Aufträge und Ergebnisse lesen, verändern oder löschen, fremde Läufe stören oder deren Ausgabe fälschen. Nach außen (Backend, Datenbank, Netz) führt von dort kein Weg. Wer das nicht tragen will, gibt `ansible` nicht frei. `openssl` und `git` sind enger, aber keine absolute Garantie: Es bleibt eine von Hand gepflegte Allowlist, kein Beweis, dass jedes zugelassene Unterkommando in jeder Argumentkombination harmlos ist. Das Ergebnis-Token erschwert das Fälschen, schließt die Lücke aber nicht.
- **Missbrauch durch Berechtigte.** Wer sich anmelden darf, darf Code ausführen. Der Teilnehmerkreis ist die eigentliche Zugangskontrolle.

Wann man das Lab besser auslässt:

- Der Teilnehmerkreis ist nicht vertrauenswürdig (offene Anmeldung, externe Gäste ohne Aufsicht).
- Der Host trägt andere, sensible Dienste, sodass eine Container-Lücke entsprechend teuer wäre.
- Niemand hat die Auslastung im Blick.

## Offener Umsetzungsplan: Läufe unter einer zweiten uid (NICHT umgesetzt)

Nicht umgesetzt, weil es sich ohne Docker/Linux nicht belastbar testen lässt: `setuid()` braucht Root bzw. Capabilities, und deren Zusammenspiel mit `cap_drop`, `no-new-privileges`, Volume-Rechten und `tmpfs` ist der riskante Teil. Ein Fehler macht das Lab unbenutzbar oder gibt Playbooks Root im Container.

Ziel: Worker = uid 0 mit minimalen Capabilities, Läufe = uid 10002 ohne Capabilities. Dann kann ein Lauf weder `/queue` noch den Worker-Prozess anfassen; die Punkte 1 bis 3 des Ergebnis-Tokens entfallen. Das Ergebnis-Token bleibt danach als zweite Schicht sinnvoll.

Schritte (Zeilenangaben der Quelle beziehen sich auf den Stand der Dokumentation):

1. `runner/Dockerfile`: zweiten Benutzer `labjob` (uid/gid 10002) anlegen; `USER labrunner` entfernen (Worker startet als root); `/queue/in` und `/queue/out` als `root:10001` mit Modus `0770` anlegen (10001 ist uid/gid des Backend-Containers, `backend/Dockerfile`). Das Backend schreibt über die Gruppe, `labjob` kommt nicht hinein. Kein `0777` mehr.
2. `docker-compose.yml`, Dienst `runner`: `cap_drop: ALL` behalten, dazu `cap_add: [SETUID, SETGID, KILL, CHOWN, DAC_OVERRIDE]`. `KILL`: Root ohne `CAP_KILL` darf Prozesse einer fremden uid nicht beenden, sonst greift die Zeitgrenze (`os.killpg`) nicht. `CHOWN` und `DAC_OVERRIDE`: Arbeitsverzeichnisse an `labjob` übergeben und aufräumen. `no-new-privileges` und `read_only` bleiben; `tmpfs` bleibt `mode=1777,noexec`.
3. `runner/worker.py`:
   - `_mit_zeitgrenze_ausfuehren`: `subprocess.Popen(..., user=JOB_UID, group=JOB_GID, extra_groups=[])` mit neuen Konstanten aus `RUNNER_JOB_UID` (Standard: keine Trennung, damit Tests und lokale Läufe unverändert bleiben). Der Wechsel von uid 0 auf 10002 leert die Capability-Mengen des Kindes.
   - `_workspace`, `_run_ansible` (`mkdtemp`) und `_run_werkzeug`: jedes Verzeichnis, in das der Lauf schreibt (`lab_dir`, `HOME`, `ANSIBLE_LOCAL_TEMP`), nach dem Anlegen per `os.chown(..., JOB_UID, JOB_GID)` übergeben, Modus `0700`.
   - `_antwort_schreiben` und `_warteschlange_vorbereiten`: `chmod 0o666`/`0o777` durch `0o640`/`0o770` ersetzen und `os.chown(..., 0, BACKEND_GID)`.
   - Startprüfung in `main()`: Läuft der Worker als uid 0 ohne gesetzte `RUNNER_JOB_UID`, nicht starten (sonst liefen Playbooks als root).
4. Bestehendes Volume: `lab_queue` einmal entfernen. Rechte werden nur in ein leeres Volume übernommen.
5. Testschritte (Linux mit Docker, vor dem Merge):
   - `docker compose up runner`; Playbook mit `command: id` muss uid=10002 zeigen, und `grep Cap /proc/self/status` muss `CapEff: 0000000000000000` liefern.
   - Playbook `command: ls /queue/in` muss „Permission denied“ liefern; `cat /proc/1/environ` und `kill -9 1` müssen abgelehnt werden.
   - Playbook `command: sleep 300` wird nach `RUNNER_TIMEOUT` beendet (`docker top` zeigt keinen `sleep` mehr).
   - Regulärer Lauf zweimal (Idempotenz-Übung), je einmal `openssl` und `git`.
   - Backend-Seite: Auftrag wird angenommen, Ergebnis gelesen und gelöscht (kein `PermissionError` im Backend-Log).
   - `docker inspect` zeigt unverändert `NetworkMode: none`.

## Ein- und Ausschalten

Einschalten (Umgebung des Backends):

```text
LAB_QUEUE_DIR=/queue
LAB_KINDS=ansible,openssl        # Backend: was die Oberfläche anbietet
RUNNER_KINDS=ansible,openssl     # Runner: was tatsächlich ausgeführt wird
```

`LAB_KINDS` und `RUNNER_KINDS` werden nicht abgeglichen, weil zwischen Backend und Runner kein Netzweg existiert. Das Volume `lab_queue` ist in `docker-compose.yml` bereits bei Backend und Runner eingehängt. Ein konfiguriertes Zugangs-Token gibt es bewusst nicht: Ohne Netzwerk ist das Volume die Grenze.

Ausschalten: `LAB_QUEUE_DIR` leeren und neu ausrollen. Die API antwortet mit `503`, das Widget zeigt einen Hinweis, der Kurs läuft weiter.

Erkennen, ob es aus ist: Als angemeldeter Teilnehmer `GET /api/lab/status` aufrufen; Antwort `{"enabled": false}`.

## Betriebshinweise

- **Basis-Image und OpenSSL:** Der Runner baut auf `python:3.12-slim-trixie` (Debian 13). Das Paket `openssl` ist dort OpenSSL 3.5 (LTS; geprüft am 12.10.2026: `3.5.7-1~deb13u3`). Mindestversion 3.5, weil die Vorlage „Post-Quanten-Schlüssel“ ML-KEM-768 und ML-DSA-65 erzeugt (`genpkey -algorithm ML-KEM-768` bzw. `ML-DSA-65`); ältere Versionen brechen mit „Algorithm … not found“ ab. Alle übrigen Befehle des PKI-Lehrgangs laufen ab 3.0. Nach einem Wechsel des Debian-Release prüfen: `docker exec <runner-container> openssl version`.
- **Logs:** Der Runner schreibt nach stderr (`docker logs <runner-container>`). Playbook-Inhalte landen bewusst nicht im Log.
- **Prüfen, ob der Runner arbeitet:** `docker logs --tail 5 <runner-container>`; erwartet wird beim Start `Lab-Runner bereit. Warteschlange: /queue, … Netzwerk: keines`. Ob die Kette insgesamt steht, zeigt am ehrlichsten ein Playbook, das zweimal ausgeführt wird.
- **Isolierung nachprüfen** (nach jedem größeren Plattform-Update): `docker inspect <runner-container> --format '{{.HostConfig.NetworkMode}}'` muss `none` liefern. Sonst das Lab abschalten, bis das geklärt ist.
- **`PermissionError: '/queue/in'` im Runner-Log:** Das Volume gehört `root`, der Runner läuft unprivilegiert. Docker übernimmt die Eigentümerschaft aus dem Image nur, wenn das Volume beim ersten Start leer ist. Volume einmal entfernen (`docker volume rm <projekt>_lab_queue`) und neu ausrollen. Der Runner stirbt in diesem Fall nicht, sondern meldet die Ursache und versucht es alle fünf Sekunden erneut.
- **Dauerlast:** `RUNNER_MAX_PARALLEL` senken oder das Lab abschalten. Läufe, die regelmäßig in die Zeitgrenze laufen, deuten eher auf zu ambitionierte Übungs-Playbooks hin als auf Missbrauch.
- **Speicher:** Das `tmpfs` ist auf 64 MB begrenzt und nach einem Neustart des Containers leer. Arbeitsverzeichnisse sind Übungsstände, kein Speicher.
