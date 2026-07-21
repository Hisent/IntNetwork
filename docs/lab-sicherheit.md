# Sicherheit des Ansible-Labs

Dieses Dokument ist die ehrliche Fassung, kein Beruhigungstext. Wer das Lab
aktiviert, sollte vorher wissen, was es bedeutet, und danach wissen, wie man
es wieder abschaltet.

## Was hier eigentlich passiert

Ein Ansible-Playbook ist ausführbarer Code. Module wie `command`, `shell`
oder `script` gehören zum Kern von Ansible und lassen sich nicht sinnvoll
herausfiltern, ohne das Werkzeug kaputt zu machen. Das heißt konkret: **wer
im Kurs ein Playbook einreichen darf, darf Code im Runner-Container
ausführen.** Das ist keine Lücke, sondern die Grundannahme, unter der dieser
Dienst gebaut wurde — deshalb ist nicht eine Filterliste für Ansible-Module
die Sicherheitsgrenze, sondern der Container selbst.

Wer diese Grundannahme nicht akzeptieren kann, sollte das Lab nicht
aktivieren (siehe unten, "Wann man das Lab besser aus lässt").

## Welche Maßnahmen greifen

- **Eigener Dienst, nicht das Backend.** Der Runner (`runner/`) kennt weder
  `SECRET_KEY` noch die Datenbank noch Teilnehmerdaten. Selbst wer im
  Runner-Container alles lesen kann, kommt an nichts Wertvolles heran, weil
  dort nichts Wertvolles liegt.
- **Kein Weg nach außen.** Der Runner hängt in `docker-compose.yml` an einem
  eigenen Netz mit `internal: true` und hat keinen zweiten Netzwerkanschluss.
  Ein Playbook mit `get_url`, `uri` oder einem `curl` im `shell`-Modul läuft
  ins Leere — es gibt schlicht keine Route ins Internet.
- **Unprivilegiert und eingeschränkt.** Eigener Systembenutzer im Image
  (`runner/Dockerfile`), dazu in Compose `cap_drop: [ALL]`,
  `no-new-privileges:true`, ein nur lesbares Root-Dateisystem sowie
  CPU-, Speicher- und Prozessgrenzen (`pids_limit`).
- **Frisches Arbeitsverzeichnis je Lauf.** Jeder Aufruf bekommt sein eigenes
  Temp-Verzeichnis unter `/tmp` (dem einzigen beschreibbaren Ort im
  Container), das nach dem Lauf wieder gelöscht wird (`runner/app.py`).
  Nichts aus einem Lauf überlebt in den nächsten hinein.
- **Zeitgrenze.** Jeder Lauf bricht nach `RUNNER_TIMEOUT` Sekunden hart ab
  (Default 30s) — ein Playbook mit `pause` oder einer Endlosschleife blockiert
  keinen Slot auf Dauer.
- **Begrenzte Parallelität.** `RUNNER_MAX_PARALLEL` (Default 2) begrenzt, wie
  viele Läufe gleichzeitig aktiv sein können; alles darüber wartet.
- **Rate-Limit im Backend.** `backend/app/routers/lab.py` limitiert
  `/lab/run` pro Teilnehmer (20 Anfragen / 60s), damit niemand den Runner
  im Alleingang flutet.
- **Anmeldepflicht.** Nur angemeldete Teilnehmende (`get_participant`) können
  `/lab/run` überhaupt erreichen — kein anonymer Zugriff.

## Was NICHT abgedeckt ist

- **Ein Ausbruch aus dem Container über eine Kernel-Lücke.** Alle oben
  genannten Maßnahmen laufen innerhalb des Linux-Containermodells. Eine
  Schwachstelle im Kernel selbst (Container-Escape) hebelt das aus. Wer das
  im eigenen Bedrohungsmodell braucht, muss auf eine VM- oder
  gVisor-/Kata-Isolierung wechseln — das leistet dieser Aufbau nicht.
- **Missbrauch der Rechenzeit durch angemeldete Teilnehmende.** Wer sich
  regulär anmelden darf, darf im Rahmen der Grenzen (Timeout, Parallelität,
  Rate-Limit) Rechenzeit verbrauchen. Das ist kein Schutz gegen jemanden, der
  einfach oft und lange im erlaubten Rahmen rechnen lässt — nur gegen
  Fluten/Blockieren über diesen Rahmen hinaus.
