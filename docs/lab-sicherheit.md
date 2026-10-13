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

Die Sperre hat drei Schichten:

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
   `--git-dir`, `--work-tree`, `--template`, `--separate-git-dir` (die
   letzten vier passierten den Pfadfilter mit einem relativen Pfad;
   `init --template=<dir>` kopiert Hooks ins Repository) — auch in der von git
   akzeptierten abgekürzten Form (`--templ=…`) —, sowie jedes Argument, das `ext::`, `fd::` oder
   `file://` enthält; für openssl `-engine`, `-provider`, `-provider-path`, `-config`, `-exec`
   (jeweils Wege, eine beliebige Bibliothek nachzuladen oder ein
   Skript/Programm zu übernehmen).
3. **Pfadwerte im Arbeitsverzeichnis.** Werte pfadwertiger Argumente dürfen
   das Arbeitsverzeichnis nicht verlassen (Details unten, „Dritte Schicht“).

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
  muss `typ=wert` sein) und `-addext` (muss mit `name=` beginnen, kein `..`,
  kein `file:`-URI, kein `@abschnitt`-/`dirName:`-Verweis in eine
  Konfigurationsdatei; `email:a@b.de` bleibt erlaubt).
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
- **Jeder Lauf unter einer eigenen, unprivilegierten uid** (10002–10009, ohne
  Gruppen, ohne Capabilities) — getrennt vom Worker (uid 0 mit fünf
  Capabilities) und von gleichzeitig laufenden Läufen. Einzelheiten im Abschnitt
  „Trennung der Läufe per uid“.
- `cap_drop: ALL` plus genau `CHOWN`, `DAC_OVERRIDE`, `SETUID`, `SETGID`,
  `KILL` für den Worker, `no-new-privileges`, `read_only` für das
  Wurzeldateisystem.
- Schreiborte sind zwei `tmpfs`: `/tmp` (64 MB, mit den Arbeitsverzeichnissen)
  und `/dev/shm` (16 MB, Ansible braucht es für Semaphoren). Beide mit
  `noexec`, `nosuid`, `nodev` — ein Playbook kann dort keine eigene Binärdatei
  ausführen, und setuid-Bits oder Gerätedateien sind wirkungslos. Dass Ansible
  auf einem `noexec`-Dateisystem trotzdem läuft, wurde geprüft (Module laufen
  über den Python-Interpreter, nicht als eigenständige Programme).
- Die Ausgabe eines Laufs wird bereinigt, bevor sie ins Ergebnis geht
  (`_bereinigen`): ANSI-Sequenzen fallen weg, alle übrigen Steuerzeichen außer
  Zeilenumbruch und Tabulator (NUL, Rücklauf, ESC, C1 …) werden durch `�`
  ersetzt, `\r` wird zu `\n`. Ansible läuft zusätzlich mit `ANSIBLE_NOCOLOR=1`.
  Das Frontend zeigt die Ausgabe als reinen Text (`<pre>`, kein HTML).
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
- **Was Läufe trotz Trennung gemeinsam haben.** Alle Läufe teilen sich den
  Container: Kernel, Image, Rechenzeit, das 64-MB-`tmpfs` und die Prozessgrenze
  (128). Konkret:
  - *Prozessliste.* `/proc` ist nicht verborgen (`hidepid` bräuchte
    `CAP_SYS_ADMIN`). Ein Lauf sieht, dass andere Läufe existieren, samt deren
    Kommandozeile — darin der Pfad des fremden Arbeitsverzeichnisses und die
    Zusatzvariablen (`extra_vars`) des fremden Laufs. Umgebung, Speicher,
    Arbeitsverzeichnis und offene Dateien des fremden Laufs sieht er nicht.
    **Deshalb: keine Geheimnisse in `extra_vars`.**
  - *Kernel-Schalter des Hosts.* `fs.protected_hardlinks` und
    `fs.protected_symlinks` (Standard 1 auf Debian/Ubuntu) sind eine zweite
    Schicht hinter den Maßnahmen oben. Der Worker verlässt sich nicht auf sie,
    meldet beim Start aber `WARNUNG: fs.protected_…=0`, wenn sie fehlen. Kein
    Sperrgrund: Ohne sie kann ein Lauf zwar einen Hardlink auf eine fremde, für
    ihn lesbare Datei in `/tmp` anlegen, der Worker übergibt ihm die Datei aber
    nicht (siehe „Was nach einem Lauf im Arbeitsverzeichnis bleibt“).
  - *Erfolgskriterien im Kurs.* Ob eine Lab-Aufgabe als gelöst gilt, liest das
    Frontend aus Rückgabewert und Ausgabe des eigenen Laufs. Wer die Ausgabe
    passend präpariert, täuscht nur die eigene Anzeige — das ist Selbstbetrug,
    kein Zugriff auf Fremdes, und wird nicht verhindert.
  - *`/tmp` und `/dev/shm`.* Beide sind für alle beschreibbar. Was ein Lauf
    dort ablegt, können gleichzeitig laufende Läufe lesen, wenn die Datei für
    alle lesbar ist (Standard-`umask` der Läufe ist `077`, also nein — außer das
    Playbook setzt den Modus selbst). Nach dem Lauf räumt der Worker auf.
  - *Verdrängen.* Ein Lauf kann das `tmpfs` füllen oder die Prozessgrenze
    ausschöpfen und damit andere Läufe scheitern lassen, solange er läuft
    (höchstens `RUNNER_TIMEOUT`). Danach beendet der Worker alle seine Prozesse
    und löscht seine Dateien.
