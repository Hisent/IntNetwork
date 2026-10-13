Stand: v1.43.0 + Trennung der Läufe per uid (2026-10-13) · Quelle: docs/lab-sicherheit.md, runner/worker.py, runner/Dockerfile, docker-compose.yml, backend/app/routers/lab.py, runner/tests/isolation_check.py

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
- Jeder Lauf unter einer eigenen, unprivilegierten uid (10002 bis 10009, ohne Gruppen, ohne Capabilities), getrennt vom Worker und von gleichzeitig laufenden Läufen (Abschnitt „Trennung der Läufe per uid“). Worker: uid 0 mit `cap_drop: ALL` plus genau `CHOWN`, `DAC_OVERRIDE`, `SETUID`, `SETGID`, `KILL`; dazu `no-new-privileges` und `read_only` für das Wurzeldateisystem.
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

### Ergebnis-Token (zweite Schicht gegen gefälschte Ergebnisse, seit v1.43)

- Das Backend legt in jeden Auftrag ein Zufalls-Token (`secrets.token_urlsafe(32)`, `backend/app/routers/lab.py`).
- Der Runner liest den Auftrag beim Beanspruchen und löscht die Datei sofort (`_auftrag_lesen` in `runner/worker.py`). Danach existiert das Token nur noch im Speicher des Workers; er legt es dem Ergebnis bei.
- Das Backend nimmt `out/<id>.json` nur an, wenn das Token stimmt und alle Felder vorhanden sind. Sonst antwortet es mit `502` und klarer Meldung statt eines ungeprüft durchgereichten Inhalts.

Das Token stammt aus der Zeit vor der Trennung per uid. Damals ließ es sich umgehen (Auftrag vor dem Beanspruchen lesen, Speicher des Workers lesen). Mit der Trennung kommt ein Lauf an beides nicht mehr heran. Das Token bleibt als zweite Schicht für den Fall, dass die Trennung einmal nicht greift, und fängt weiterhin kaputte oder unvollständige Ergebnisdateien ab.

Rollout: Backend und Runner gemeinsam ausrollen. Ein neuer Runner mit altem Backend funktioniert (kein Token im Auftrag, keines im Ergebnis). Ein neues Backend mit altem Runner verwirft jedes Ergebnis mit `502`.

## Trennung der Läufe per uid

Umgesetzt am 13.10.2026. Vorher lief ein Playbook unter der uid des Workers und konnte in `/queue` fremde Aufträge lesen und löschen, mit dem mitgelesenen Token Ergebnisse fälschen, fremde Arbeitsverzeichnisse lesen und ändern, den Worker beenden und dessen Speicher lesen.

### Aufbau

| Wer | uid | Rechte |
|---|---|---|
| Worker (`worker.py`) | 0 | `CHOWN`, `DAC_OVERRIDE`, `SETUID`, `SETGID`, `KILL`, sonst nichts |
| Lauf (Playbook, `openssl`, `git`) | eine aus 10002 bis 10009 | keine Capability, keine Gruppe, `umask 077` |
| Backend | 10001 | Gruppe 10001 auf `/queue` |

- **Eine uid je gleichzeitigem Lauf.** Der Worker vergibt die uids exklusiv und reihum. Mit einer gemeinsamen Job-uid könnten gleichzeitige Läufe einander lesen und beenden; so sind auch Teilnehmer untereinander getrennt. Acht uids sind die Obergrenze gleichzeitiger Läufe.
- **`/queue`** gehört `root:10001`, Modus `0750`, `in/` und `out/` `0770`: Worker und Backend ja, Läufe nein. Der Worker setzt das bei jedem Start.
- **Arbeitsverzeichnis.** Vor dem Lauf gibt der Worker es samt Inhalt der uid des Laufs (`0700`), danach nimmt er es zurück (`root`, `0700`). In Ruhe kommt keine Job-uid hinein, auch nicht der nächste Lauf mit derselben uid. Das übergeordnete Verzeichnis ist nicht auflistbar (`0711`). Ein Arbeitsverzeichnis hat höchstens einen Lauf gleichzeitig.
- **Umgebung.** `HOME`, `TMPDIR` und die Ansible-Temp-Verzeichnisse liegen im Laufverzeichnis des Laufs, bei `openssl`/`git` ist `HOME` das Arbeitsverzeichnis. Nichts zeigt nach `/queue`. Das Ergebnis-Token steht nie in einer Umgebung oder Kommandozeile.
- **Zeitgrenze und Aufräumen.** Bei Zeitüberschreitung beendet der Worker die Prozessgruppe. Nach jedem Lauf beendet er zusätzlich alle Prozesse der Job-uid, auch solche, die die Prozessgruppe mit `setsid()` verlassen haben, und löscht, was der Lauf in `/tmp` und `/dev/shm` hinterlassen hat. Gelingt das Beenden nicht, bleiben uid und Arbeitsverzeichnis bis zum Neustart gesperrt (`Job-Slot uid … GESPERRT` im Log).

