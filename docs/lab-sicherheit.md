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
- **`git`** — dasselbe mit `git`. Netzbefehle (`clone`, `fetch`, `push`,
  `pull`) scheitern mangels Netz; das ist beabsichtigt.

**Wichtig für die Bewertung:** Die Arten sind nicht gleich mächtig. `ansible`
erlaubt beliebige Codeausführung, `openssl` und `git` erlauben nur Datei-Ein-
und -Ausgabe über genau ein Programm. Ein Durchlauf, der nur den PKI-Lehrgang
fährt, kann deshalb `openssl` freigeben und `ansible` weglassen — dann ist der
Container **kein** Sandkasten für fremden Code mehr. Das ist strikt weniger
Angriffsfläche als der bisherige Zustand, nicht mehr.

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
- Harte Zeitgrenze je Lauf (`RUNNER_TIMEOUT`, Standard 30 s), Obergrenze für die
  Ausgabemenge, begrenzte Parallelität (`RUNNER_MAX_PARALLEL`, Standard 2).
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
- **Alles, was im Runner-Container liegt.** Ein Playbook kann das Image und die
  Arbeitsverzeichnisse anderer Teilnehmender im selben Container lesen. Dort
  liegen keine Geheimnisse und keine Nutzerdaten — aber es ist keine Trennung
  wie zwischen zwei Maschinen.
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