- **Der Worker ist root im Container.** Mit `SETUID`, `CHOWN` und
  `DAC_OVERRIDE` ist das im Container gleichbedeutend mit vollem Zugriff auf
  `/queue` und alle Arbeitsverzeichnisse — das hatte er vorher auch, nur unter
  uid 10001. Neu ist: Ein Fehler **im Worker selbst** (nicht im Playbook), der
  sich von einem Auftrag ausnutzen ließe, hätte diese Capabilities. Das Netz
  bleibt aus, das Wurzeldateisystem nur lesbar, und nach außen führt weiterhin
  nur `/queue`. Die Stellen, an denen der Worker als root Dateien eines Laufs
  anfasst, folgen keinem Symlink (`_uebergeben`, `_datei_schreiben`).
- **Dieselbe Person gegen sich selbst.** Zwei Auftragsarten derselben Person
  teilen sich ein Arbeitsverzeichnis. Ein Playbook kann dort z. B. einen
  git-Hook hinterlegen, den ein späterer `git`-Auftrag ausführt. Das bleibt
  folgenlos: Auch `openssl`- und `git`-Aufträge laufen unter einer Job-uid.
- **Missbrauch durch Berechtigte.** Wer sich anmelden darf, darf Code
  ausführen. Der Teilnehmerkreis ist die eigentliche Zugangskontrolle.

## Trennung der Läufe per uid

Umgesetzt am 13.10.2026 (`runner/worker.py`, `runner/Dockerfile`,
`docker-compose.yml`). Vorher lief ein Playbook unter der uid des Workers und
konnte in `/queue` fremde Aufträge lesen und löschen, mit dem mitgelesenen
Token Ergebnisse fälschen, fremde Arbeitsverzeichnisse lesen und ändern, den
Worker beenden und dessen Speicher lesen.

### Aufbau

| Wer | uid | Rechte |
|---|---|---|
| Worker (`worker.py`) | 0 | `CHOWN`, `DAC_OVERRIDE`, `SETUID`, `SETGID`, `KILL` — sonst nichts |
| Lauf (Playbook, `openssl`, `git`) | eine aus 10002–10009 | keine Capability, keine Gruppe, `umask 077` |
| Backend | 10001 | Gruppe 10001 auf `/queue` |

- **Eine uid je gleichzeitigem Lauf.** Der Worker vergibt die uids exklusiv
  und reihum (`_job`). Mit *einer* gemeinsamen Job-uid könnten gleichzeitige
  Läufe einander lesen und beenden; so sind auch Teilnehmende untereinander
  getrennt. Acht uids sind die Obergrenze gleichzeitiger Läufe
  (`RUNNER_MAX_PARALLEL` darüber wartet auf einen freien Slot).