- **Alles, was der Runner-Container selbst lesen kann.** Das ist bewusst
  wenig (kein Secret, keine DB), aber eben nicht nichts — Umgebungsvariablen
  des Runner-Prozesses (`RUNNER_TOKEN` selbst!) und was im Image liegt, sind
  für ausgeführten Code im Container sichtbar. Deshalb: keine zusätzlichen
  Geheimnisse in den Runner-Dienst hängen, "nur weil's praktisch wäre".

## Wann man das Lab besser aus lässt

- Der Teilnehmerkreis ist nicht vertrauenswürdig oder nicht namentlich
  bekannt (z. B. ein offener/öffentlicher Kurs ohne Zugangskontrolle).
- Der Host läuft nicht isoliert für diesen Kurs, sondern teilt sich CPU,
  Speicher oder Netz mit anderen, wichtigeren Diensten — die Ressourcengrenzen
  in `docker-compose.yml` schützen den Runner-Container, nicht zwangsläufig
  den ganzen Host bei einem Kernel-Bug.
- Es besteht Unsicherheit darüber, ob "ein Playbook ist ausführbarer Code,
  den Teilnehmende schreiben dürfen" für die eigene Situation akzeptabel ist.
  Im Zweifel: aus lassen.

## Ein- und ausschalten

**Aus (Standard):** `LAB_RUNNER_URL` und/oder `LAB_RUNNER_TOKEN` in der `.env`
leer lassen. Das Backend meldet dann bei `GET /lab/status` `enabled: false`,
`POST /lab/run` antwortet mit `503`, das Widget zeigt einen Hinweis. Der
restliche Kurs läuft unverändert weiter.

**An:** In der `.env` setzen:

```
LAB_RUNNER_URL=http://runner:8080
LAB_RUNNER_TOKEN=<mit `openssl rand -hex 32` erzeugt>
```

Der Wert von `LAB_RUNNER_TOKEN` geht unverändert auch als `RUNNER_TOKEN` an
den Runner-Container (bereits so in `docker-compose.yml` verdrahtet) — beide
Seiten lesen denselben `.env`-Wert, nichts weiter einzutragen. Danach den
Stack neu hochfahren, damit Backend und Runner die neuen Werte einlesen.

**Woran erkennt man, dass es aus ist:** `GET /lab/status` liefert
`{"enabled": false}`, und im Kurs zeigt das Lab-Widget einen Hinweistext statt
der Eingabemaske.

## Betriebshinweise

- **Logs:** Der Runner schreibt wie jeder Compose-Dienst nach stdout/stderr,
  abrufbar mit `docker compose logs runner` (bzw. `docker compose logs -f
  runner` für ein Live-Mitlesen). Es gibt keine separate Logdatei und keine
  Log-Persistenz über einen Volume-Mount hinaus — bei Bedarf extern sammeln
  (z. B. über die Docker-Log-Treiber von Coolify).
- **Bei Dauerlast:** Erst prüfen, ob `RUNNER_MAX_PARALLEL` bereits ausgereizt
  ist (viele Anfragen warten) oder ob einzelne Läufe regelmäßig in
  `RUNNER_TIMEOUT` laufen (dann eher ein Hinweis auf zu ambitionierte
  Playbooks als auf Missbrauch). Hilft nichts: `RUNNER_MAX_PARALLEL`
  vorübergehend senken oder das Lab ganz abschalten (siehe oben).
- **Von Hand prüfen, ob der Runner lebt:** Der Runner ist von außen nicht
  erreichbar (kein `ports:`-Eintrag, eigenes internes Netz) — ein `curl` vom
  Host aus läuft ins Leere. Stattdessen aus dem Backend-Container heraus
  prüfen, das im selben internen Netz hängt:

  ```
  docker compose exec backend python -c "import urllib.request;print(urllib.request.urlopen('http://runner:8080/health',timeout=5).read().decode())"
  ```

  (Kein `curl` in den Beispielen: beide Images sind `-slim`-Varianten und
  bringen keines mit — derselbe Grund, aus dem der Healthcheck des Backends
  seinerzeit auf einen urllib-Einzeiler umgestellt wurde.)

  Erwartete Antwort: `{"status":"ok","ansible":true}`. Kommt keine Antwort,
  prüft `docker compose ps runner` den Container-Status und `docker compose
  logs runner` die Fehlermeldung.