### Verworfene Alternativen

| Alternative | Warum nicht |
|---|---|
| Worker unprivilegiert, Start über ein setuid-Hilfsprogramm (`setpriv`, `su`) | `no-new-privileges` macht setuid-Bits und Datei-Capabilities wirkungslos, und die Option soll bleiben |
| Worker als uid 10001 mit Capabilities | Docker gibt die Capabilities aus `cap_add` nur uid 0 |
| Zwei Container (Worker und Läufe getrennt) | bräuchte den Docker-Socket oder eine zweite Warteschlange |
| Eine gemeinsame Job-uid | gleichzeitige Läufe könnten einander lesen und beenden |
| `CAP_KILL` einsparen (Hilfsprozess unter der Job-uid ruft `kill(-1)`) | den Hilfsprozess könnte der Lauf selbst zuerst beenden |

### Was die Trennung verhindert

Ein Lauf kann nicht mehr:

- `/queue`, `/queue/in`, `/queue/out` auflisten, lesen, beschreiben oder dort löschen,
- ein fremdes Arbeitsverzeichnis lesen oder ändern, die Liste der Arbeitsverzeichnisse sehen,
- dem Worker oder einem fremden Lauf ein Signal schicken,
- `/proc/<pid>/environ`, `mem`, `cwd`, `fd` des Workers oder eines fremden Laufs lesen,
- die Zeitgrenze mit `setsid()` überleben.

### Fail-closed

Beim Start probiert der Worker aus, was er braucht (`chown` an eine Job-uid, Schreiben in deren Verzeichnis, Prozess unter der Job-uid starten und beenden, Prüfung auf leere Capabilities und `NoNewPrivs`). Scheitert ein Schritt, etwa weil `user: "0:0"` oder ein `cap_add` in der Compose-Datei fehlt:

- Im Log steht `ANSIBLE-LAB DEAKTIVIERT (fail-closed): <Schritt und Ursache>`.
- Jeder Ansible-Auftrag endet mit `rc=2` und der Meldung „Das Ansible-Lab ist auf diesem Server deaktiviert …“ (sichtbar im Widget).
- `openssl` und `git` laufen weiter, unter der uid des Workers wie vor der Trennung. Sie führen keinen frei geschriebenen Code aus, und die Argumentprüfung hält sie im Arbeitsverzeichnis.

Entwicklungsschalter (unsicher): `RUNNER_ISOLATION=aus-unsicher` lässt Playbooks ohne Trennung laufen. Nur für lokale Entwicklung ohne root und Container und für die Unit-Tests. Der Wert steht in keiner Compose-Datei und in keinem Image; ein Worker mit uid 0 verweigert ihn.

### Trennung nachprüfen

Der Test stellt echte Aufträge und lässt ein bösartiges Playbook alles versuchen, was oben als verhindert steht. Er läuft in der CI bei jedem Push (Job `runner-isolation`).

Auf einem Rechner mit Docker, im Repository (eigenes Compose-Projekt, ein laufendes System bleibt unberührt):

```text
bash ops/lab-isolation-test.sh
```

Gegen das laufende System, zum Beispiel auf dem Coolify-Server:

```text
docker exec -i <backend-container> python - < runner/tests/isolation_check.py
```

Das belegt für etwa eine Minute zwei Läufe. Jede Prüfung erscheint als Zeile `OK …` oder `FEHLER …`; Exit-Code 0 heißt: alles bestanden.

| Prüfung | Inhalt |
|---|---|
| (a) | Normales Playbook läuft unter einer Job-uid, liefert ein Ergebnis mit Token, zweiter Lauf idempotent |
| (b) | Bösartiges Playbook scheitert an `/queue`, an fremden Arbeitsverzeichnissen und am Worker (Signal, `environ`, `mem`) |
| (c) | Endlos-Playbook mit `setsid()`-Kindern wird an der Zeitgrenze beendet, danach läuft keiner seiner Prozesse mehr |
| (d) | Kursvorlagen für `openssl` (darunter die Post-Quanten-Vorlage) und `git` laufen, `openssl version` ist mindestens 3.5 |
| (e) | Zwei gleichzeitige Läufe haben verschiedene uids und kommen nicht aneinander heran |