- **`/queue`** gehört `root:10001`, Modus `0750`, `in/` und `out/` `0770`:
  Worker und Backend ja, Läufe nein. Der Worker setzt das bei jedem Start.
- **Arbeitsverzeichnis.** Vor dem Lauf gibt der Worker es samt Inhalt der uid
  des Laufs (`0700`), danach nimmt er es zurück (`root`, `0700`). In Ruhe
  kommt also keine Job-uid hinein — auch nicht der nächste Lauf, der dieselbe
  uid bekommt. Das übergeordnete Verzeichnis ist `0711`: nicht auflistbar. Ein
  Arbeitsverzeichnis hat höchstens einen Lauf gleichzeitig; ein zweiter Auftrag
  derselben Person wartet.
- **Umgebung.** Jeder Lauf bekommt ein frisches Laufverzeichnis, das ihm
  gehört und danach gelöscht wird. Ansible: `HOME`, `TMPDIR`,
  `ANSIBLE_LOCAL_TEMP` und `ANSIBLE_REMOTE_TEMP` liegen dort. `openssl`/`git`:
  `TMPDIR` liegt dort (nicht im gemeinsamen `/tmp`), `HOME` ist das
  Arbeitsverzeichnis, `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` zeigen auf
  `/dev/null`. Nichts davon zeigt nach `/queue`. Die Standardeingabe ist
  `/dev/null`, nicht die des Workers. Das Ergebnis-Token steht nie in einer
  Umgebung oder Kommandozeile, nur im Speicher des Workers.
- **Der Worker folgt keinem Symlink eines Laufs.** Er ist root und fasst
  Dateien an, die Läufe angelegt haben. Überall dort arbeitet er über
  Deskriptoren (`O_NOFOLLOW`, `os.fwalk`, `dir_fd`) statt über Pfade:
  beim Übergeben und Zurücknehmen (`_uebergeben`), beim Anlegen mitgeschickter
  Dateien und der Ergebnisdatei (`_exklusiv_schreiben`: alten Eintrag
  entfernen, dann `O_EXCL|O_NOFOLLOW`), beim Lesen eines Auftrags
  (`_regulaer_lesen`: nur reguläre Dateien, ein FIFO hält ihn nicht an) und
  beim Setzen der Rechte von `/queue` (`_verzeichnis_sichern`). Ist `in/` oder
  `out/` in einem Bestands-Volume ein Symlink, wird er entfernt und durch ein
  echtes Verzeichnis ersetzt — das Ziel bleibt unberührt.
- **Was nach einem Lauf im Arbeitsverzeichnis bleibt.** Bei der Rücknahme
  entfernt der Worker FIFOs, Sockets und Gerätedateien, löscht
  setuid/setgid/sticky und entfernt Dateien mit mehr als einem Hardlink
  (ein Hardlink kann auf eine fremde Datei desselben Dateisystems zeigen; ein
  `chown` gäbe sie dem Lauf — **Hardlinks überleben einen Lauf deshalb nicht**).
  In Ruhe gehört das Verzeichnis selbst root (`0700`), sein Inhalt weiter der
  letzten Job-uid; root gehört darin nichts. Der nächste Lauf bekommt alles an
  seine uid. Zu setuid-Bits im Besonderen: Linux löscht sie bei jedem `chown`
  auf eine Datei, auch für root (seit 2.2.13); der Worker verlässt sich nicht
  darauf und löscht sie selbst, und `/tmp` ist `nosuid` eingehängt.
- **Zeitgrenze und Aufräumen.** Bei Zeitüberschreitung beendet der Worker
  die Prozessgruppe (`CAP_KILL`). Nach **jedem** Lauf beendet er zusätzlich
  alle Prozesse der Job-uid (`_job_prozesse_beenden`: erst `SIGSTOP`, dann
  `SIGKILL`, bis keiner mehr da ist; gesendet über ein `pidfd` nach erneuter
  Prüfung der uid, damit eine inzwischen neu vergebene pid nicht den Falschen
  trifft) — das erfasst auch Prozesse, die die
  Prozessgruppe mit `setsid()` verlassen haben. Diese frühere Lücke ist damit
  geschlossen. Danach löscht er, was der Lauf in `/tmp` und `/dev/shm`
  hinterlassen hat. Gelingt das Beenden nicht, bleiben uid und
  Arbeitsverzeichnis bis zum Neustart gesperrt (`Job-Slot uid … GESPERRT` im
  Log).

### Warum so und nicht anders

- **Worker unprivilegiert, Start über ein setuid-Hilfsprogramm
  (`setpriv`, `su`)?** Geht nicht: `no-new-privileges` macht setuid-Bits und
  Datei-Capabilities wirkungslos, und genau diese Option soll bleiben — sie
  verhindert, dass ein Lauf über `su`/`mount` im Image Rechte zurückholt.
- **Worker als uid 10001 mit Capabilities statt root?** Docker gibt die
  Capabilities aus `cap_add` nur uid 0; ein Nicht-root-Benutzer startet mit
  leerer Menge.
- **Zwei Container (Worker und Läufe getrennt)?** Bräuchte den Docker-Socket
  oder eine zweite Warteschlange; deutlich mehr bewegliche Teile.
- **`CAP_KILL` einsparen**, indem ein Hilfsprozess unter der Job-uid
  `kill(-1)` ruft? Den Hilfsprozess könnte der Lauf selbst zuerst beenden.
- **`CAP_FOWNER` wird nicht gebraucht:** Der Worker nimmt eine Datei erst an
  sich (`chown`) und ändert dann ihre Rechte.

### Was die Trennung verhindert

Ein Lauf kann **nicht** mehr: `/queue`, `/queue/in`, `/queue/out` auflisten,
lesen, beschreiben oder dort löschen; ein fremdes Arbeitsverzeichnis lesen oder
ändern (ob dessen Besitzer gerade läuft oder nicht); die Liste der
Arbeitsverzeichnisse sehen; dem Worker oder einem fremden Lauf ein Signal
schicken; `/proc/<pid>/environ`, `mem`, `cwd`, `fd` des Workers oder eines
fremden Laufs lesen; die Zeitgrenze mit `setsid()` überleben. Das alles prüft
`runner/tests/isolation_check.py` im echten Container (siehe unten). Was
bleibt, steht unter „Was NICHT abgedeckt ist“.

### Fail-closed: wenn die Trennung nicht eingerichtet werden kann

Beim Start probiert der Worker aus, was er braucht (`_isolation_probe`):
`chown` an eine Job-uid, Schreiben in deren `0700`-Verzeichnis, einen Prozess
unter der Job-uid starten, prüfen, dass dieser Prozess keine Capability und
`NoNewPrivs` gesetzt hat, und ihn beenden. Scheitert ein Schritt — etwa weil
`user: "0:0"` oder ein `cap_add` in der Compose-Datei fehlt —, dann

- steht im Log `ANSIBLE-LAB DEAKTIVIERT (fail-closed): <Schritt und Ursache>`,
- endet jeder Ansible-Auftrag mit `rc=2` und der Meldung „Das Ansible-Lab ist
  auf diesem Server deaktiviert …“ (sichtbar im Widget),
- laufen `openssl` und `git` weiter, unter der uid des Workers wie vor der
  Trennung. Begründung: Sie führen keinen frei geschriebenen Code aus, und die
  Argumentprüfung hält sie im Arbeitsverzeichnis — das Risiko, um das es hier
  geht, betrifft sie nicht.

Die Startzeile endet mit `Trennung: uid je Lauf` oder `Trennung: KEINE`.

**Entwicklungsschalter (unsicher):** `RUNNER_ISOLATION=aus-unsicher` lässt
Playbooks ohne Trennung unter der uid des Workers laufen. Gedacht für lokale
Entwicklung ohne root und Container (macOS, Windows) und für die Unit-Tests
(`runner/tests/conftest.py`). Der Wert steht in keiner Compose-Datei und in
keinem Image; ein Worker mit uid 0 verweigert ihn.