## Bekannte Restrisiken (nicht abgedeckt)

- **Ausbruch aus dem Container.** Eine Lücke im Kernel oder in der Container-Laufzeit hebelt die Isolierung aus. Wer das im Bedrohungsmodell braucht, muss auf VM-Isolierung wechseln (eigene Maschine, Firecracker, gVisor).
- **Rechenzeit.** Angemeldete Teilnehmer können den Runner beschäftigen. Zeitgrenze, Parallelitätsgrenze und CPU-Limit bremsen das, verhindern es aber nicht vollständig.
- **Was Läufe trotz Trennung gemeinsam haben.** Alle Läufe teilen sich Kernel, Image, Rechenzeit, das 64-MB-`tmpfs` und die Prozessgrenze (128). Die Prozessliste ist nicht verborgen: Ein Lauf sieht die Kommandozeilen anderer Läufe, darin den Pfad des fremden Arbeitsverzeichnisses und dessen `extra_vars` (deshalb keine Geheimnisse in `extra_vars`), nicht aber Umgebung, Speicher oder Dateien. `/tmp` und `/dev/shm` sind für alle beschreibbar; der Worker räumt sie nach jedem Lauf auf. Ein Lauf kann das `tmpfs` füllen oder die Prozessgrenze ausschöpfen und damit andere Läufe scheitern lassen, solange er läuft (höchstens `RUNNER_TIMEOUT`).
- **Der Worker ist root im Container.** Mit `SETUID`, `CHOWN` und `DAC_OVERRIDE` hat er vollen Zugriff auf `/queue` und alle Arbeitsverzeichnisse (wie vorher unter uid 10001). Neu ist: Ein ausnutzbarer Fehler im Worker selbst hätte diese Capabilities. Das Netz bleibt aus, das Wurzeldateisystem nur lesbar, nach außen führt nur `/queue`.
- **Missbrauch durch Berechtigte.** Wer sich anmelden darf, darf Code ausführen. Der Teilnehmerkreis ist die eigentliche Zugangskontrolle.

Wann man das Lab besser auslässt:

- Der Teilnehmerkreis ist nicht vertrauenswürdig (offene Anmeldung, externe Gäste ohne Aufsicht).
- Der Host trägt andere, sensible Dienste, sodass eine Container-Lücke entsprechend teuer wäre.
- Niemand hat die Auslastung im Blick.

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
- **Prüfen, ob der Runner arbeitet:** `docker logs --tail 5 <runner-container>`; erwartet werden beim Start `Trennung aktiv: Läufe unter uid 10002-10009, ohne Capabilities.` und `Lab-Runner bereit. Warteschlange: /queue, … Netzwerk: keines, …, Trennung: uid je Lauf`. Steht dort `ANSIBLE-LAB DEAKTIVIERT`, nennt dieselbe Zeile die Ursache. Ob die Kette insgesamt steht, zeigt am ehrlichsten ein Playbook, das zweimal ausgeführt wird.
- **Isolierung nachprüfen** (nach jedem größeren Plattform-Update): `docker inspect <runner-container> --format '{{.HostConfig.NetworkMode}}'` muss `none` liefern. Sonst das Lab abschalten, bis das geklärt ist.
- **Rechte von `/queue`:** Der Worker setzt sie bei jedem Start selbst (`root:10001`, `0750`/`0770`), auch auf einem Volume einer älteren Fassung (uid 10001, `0777`). Das Volume muss dafür nicht mehr entfernt werden. Gelingt es nicht, meldet der Runner alle fünf Sekunden `Warteschlange … lässt sich nicht für Läufe schließen` und nimmt keine Aufträge an. Rollout einer bestehenden Installation: Seite „Betrieb“, Abschnitt „Rollout: Trennung der Lab-Läufe“.
- **`Job-Slot uid … GESPERRT` im Runner-Log:** Prozesse eines Laufs ließen sich nicht beenden. Der Slot und das betroffene Arbeitsverzeichnis bleiben außer Betrieb, die übrigen arbeiten weiter. Runner-Container neu starten.
- **Dauerlast:** `RUNNER_MAX_PARALLEL` senken oder das Lab abschalten. Läufe, die regelmäßig in die Zeitgrenze laufen, deuten eher auf zu ambitionierte Übungs-Playbooks hin als auf Missbrauch.
- **Speicher:** Das `tmpfs` ist auf 64 MB begrenzt und nach einem Neustart des Containers leer. Arbeitsverzeichnisse sind Übungsstände, kein Speicher.