### Trennung nachprüfen

Der Test stellt echte Aufträge und lässt ein bösartiges Playbook alles
versuchen, was oben als verhindert steht. Er läuft in der CI bei jedem Push
(Job `runner-isolation`) und von Hand:

```
# Auf einem Rechner mit Docker, im Repository. Eigenes Compose-Projekt mit
# eigenem Volume - ein laufendes System bleibt unberührt. Dauer: wenige Minuten.
bash ops/lab-isolation-test.sh
```

Gegen das **laufende** System (z. B. auf dem Coolify-Server, ohne Repository
im Container — das Skript kommt über die Standardeingabe):

```
docker exec -i <backend-container> python - < runner/tests/isolation_check.py
# nur manche Arten freigegeben oder anderes Zeitlimit:
docker exec -i <backend-container> python - --arten ansible,openssl --zeitgrenze 30 \
  < runner/tests/isolation_check.py
```

Das belegt für etwa eine Minute zwei Läufe und hinterlässt Arbeitsverzeichnisse
`pruefung…`, die nach 12 Stunden verschwinden. Jede Prüfung erscheint als Zeile
`OK …` oder `FEHLER …`; Exit-Code 0 heißt: alles bestanden. Geprüft wird:

- (a) ein normales Playbook läuft unter einer Job-uid, liefert ein Ergebnis mit
  Token, und der zweite Lauf ist idempotent;
- (b) das bösartige Playbook scheitert an `/queue`, an fremden
  Arbeitsverzeichnissen und am Worker (Signal, `environ`, `mem`);
- (c) ein Endlos-Playbook mit `setsid()`-Kindern wird an der Zeitgrenze
  beendet, danach läuft keiner seiner Prozesse mehr;
- (d) Kursvorlagen für `openssl` (darunter die Post-Quanten-Vorlage, die
  OpenSSL ≥ 3.5 braucht) und `git` laufen, `openssl version` ist ≥ 3.5;
- (e) zwei gleichzeitige Läufe haben verschiedene uids und kommen nicht
  aneinander heran;
- (1) ein Lauf hinterlegt Symlinks nach `/queue/in/evil.json` und
  `/etc/passwd`, der nächste schreibt Lab-Dateien gleichen Namens: die Ziele
  bleiben unberührt;
- (2) ein Hardlink auf eine fremde Datei ist abgelehnt oder folgenlos;
- (3) setuid/setgid/sticky sind nach dem Lauf weg, nichts gehört root;
- (4) FIFO und Socket im Arbeitsverzeichnis halten den nächsten Lauf nicht an;
- (5) eine Ausgabeflut mit ANSI-Sequenzen, NUL und ungültigem UTF-8 kommt
  gekürzt und ohne Steuerzeichen an;
- (6) was ein Lauf in `/tmp` und `/dev/shm` ablegt (auch Symlinks nach
  `/queue`), ist danach weg.

`ops/lab-isolation-test.sh` prüft zusätzlich von außen:

- per `docker inspect` und `/proc/mounts`, dass der Container wirklich mit
  `network none`, `read_only`, `cap_drop ALL`, genau fünf Capabilities,
  `no-new-privileges`, Prozessgrenze und beiden `tmpfs` mit
  `noexec,nosuid,nodev` läuft;
- (7) dass `/queue/in` und `/queue/out` nach allen Läufen echte Verzeichnisse
  mit `root:10001`, `0770` sind, und dass ein Start gegen ein präpariertes
  Bestands-Volume (`0777`, `out/` als Symlink, FIFO/Symlink/Verzeichnis als
  „Aufträge“) sauber endet, ohne das Symlink-Ziel umzuhängen;
- (8) fail-closed: derselbe Container ohne root
  (`ops/lab-isolation-failclosed.override.yml`) meldet `ANSIBLE-LAB
  DEAKTIVIERT`, lehnt einen Ansible-Auftrag mit Klartext ab und führt einen
  OpenSSL-Auftrag aus.

Gegen das laufende System laufen nur (a) bis (e) und (1) bis (6).

## Ergebnis-Token (zweite Schicht gegen gefälschte Ergebnisse)

Das Backend legt in jeden Auftrag ein Zufalls-Token (`secrets.token_urlsafe(32)`,
`backend/app/routers/lab.py`). Der Runner liest den Auftrag **beim Beanspruchen**
und löscht die Datei sofort (`_auftrag_lesen` in `runner/worker.py`, aufgerufen
aus `_runde`); danach existiert das Token nur noch im Speicher des Workers. Er
legt es dem Ergebnis bei. Das Backend nimmt `out/<id>.json` nur an, wenn das
Token stimmt und alle Felder vorhanden sind — sonst `502` mit klarer Meldung
statt eines ungeprüft durchgereichten Inhalts.

Das Token stammt aus der Zeit vor der Trennung per uid. Damals ließ es sich
umgehen (Auftrag vor dem Beanspruchen lesen, Speicher des Workers lesen). Mit
der Trennung kommt ein Lauf an beides nicht mehr heran; das Token bleibt als
zweite Schicht für den Fall, dass die Trennung einmal nicht greift, und fängt
weiterhin kaputte oder unvollständige Ergebnisdateien ab (`502` statt `500`).

**Rollout:** Backend und Runner gemeinsam ausrollen. Ein neuer Runner mit altem
Backend funktioniert (kein Token im Auftrag → keines im Ergebnis); ein **neues
Backend mit altem Runner verwirft jedes Ergebnis mit 502**.

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

  Erwartet werden beim Start `Trennung aktiv: Läufe unter uid 10002-10009, ohne
  Capabilities.` und `Lab-Runner bereit. Warteschlange: /queue, … Netzwerk:
  keines, …, Trennung: uid je Lauf`. Steht dort `ANSIBLE-LAB DEAKTIVIERT`, nennt
  dieselbe Zeile die Ursache (siehe „Fail-closed“ oben). Ob die Kette insgesamt
  steht, prüft man am ehrlichsten im Kurs selbst: ein Playbook zweimal ausführen.
- **Isolierung nachprüfen** (nach jedem größeren Plattform-Update sinnvoll):

  ```
  docker inspect <runner-container> --format '{{.HostConfig.NetworkMode}}'
  ```

  Erwartet: `none`. Steht dort etwas anderes, hat die Plattform die Vorgabe
  überschrieben — dann das Lab abschalten, bis das geklärt ist.
- **Rechte von `/queue`:** Der Worker setzt sie bei jedem Start selbst
  (`root:10001`, `0750`/`0770`) — auch auf einem Volume, das eine ältere
  Fassung mit uid 10001 und `0777` angelegt hat. Das Volume muss dafür nicht
  mehr entfernt werden. Gelingt es nicht, meldet der Runner alle fünf Sekunden
  `Warteschlange … lässt sich nicht für Läufe schließen` und nimmt keine
  Aufträge an. Rollout einer bestehenden Installation: `docs/operations.md`,
  „Rollout: Trennung der Lab-Läufe“.
- **`Job-Slot uid … GESPERRT` im Runner-Log:** Prozesse eines Laufs ließen
  sich nicht beenden. Der Slot und das betroffene Arbeitsverzeichnis bleiben
  außer Betrieb, die übrigen sieben arbeiten weiter. Runner-Container neu
  starten; tritt es wieder auf, das Lab abschalten und den Lauf untersuchen.
- **Dauerlast:** `RUNNER_MAX_PARALLEL` senken oder das Lab abschalten. Läufe,
  die regelmäßig in die Zeitgrenze laufen, deuten eher auf zu ambitionierte
  Übungs-Playbooks hin als auf Missbrauch.
- **Speicher:** Das `tmpfs` `/tmp` ist auf 64 MB begrenzt (`/dev/shm`: 16 MB) und nach einem Neustart des
  Containers leer. Arbeitsverzeichnisse sind Übungsstände, kein Speicher.
