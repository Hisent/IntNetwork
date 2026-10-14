Stand: v1.43.0 + Trennung der Lab-Läufe per uid, Admin-Rolle, Aufbewahrung, Fehler-IDs (2026-10-14) · Quelle: docs/operations.md, README.md, .env.example, docker-compose.yml, docs/lab-sicherheit.md, backend/app/database.py, backend/app/utils.py, backend/app/content/changelog.py, backend/app/routers/trainer_accounts.py, backend/app/services/retention.py, backend/app/main.py

# IntLab: Betrieb

## Deployment

Das Projekt wird mit Docker Compose betrieben (`docker-compose.yml`). Der Zielbetrieb läuft auf Coolify mit Traefik als Ingress.

| Dienst | Image/Build | Zweck |
|---|---|---|
| `db` | `postgres:16-alpine` | Datenbank; einziger Dienst mit Compose-Healthcheck |
| `backend` | `backend/Dockerfile` (`python:3.11-slim-trixie`, Benutzer uid 10001) | FastAPI, führt Migrationen und Content-Sync beim Start aus; Port 8000 intern |
| `frontend` | `frontend/Dockerfile` | nginx mit der gebauten Oberfläche; reicht `/api/` an `backend:8000` weiter |
| `runner` | `runner/Dockerfile` (`python:3.12-slim-trixie`; Worker uid 0 mit fünf Capabilities, Läufe unter uid 10002 bis 10009) | Lab-Ausführung ohne Netzwerk (`network_mode: "none"`) |

Volumes: `postgres_data` (Datenbank) und `lab_queue` (Austausch Backend und Runner).

Lokaler Start:

```bash
cp .env.example .env   # danach SECRET_KEY, POSTGRES_PASSWORD, ADMIN_PASSWORD ersetzen
docker compose up --build
```

Frontend lokal: `http://localhost:5173`, API: `http://localhost:8000`.

### Nach jedem Deploy

1. `GET /api/health` muss erfolgreich antworten.
2. Trainer-Login, Kursbeitritt und ein Quiz einmal im Browser prüfen.
3. Falls das Lab aktiv ist: einen harmlosen Lauf zweimal ausführen und im Runner prüfen, dass `NetworkMode` weiterhin `none` ist und das Log `Trennung aktiv` zeigt.
4. Die CI muss grün sein. `pip-audit` und `npm audit --omit=dev` sind bewusst blockierend; ein Advisory wird vor dem Deploy bewertet und nicht übergangen.

## Konfiguration und Secrets

Konfiguration erfolgt über Umgebungsvariablen (Vorlage: `.env.example`).

| Variable | Bedeutung |
|---|---|
| `POSTGRES_PASSWORD` | Datenbankpasswort; nur URL-sichere Zeichen, da es unkodiert in `DATABASE_URL` steht |
| `SECRET_KEY` | JWT-Schlüssel; erzeugen mit `openssl rand -hex 32`. Leer oder `change-me`-Platzhalter: Backend startet nicht |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Erstes Trainer-Konto. Ein `change-me`-Passwort verhindert den Erststart |
| `ALLOWED_ORIGINS` | Erlaubte Frontend-Origins (CORS), kommasepariert; nur nötig, wenn Frontend und Backend unter verschiedenen Origins laufen |
| `LAB_QUEUE_DIR` | Pfad der gemeinsamen Warteschlange (`/queue`); leer schaltet das Lab ab (API antwortet `503`) |
| `LAB_KINDS` (Backend), `RUNNER_KINDS` (Runner) | Freigegebene Lab-Arten (`ansible`, `openssl`, `git`; Standard `ansible`). Werden nicht automatisch abgeglichen |
| `RUNNER_TIMEOUT`, `RUNNER_MAX_PARALLEL`, `RUNNER_MAX_QUEUE_DEPTH`, `RUNNER_MAX_OUTPUT` | Runner-Grenzen (Vorlage: 30 s, 2, 4, 65536); passend zu den Container-Limits wählen |
| `WEBAUTHN_RP_ID`, `WEBAUTHN_ORIGIN` | Passkey-Anmeldung für Trainer; beide setzen oder beide leer lassen |
| `COURSE_RETENTION_DAYS` | Aufbewahrung von Teilnehmerdaten in Tagen ohne Aktivität (siehe „Aufbewahrung von Teilnehmerdaten“); `0` oder leer = aus (Standard) |

Passkey-Werte:

```text
WEBAUTHN_RP_ID=lab.example.de           # nur die Domain, ohne Schema, Port und Pfad
WEBAUTHN_ORIGIN=https://lab.example.de  # vollständiger Ursprung, ohne abschließenden Schrägstrich
```

Beide müssen der von außen sichtbaren Adresse entsprechen (hinter Traefik der öffentliche Hostname, nicht der Containername). WebAuthn braucht HTTPS (außer `localhost`) und einen Domainnamen, keine reine IP-Adresse. Fehlt ein Wert, ist die Funktion aus und der Anmeldeknopf erscheint nicht.

## Datenbank-Migrationen

- Das Schema wird mit Alembic verwaltet (`backend/migrations/`). Ausstehende Migrationen laufen beim App-Start automatisch auf `head`.
- Bestandsdatenbanken aus der Zeit vor Alembic werden einmalig auf die Baseline gestampt und danach nur mit den Folge-Revisionen nachgezogen.
- Revision nach einer Modelländerung erzeugen und prüfen:

```bash
cd backend
python -m alembic revision --autogenerate -m "beschreibung"
python -m alembic upgrade head
```

- `Base.metadata.create_all()` läuft seit v1.36 nicht mehr beim Start; Alembic ist allein für das Schema zuständig.
- Jede Migration, die per `create_table` eine Tabelle anlegt, braucht einen Guard gegen bereits vorhandene Tabellen. Ohne Guard gab es den Crashloop v1.34.0 („relation already exists“, Neustart, Wiederholung). Dasselbe gilt für `add_column` und Constraints.

```python
def upgrade() -> None:
    if sa.inspect(op.get_bind()).has_table("neue_tabelle"):
        return

    op.create_table("neue_tabelle", ...)
```

- Fehlt der Datenbank trotzdem eine Spalte, die ein Modell erwartet, bricht der Start vor dem Seeding mit einer benannten „Schema-Drift“-Meldung ab.
- Inhaltliche Änderungen an ausgelieferten Modulen laufen getrennt vom Schema über den Content-Sync (siehe unten).

## Content-Sync: geänderte Kursinhalte nach einem Deploy

Kursinhalte liegen im Code (`backend/app/content/*.py`), ausgeliefert wird aus der Datenbank. Beim Start gleicht `seed_missing_content()` beides ab (`backend/app/content/sync.py`). Jedes mitgelieferte Modul, das kein Trainer verändert hat, wird auf den Stand der Quelle gebracht: Texte, Blöcke, Quizfragen samt Erklärungen, Titel, Lernziele (Deutsch und englisch in `content_module.goals_en`, seit Migration `b7c8d9e0f1a2`), Reihenfolge und Voraussetzungen. Ein Modul ohne `goals_en` behält seinen bisherigen Hash und gilt weiter als unverändert; kommt `goals_en` mit einem Release dazu, wird es wie jede andere Inhaltsänderung eingespielt. Ein zweiter Start ändert nichts mehr.

Zugeordnet wird über Kennungen: Jeder Block und jede Frage trägt eine je Modul eindeutige `id` (Spalte `uid` in `content_block` und `content_quiz_question`, seit v1.43.0).

| Änderung in der Quelle | Wirkung in der Datenbank |
|---|---|
| bekannte Kennung | Zeile wird überschrieben und behält ihre Datenbank-id; Quiz-Abgaben, Fragenstatistik und Kommentare bleiben dran |
| neue Kennung | Block bzw. Frage wird an der Stelle der Quelle eingefügt |
| Kennung entfällt | Zeile wird gelöscht; Kommentare am entfallenen Block hängen danach am nächsten verbliebenen Block davor |
| Reihenfolge | wie in der Quelle; Kommentare wandern mit ihrem Block |

Quiz-Ergebnisse:

- Es wird nichts rückwirkend neu bewertet. `quiz_result` speichert Punktzahl und Gesamtzahl zum Zeitpunkt der Abgabe; „bestanden“, Fortschritt, Bestwert und Zertifikate bleiben unverändert.
- Neue Fragen zählen ab der nächsten Abgabe. In der Fragenstatistik zählt je Frage nur als Versuch, wer sie in seiner Abgabe hatte.
- Wer das Quiz vor dem Deploy geladen hat und danach abgibt, bekommt die neuen Fragen als nicht beantwortet gewertet. Abhilfe: Seite neu laden und wiederholen.
- Ändern sich Lösung oder Optionsreihenfolge einer bestehenden Frage, startet deren Statistik neu (Abschnitt „Geänderter Lösungsschlüssel“ unten). Punktzahl, „bestanden“ und Teilnahmebestätigungen bleiben unberührt.

### Geänderter Lösungsschlüssel unter gleicher Kennung

Das gilt für Sync, Speichern im Editor, „Auslieferungszustand laden“ und Wiederherstellen. Eine Fragezeile wird nur wiederverwendet, wenn Fragetyp und Lösung gleich sind und kein weiter vorhandener Optionstext (deutsch oder englisch) an einer anderen Position steht.

| Änderung an einer Frage | Wirkung |
|---|---|
| Textkorrektur an Frage, Erklärung oder Optionswortlaut; hinten angefügte oder gestrichene Option | Zeile bleibt, die Statistik bleibt |
| Lösung geändert, Fragetyp geändert, Optionen umsortiert oder vorn bzw. mittig eingefügt | neue Zeile mit neuer Datenbank-id, die alte entfällt |

Bei einer neuen Zeile zählen alte Abgaben (gespeichert ist nur der gewählte Index) für diese Frage weder in der Fragenstatistik noch in „Üben: zuletzt falsch“. Nicht erkennbar ist ein Umsortieren, bei dem zugleich alle Optionen umformuliert werden; dafür vergeben Autoren eine neue Kennung (Seite „Inhalte pflegen“).

### Gleichzeitiges Speichern

Die Prüfung „unverändert“ sperrt die Modulzeilen (Postgres, `FOR NO KEY UPDATE`) bis zum Commit des Syncs; dieselbe Sperre nimmt der Editor beim Speichern.

- Ein Trainer, der während des Starts speichert, wartet kurz und bekommt `409`, falls der Sync sein Modul geändert hat.
- Speichert er über einen noch laufenden alten Container (Rolling-Deploy, kennt die Sperre nicht), liest der Sync vor dem Einspielen frisch und lässt das Modul als „vom Trainer geändert“ aus.
- Ausgenommen sind Module, die eine Seed-Migration desselben Starts selbst angefasst hat.

Datenbanken bis v1.42.0 haben noch keine Kennungen. Beim ersten Start mit v1.43.0 legt die Migration `a6b7c8d9e0f1` die Spalten an, und der Sync trägt die Kennungen einmalig ein, für jedes Modul, auch für vom Trainer geänderte. Dazu dient der Stand v1.42.0 (`"structure"` in `backend/app/content/sync_baseline.json`); Widgets werden über ihre Widget-id zugeordnet, andere Blöcke als n-ter Block ihres Typs, Fragen über ihre Position. Was nicht passt (eigene Blöcke, Fragen, Module), bekommt eine zufällige Kennung (`x…`).

Wann ein Modul als „unverändert“ gilt:

- Sein Stand entspricht dem beim letzten Sync gespeicherten Hash (Tabelle `setting`, Schlüssel `content-sync:<modul>`).
- Datenbanken aus der Zeit vor dem Sync haben diesen Hash nicht. Dort gilt ein Modul als unverändert, wenn es nie im Editor gespeichert wurde (kein Eintrag in `content_module_snapshot`) oder sein Stand ein bekannter Auslieferungsstand bis v1.42.0 ist (`backend/app/content/sync_baseline.json`, erzeugt von `backend/build_content_baseline.py`).

Log-Meldungen nach einem Deploy (Logger `app.content.sync`, Stufe WARNING):

| Meldung | Bedeutung |
|---|---|
| `Content-Sync: N Module auf Auslieferungsstand aktualisiert: …` | einmal je Release; dazu Eintrag `content.sync` im Audit-Log (Benutzer `system`) |
| `Content-Sync: N Module weichen vom Auslieferungsstand ab und bleiben unangetastet: <modul> (<Grund>); …` | bei jedem Start, solange es zutrifft; kommt neuer Inhalt für ein solches Modul, entsteht einmalig `content.sync.skipped` im Audit-Log |
| `Content-Sync: Modul <modul> konnte nicht aktualisiert werden` (mit Traceback) | nur dieses Modul bleibt auf dem alten Stand, der Start läuft weiter; bitte melden |

Vom Trainer geänderte Module sind der einzige Grund, ein Modul auszulassen; der Trainer-Stand hat Vorrang. Wer die neuen Inhalte will, nutzt im Modul-Editor „Auslieferungszustand laden“ und pflegt eigene Änderungen danach wieder ein. Die vorherige Fassung liegt eine Stufe tief unter „Vorherige Version wiederherstellen“. Seit v1.43.0 arbeiten Speichern, „Auslieferungszustand laden“ und Wiederherstellen ebenfalls über die Kennungen: Bestehende Fragen und Blöcke behalten ihre Zeile, laufende Abgaben und die Fragenstatistik bleiben gültig. Nur an einem dabei entfernten Block gehen die Kommentare verloren. Ist das Modul wieder auf Auslieferungsstand, nimmt es ab dem nächsten Start wieder am Sync teil.

Deaktiviert ein Trainer ein Modul in einem Kurs, bleibt das auch über Neustarts so (Tabelle `module_disabled`); nur wirklich neue Module rücken automatisch in bestehende Kurse nach. Trainer-eigene Module bleiben Opt-in.

Entwicklungsreset der nichtproduktiven lokalen Datenbank (löscht Kurse, Teilnehmer, Fortschritte und Trainerdaten der konfigurierten SQLite-Datenbank und seedet neu):

```bash
cd backend
python reset_dev_db.py --yes
```

## Modul-Editor: Speichern, Sperre, Kennungen

- **`base_version` ist Pflicht.** `PUT /api/trainer/content/modules/{key}?base_version=…` erwartet als Wert die `version` aus dem GET. Fehlt sie oder ist sie veraltet, antwortet die API mit `409` und speichert nichts. Hintergrund: Ein Editor-Tab von vor einem Update kennt neuere Felder (Erklärungen, `goals_en`) nicht und hätte sie beim Speichern still gelöscht.
- **Rollout:** Trainer mit offenem Editor müssen nach dem Deploy die Seite neu laden. Eigene Skripte gegen diese API senden erst GET, dann PUT mit `base_version`.
- **Atomar:** Speichern, „Auslieferungszustand laden“ und Wiederherstellen sperren unter Postgres die Modulzeile (`SELECT … FOR NO KEY UPDATE`). Zwei gleichzeitige PUTs laufen nacheinander; der zweite scheitert an `base_version` (`409`). Unter SQLite (nur Entwicklung und Tests) gibt es die Zeilensperre nicht.
- **Kein Unique-Index auf `(module_key, uid)` (bewusst, Plan).** Die Eindeutigkeit der Kennungen stellt der Code sicher (`_write_rows` vergibt bei doppelt gelieferter Kennung eine neue). Ein Index per Migration könnte an Bestandsdaten scheitern und den Start blockieren. Falls gewünscht: zuerst die folgende Abfrage ausführen (ebenso für `content_quiz_question`). Die Migration legt den Index nur an, wenn beide Abfragen leer sind, und warnt sonst im Log, statt zu scheitern.

```sql
SELECT module_key, uid, count(*) FROM content_block WHERE uid IS NOT NULL GROUP BY 1, 2 HAVING count(*) > 1;
```

- Leere optionale Textfelder (`note`, `value_de`/`value_en`, `widget_id`, Erklärungen, `goals_en`) werden als „nicht gesetzt“ gespeichert. Ein unverändertes Speichern macht ein Modul nicht zu einem Trainer-Stand.

## Zeitstempel der API

Alle Zeitfelder (`created_at`, `issued_at`, `last_used_at`) kommen als ISO 8601 in UTC mit Offset, zum Beispiel `2026-10-13T11:50:00.123456+00:00` (`iso_utc` in `backend/app/utils.py`).

- Die Datenbankspalten bleiben zeitzonenlos und enthalten UTC.
- Damit das nicht von der Zeitzone des Postgres-Servers abhängt, setzt das Backend für seine Sitzungen `timezone=UTC` (Verbindungsoption in `backend/app/database.py`, nur für Postgres).
- Grund: Postgres rechnet einen Wert mit Zone beim Schreiben in die Sitzungs-Zeitzone um. Stünde der Server auf `Europe/Berlin`, landete Ortszeit in der Spalte, und die API gäbe sie als UTC aus.
- Vor dem Deploy prüfen: `SHOW timezone;`. Stand der Server bisher nicht auf UTC, enthalten Bestandszeilen Ortszeit und werden um den Versatz falsch angezeigt. Neue Zeilen stimmen.

## Bekannte Eigenschaften (bewusst so)

- **Üben ist ein Lösungs-Orakel für bereits abgegebene Module.** `POST /api/practice/check` sagt je Frage richtig oder falsch und liefert die Erklärung, wie das Quiz nach jeder Abgabe; das Quiz ist beliebig wiederholbar. Wer ein Modul einmal abgegeben hat, kann sich die Lösungen also erarbeiten. Das ist konstruktionsbedingt (Lernplattform, keine Prüfung). Mögliche Abhilfe, falls das Zertifikat härter werden soll: Üben erst für bestandene Module öffnen (`_last_answers` in `backend/app/routers/learning.py`).
- **Die Reihenfolge-Sperre der Module ist nur Anzeige.** Voraussetzungen (`prerequisites`) graut Module im Frontend aus; die API liefert jedes im Kurs freigeschaltete Modul auch ohne erfüllte Voraussetzung aus. Das ist didaktische Führung, keine Zugriffskontrolle; die Zugriffskontrolle ist die Freischaltung je Kurs.
- **Namen im Kurs sind beim Beitritt erkennbar.** Der Beitritt unter einem vergebenen Namen verlangt den Wiederaufnahme-Code; daran lässt sich mit dem Kurscode ablesen, ob ein Name im Kurs existiert. Der Kurscode ist das Geheimnis des Kurses; ein Rate-Limit je IP begrenzt das Durchprobieren.
- **Abgewähltes Modul.** `GET /api/modules/{key}`, `/heartbeat` und `/quiz` antworten mit `404` und einem Feld `code` neben `detail`: `module_not_enabled` (im Kurs abgewählt) bzw. `module_unknown`. Die Oberfläche zeigt je nach `code` eine eigene Meldung.

## Alembic-Downgrade

Der Downgrade von `b7c8d9e0f1a2` (entfernt `goals_en`) und `a6b7c8d9e0f1` (entfernt Kennungen und Erklärungen) löscht die gespeicherten Sync-Hashes (`setting`, Schlüssel `content-sync:*`). Ohne das gälte nach einem erneuten Upgrade jedes Modul dauerhaft als „vom Trainer geändert“.

Folge: Nach Downgrade und Upgrade greift die Bootstrap-Regel des Syncs (nie im Editor gespeichert oder bekannter Stand bis v1.42.0 gilt als unverändert). Module, die je im Editor gespeichert wurden, bleiben vorsichtshalber Trainer-Stand; „Auslieferungszustand laden“ holt sie zurück.

## Backup und Restore

`ops/backup.sh` zieht per `docker compose exec` einen `pg_dump` aus dem laufenden `db`-Container, komprimiert ihn mit gzip und legt ihn im Zielverzeichnis ab (Standard `./backups`). Dumps älter als 14 Tage werden dabei gelöscht. Täglicher Cron-Lauf:

```bash
0 3 * * * cd /opt/intnetwork && ops/backup.sh /var/backups/intnetwork >> /var/log/intnetwork-backup.log 2>&1
```

Zurückspielen:

```bash
docker compose stop backend
ops/restore.sh pfad/zum/dump.sql.gz
docker compose start backend
```

- Das Skript fragt vor dem Überschreiben ausdrücklich nach Bestätigung.
- Es ersetzt das Schema `public` in einer Transaktion durch den Dump. Schlägt das Einspielen fehl, bleibt der alte Stand erhalten.
- Mindestens vierteljährlich einen aktuellen Dump in eine isolierte Testdatenbank wiederherstellen und dort Login, Kursdaten, Fortschritt und Kommentare prüfen. Ein Backup ohne erfolgreichen Restore-Test gilt nicht als verifiziert.

## Monitoring

Ein externer Monitor soll mindestens `/api/health` im Minutenintervall aufrufen und bei zwei aufeinanderfolgenden Fehlschlägen alarmieren. Die Einrichtung erfolgt in der Hosting-Plattform; das Repository kann keinen externen Alarmkanal konfigurieren.

### Wo Fehler auftauchen

Es gibt keinen externen Fehlerdienst. Alles landet im Log des Backend-Containers (`docker compose logs backend`, in Coolify: Logs des Backend-Dienstes).

| Quelle | Logzeile | Was der Nutzer sieht |
|---|---|---|
| Unbehandelter Fehler im Backend | `ERROR [app.main] Unbehandelter Fehler request_id=<id> GET /api/...` und Traceback | HTTP 500 mit „Interner Fehler (Fehler-ID <id>)“ |
| Fehler im Browser (Render-Fehler, Skriptfehler, unbehandelte Promise) | `WARNING [app.routers.client_errors] Client-Fehler version=… route=… message=… stack=…` | den bisherigen Fehlerhinweis der Oberfläche |

- Jede Antwort trägt den Header `X-Request-ID`.
- Meldet ein Trainer eine Fehler-ID, findet man den Traceback so:

```bash
docker compose logs backend | grep <fehler-id>
```

- Browser-Berichte (`POST /api/client-errors`, ohne Anmeldung) enthalten nur Meldung, Stack (höchstens 4000 Zeichen), Pfad ohne Query und App-Version. Keine Namen, Tokens oder Request-Inhalte.
- Grenzen: 10 Berichte je IP und Minute, 5 je Seitenaufruf; zu lange Felder lehnt der Server mit 422 ab. Gespeichert wird nur die Logzeile.
- Nach jedem Deploy einmal im Backend-Log nach `Unbehandelter Fehler` und `Client-Fehler` suchen.

## Rollen: Admin und Trainer

Seit Migration `3f9a1c7e2b40` hat jeder Trainer-Zugang eine Rolle (Spalte `trainer.role`).

| Aktion | Trainer | Admin |
|---|---|---|
| Kurse, Teilnehmer, Module, Inhalte, Abstimmungen, Protokoll lesen | ja | ja |
| Trainer-Zugänge anlegen und löschen | nein | ja |
| Rollen ändern | nein | ja |
| Globale Einstellungen (Feedback-Kommentare an/aus) | nein | ja |

- Beim Upgrade wird der älteste Trainer (niedrigste `id`, in der Regel der über `ADMIN_EMAIL` angelegte) Admin; alle anderen bleiben Trainer.
- Auf einer leeren Datenbank ist der über `ADMIN_EMAIL` und `ADMIN_PASSWORD` angelegte erste Trainer Admin. Neu angelegte Zugänge sind immer Trainer.
- Schutz vor Aussperren: Der letzte Admin kann weder gelöscht noch herabgestuft werden. Niemand kann den eigenen Zugang löschen.
- Die Rolle wird bei jedem Request aus der Datenbank gelesen; ein Rollenwechsel wirkt sofort, ohne Neuanmeldung.
- Rollenwechsel stehen im Protokoll als `trainer.role_change`.

Trainer zum Admin machen: Als Admin unter „Verwaltung“, Bereich „Trainer-Zugänge“, die Auswahl neben dem Namen auf „Admin“ stellen.

Notfall (kein Admin erreichbar):

```bash
docker compose exec db psql -U intnetwork -d intnetwork \
  -c "UPDATE trainer SET role = 'admin' WHERE email = 'person@firma.de';"
```

## Aufbewahrung von Teilnehmerdaten (DSGVO)

Opt-in über `COURSE_RETENTION_DAYS` (Standard `0` = aus). Ist ein Wert gesetzt, löscht das Backend beim Start und danach alle 24 Stunden die Teilnehmerdaten aller Kurse, in denen seit so vielen Tagen kein Teilnehmer mehr aktiv war.

| Aspekt | Verhalten |
|---|---|
| Aktivität | jüngster Zeitpunkt aus Beitritt, geöffnetem Modul, abgeschlossenem Modul, Quiz-Abgabe und Teilnehmer-Kommentar |
| Gelöscht | Teilnehmer, Fortschritt, Quiz-Ergebnisse, Teilnehmer-Kommentare, Abstimmungs-Stimmen |
| Bleibt | Kurs, Kurs-Code, Modulauswahl, Trainer-Kommentare, Inhalte, ausgestellte Teilnahmebestätigungen |
| Protokoll | nur Zahlen, keine Namen: Logzeile `Aufbewahrung (N Tage): gelöscht …` und Audit-Eintrag `retention.purge` (Benutzer `system:retention`) |
| Mehrere Worker, Neustarts | unkritisch: jeder Lauf ist ein DELETE in einer Transaktion; ein zweiter Lauf findet nichts mehr. Ein Neustart zählt als Lauf. |

- Ein Kurs mit einem einzigen noch aktiven Teilnehmer bleibt vollständig erhalten.
- Teilnahmebestätigungen bleiben wie beim Kurs-Löschen bewusst stehen (unveränderlicher Nachweis). Wer sie entfernen will, löscht den Kurs mit „Teilnahmebestätigungen mitlöschen“.
- Die Einstellung wirkt beim ersten Start sofort auf alle Altkurse. Vorher ein Backup ziehen (`ops/backup.sh`).

Beispiel in `.env`:

```text
COURSE_RETENTION_DAYS=180
```

## Live-Abstimmung und Polling-Last

- Zwei Tabellen (Migration `c8d9e0f1a2b3`): `live_poll` (je Kurs höchstens eine nicht geschlossene Zeile) und `live_poll_vote` (eine Zeile je Teilnehmer und Abstimmung).
- Abstimmungsarten (Migration `9f3e7a1c5b2d`): `live_poll.kind` (`single`, `multi`, `scale`, `text`, `words`; Bestand wird `single`) und `live_poll.config` (Frage und Einstellungen eigener Abstimmungen); `live_poll_vote.value` (Antwort der neuen Arten) und `live_poll_vote.hidden` (vom Trainer ausgeblendeter Freitext); `live_poll_vote.choice` ist nur noch bei `single` gefüllt. Der Downgrade löscht Abstimmungen der neuen Arten samt Antworten; Single-Choice-Abstimmungen bleiben.
- Grenzen an der API: Freitext höchstens 280 Zeichen, Wortwolke 1 bis 3 Wörter zu je höchstens 30 Zeichen, eigene Frage höchstens 300 Zeichen, Mehrfachauswahl 2 bis 10 Antworten. Antworten laufen über denselben Endpunkt wie Stimmen (Rate-Limit 240 je Minute und IP); je Teilnehmer und Abstimmung bleibt es bei einer Zeile.
- Beide hängen per `ON DELETE CASCADE` am Kurs bzw. Teilnehmer; ein Aufräumjob ist nicht nötig. Der Zustand liegt ausschließlich in der Datenbank, mehrere Worker sind unkritisch.
- Last: Jeder Teilnehmer mit offenem, sichtbarem Modul fragt alle 5 s `GET /api/modules/{key}/poll` ab. 20 Teilnehmer entsprechen etwa 4 Anfragen pro Sekunde (je eine Handvoll kleiner Lesezugriffe). Im Hintergrund-Tab ruht die Abfrage.
- Der Beamer lädt nur während einer laufenden Abstimmung alle 2 s nach.
- Bleibt eine Abstimmung offen (Browser geschlossen), beendet sie der Trainer im Kurs-Detail („Abstimmung beenden“) oder im Beamer-Modus desselben Kurses, oder die nächste Abstimmung schließt sie.

## Lab: Betrieb

Das Lab ist standardmäßig aus. Vor dem Einschalten die Seite „Lab-Sicherheit“ lesen.

- Einschalten: `LAB_QUEUE_DIR=/queue` beim Backend, dazu `LAB_KINDS` (Backend) und `RUNNER_KINDS` (Runner) mit denselben Werten.
- Ausschalten: `LAB_QUEUE_DIR` leeren und neu ausrollen. Die API antwortet dann mit `503`, das Widget zeigt einen Hinweis.
- Status: Als angemeldeter Teilnehmer `GET /api/lab/status`; Antwort `{"enabled": false}`, wenn aus.
- Runner prüfen: `docker logs --tail 5 <runner-container>`; erwartet werden beim Start `Trennung aktiv: Läufe unter uid 10002-10009, ohne Capabilities.` und `Lab-Runner bereit. Warteschlange: /queue, … Netzwerk: keines, …, Trennung: uid je Lauf`. Einen Health-Endpunkt gibt es nicht.
- Isolierung prüfen: `docker inspect <runner-container> --format '{{.HostConfig.NetworkMode}}'` muss `none` liefern. Sonst das Lab abschalten, bis das geklärt ist.
- Rechte von `/queue`: Der Worker setzt sie bei jedem Start selbst (`root:10001`, `0750`/`0770`). Ein Volume aus einer älteren Fassung muss nicht mehr entfernt werden (siehe „Rollout: Trennung der Lab-Läufe“).
- Dauerlast: `RUNNER_MAX_PARALLEL` senken oder das Lab abschalten.
- OpenSSL im Runner: Basis ist Debian 13 (trixie) mit OpenSSL 3.5 (LTS). Mindestversion 3.5, weil die Vorlage „Post-Quanten-Schlüssel“ ML-KEM-768 und ML-DSA-65 erzeugt. Nach einem Wechsel des Debian-Release prüfen: `docker exec <runner-container> openssl version`.

### Rollout: Trennung der Lab-Läufe

Seit dem 13.10.2026 läuft der Lab-Worker als uid 0 mit fünf Capabilities und startet jeden Lauf unter einer eigenen uid (10002 bis 10009). Hintergrund und Restrisiken: Seite „Lab-Sicherheit“, Abschnitt „Trennung der Läufe per uid“.

Was sich ändert:

- `docker-compose.yml`, Dienst `runner`: neu `user: "0:0"` und `cap_add` (`SETUID`, `SETGID`, `CHOWN`, `DAC_OVERRIDE`, `KILL`); das `tmpfs` `/tmp` bekommt zusätzlich `nosuid,nodev`, `/dev/shm` ist jetzt ausdrücklich ein `tmpfs` mit 16 MB und `noexec,nosuid,nodev`. Alles andere bleibt (`network_mode: none`, `cap_drop: ALL`, `no-new-privileges`, `read_only`, Limits). Wer den Dienst in Coolify von Hand überschrieben hat, muss dort nachziehen.
- Runner-Image: Benutzer `labjob10002` bis `labjob10009`, `/queue` gehört `root:10001`. Backend-Image und Backend-Konfiguration bleiben unverändert. Neue Umgebungsvariablen braucht es nicht.

Schritte:

1. Backend und Runner gemeinsam ausrollen (Image und Compose-Datei aus demselben Stand).
2. Runner-Log prüfen: `docker logs --tail 20 <runner-container>` muss `Trennung aktiv: Läufe unter uid 10002-10009, ohne Capabilities.` und `Lab-Runner bereit … Trennung: uid je Lauf` zeigen.
3. Im Kurs ein Playbook zweimal ausführen, je einmal `openssl` und `git`, falls freigegeben.
4. Empfohlen, einmal je Installation und nach Plattform-Updates: den Trennungstest gegen das laufende System fahren (belegt für etwa eine Minute zwei Läufe):

```text
docker exec -i <backend-container> python - < runner/tests/isolation_check.py
```

Das vorhandene Volume `lab_queue`: Ein Volume aus einer älteren Fassung gehört uid 10001 mit Modus `0777`. Es muss nicht entfernt werden. Der Worker setzt beim ersten Start `/queue` auf `root:10001`, `0750` und `in/`, `out/` auf `0770`. Das darf nur er (einziger Prozess mit `CAP_CHOWN` auf diesem Volume); das Backend ändert dort keine Rechte. Liegengebliebene Dateien werden normal behandelt: reguläre Aufträge in `in/` führt der neue Worker aus, Ergebnisse in `out/` holt das Backend ab oder der Worker löscht sie nach fünf Minuten. Was in `in/` keine reguläre Datei ist (Symlink, FIFO, Verzeichnis), weist er mit `Auftrag unlesbar: …` ab und entfernt es. Ist `in/` oder `out/` selbst ein Symlink, ersetzt er ihn durch ein echtes Verzeichnis und folgt ihm nicht. Gelingt die Korrektur nicht, meldet der Runner alle fünf Sekunden `Warteschlange … lässt sich nicht für Läufe schließen` und nimmt keine Aufträge an; dann das Volume einmal entfernen (`docker volume rm <projekt>_lab_queue`) und neu ausrollen.

| Log-Zeile im Runner | Ursache | Behebung |
|---|---|---|
| `ANSIBLE-LAB DEAKTIVIERT (fail-closed): Der Worker läuft als uid 10001 statt 0` | neues Image, aber alte Compose-Datei (kein `user: "0:0"`) | Compose-Datei aus dem Repository ausrollen |
| `ANSIBLE-LAB DEAKTIVIERT (fail-closed): … (CAP_…) fehlgeschlagen` | die genannte Capability fehlt in `cap_add` | `cap_add` wie im Repository |
| `ANSIBLE-LAB DEAKTIVIERT … fehlt security_opt no-new-privileges?` | `no-new-privileges` wurde entfernt | wieder eintragen |
| `Job-Slot uid … GESPERRT` | Prozesse eines Laufs ließen sich nicht beenden | Runner-Container neu starten |
| `WARNUNG: fs.protected_hardlinks=0` (oder `protected_symlinks`) | Kernel-Schalter des Hosts ist aus | auf dem Host auf 1 setzen und dauerhaft eintragen; das Lab läuft auch ohne weiter |
| `… nicht übergebbar (…) - entfernt` | ein Lauf hat etwas hinterlassen, das der Worker nicht übernehmen kann (typisch: Datei mit setuid-Bit) | nichts zu tun |
| `Arbeitsverzeichnis … wird verworfen, der nächste Lauf beginnt leer` | das Arbeitsverzeichnis ließ sich nach einem Lauf nicht zurücknehmen | nichts zu tun; der Übungsstand dieser Person ist weg |
| `… Einträge entfernt (Spezialdatei oder mehrfach verlinkt)` | ein Lauf hat FIFOs, Sockets oder Hardlinks im Arbeitsverzeichnis hinterlassen | nichts zu tun |

In allen `DEAKTIVIERT`-Fällen läuft der Runner weiter: Ansible-Aufträge enden mit einer klaren Meldung im Widget, `openssl` und `git` funktionieren. Es läuft nie still ein Playbook ohne Trennung.

Zurückrollen: vorherigen Stand von Image und Compose-Datei ausrollen. Der alte Worker (uid 10001) kann in das inzwischen `root` gehörende `/queue` weiter schreiben, weil uid 10001 der Gruppe 10001 angehört.

Lokale Entwicklung ohne Docker: `RUNNER_ISOLATION=aus-unsicher` schaltet die Trennung ab. Nie auf einem Server setzen; ein Worker mit uid 0 verweigert den Wert.

## Bekannte Fallstricke und Vorfälle

- **Kein Healthcheck für backend und frontend (bewusst).** Nur `db` hat einen Compose-Healthcheck. Coolify routet per Traefik nur auf Container im Zustand „healthy“; ein Check, der in dieser Umgebung anders ausfällt als lokal gedacht, nimmt den Dienst vom Netz („no available server“, Vorfall 2026-07-21). `docker-compose.yml` sagt deshalb ausdrücklich: keinen Healthcheck eintragen; falls doch gewünscht, erst in Coolify gegen einen Test-Deploy verifizieren. Das externe Monitoring auf `/api/health` ist die einzige externe Absicherung; nicht auf Traefiks Zustandsanzeige verlassen.
- **`LAB_KINDS` und `RUNNER_KINDS` laufen auseinander.** Es gibt keinen Netzweg, der beide Listen synchron hält. Bei neuen Lab-Typen immer beide Stellen prüfen. Steht eine Art nur beim Backend, scheitert der Lauf mit einer Runner-Meldung; steht sie nur beim Runner, bleibt sie ungenutzt.
- **Passkey-Domainwechsel entwertet alle Passkeys.** Bei Umzug, neuem Reverse Proxy oder Test- statt Produktionsdomain müssen alle Passkeys neu registriert werden. Das Passwort bleibt vollwertiger Anmeldeweg.
- **Migrationen persistierten auf Postgres nicht (v1.24.1 bis v1.41.1).** `migrations/env.py` setzte `lock_timeout` in einer Transaktion, die nie committet wurde. Alembic meldete „Running upgrade“, Postgres rollte alles zurück; `alembic_version` blieb auf dem Stand vor v1.24.1. Ursache der Crashloops vom 22./23.07.2026. Der Fix lässt die ausstehenden Migrationen beim ersten Start danach erstmals wirklich wirken (siehe Checkliste unten).
- **Migrations-Guard nicht vergessen** (siehe Abschnitt Datenbank-Migrationen).
- **Rate-Limit hinter Proxy.** Das Rate-Limiting (`backend/app/services/ratelimit.py`) nimmt die Client-IP aus `X-Forwarded-For`. Das ist nur sicher, weil nginx per `real_ip`-Modul die echte Client-IP aus der Kette Traefik/Coolify, nginx ermittelt und dabei private Ranges als „trusted“ behandelt. Ändert sich die Proxy-Kette (anderer Ingress, nginx direkt exponiert, ein Hop weniger), muss diese Annahme neu geprüft werden.
- **Bewertung der `set_real_ip_from`-Zeilen (Stand v1.43, nicht geändert).** `frontend/nginx.conf` vertraut allen privaten Netzen (10/8, 172.16/12, 192.168/16), weil das Docker-Subnetz des Ingress je Coolify-Installation anders ist. Folgen: (1) Jeder Container im selben Docker-Netz wie das Frontend kann `X-Forwarded-For` frei setzen; betroffen ist nur das Rate-Limit und die IP im Log, keine Anmeldung; der Runner hat kein Netz. (2) Kommen die Nutzer selbst aus einem privaten Netz (Intranet, VPN), ist das IP-Rate-Limit umgehbar. Abhilfe dann: die drei Zeilen durch das konkrete Subnetz oder die Adresse des Ingress ersetzen (`docker network inspect <netz>`) und mit zwei Clients prüfen, dass das Backend unterschiedliche IPs sieht.
- **Frontend-Cache nach Deploy.** `index.html` wird mit `Cache-Control: no-cache` ausgeliefert, Dateien mit Hash im Namen ein Jahr `immutable`. Die Sicherheits-Header liegen in `frontend/nginx-security-headers.conf` und werden in jedem `location`-Block mit eigenem `add_header` erneut eingebunden, da nginx `add_header` sonst nicht vererbt (vor v1.43 fehlten CSP und HSTS auf allen JS- und CSS-Dateien).
- **Kurs löschen und Zertifikate.** Zertifikate überleben das Löschen eines Kurses standardmäßig und bleiben mit Namen unter `/verify/<id>` öffentlich. Der Lösch-Dialog nennt die Zahl und bietet „Teilnahmebestätigungen mitlöschen“ an (`DELETE /api/courses/{id}?delete_certificates=true`). Das Audit-Log hält fest, wie viele gelöscht bzw. behalten wurden.
- **Teilnehmer ohne Wiederaufnahme-Code.** Sie kommen seit v1.43 nicht mehr allein über ihren Namen hinein. Der Trainer vergibt im Kurs-Detail über „Code zurücksetzen“ einen Code und gibt ihn persönlich weiter.

## Upgrade auf v1.42.0 / v1.43.0

Diese Checkliste fasst die im Repository dokumentierten Rollout-Schritte zusammen (Quelle: `docs/operations.md`, Abschnitte „Modul-Editor“, „Zeitstempel der API“, „Content-Sync“). Die Reihenfolge ist eine Zusammenstellung; die einzelnen Schritte stammen aus `docs/operations.md`, `docs/lab-sicherheit.md`, `README.md` und dem Änderungslog.

Hintergrund: Auf Postgres-Instanzen mit v1.24.1 bis v1.41.1 sind Migrationen nie dauerhaft angekommen. Beim ersten Start mit der korrigierten Version laufen sie erstmals wirklich. Das betrifft auch das Löschen verwaister Zeilen durch `75aeb8d5399c`.

1. **Backup ziehen.** `ops/backup.sh` (bzw. `pg_dump`) ausführen. Das ist Pflicht, nicht Kür.
2. **Ausgangslage notieren.** `SELECT version_num FROM alembic_version;` und das Ergebnis aufschreiben.
3. **Verwaiste Zeilen zählen.** `75aeb8d5399c` löscht Teilnehmer, Kurs-Module und Kommentare ohne Kurs sowie Fortschritt, Quiz-Ergebnisse und Kommentare ohne Teilnehmer. Vorher zählen, zum Beispiel mit `SELECT count(*) FROM participant WHERE course_id NOT IN (SELECT id FROM course);`
4. **Zeitzone des Postgres prüfen.** `SHOW timezone;` ausführen und das Ergebnis notieren. Das Backend setzt seine Sitzungszeitzone jetzt auf UTC (`backend/app/database.py`). Stand der Server bisher nicht auf UTC, enthalten Bestandszeilen Ortszeit und werden nach dem Deploy um den Versatz falsch angezeigt; neue Zeilen stimmen. API-Zeitfelder (`created_at`, `issued_at`, `last_used_at`) tragen den Offset `+00:00`.
5. **Platzhalter-Secrets prüfen.** `SECRET_KEY`, `POSTGRES_PASSWORD` und `ADMIN_PASSWORD` dürfen keine `change-me`-Platzhalter sein; mit Platzhaltern startet das Backend bewusst nicht.
6. **Backend und Runner gemeinsam ausrollen.** Ein neues Backend mit altem Runner verwirft jedes Lab-Ergebnis mit `502`. Ein neuer Runner mit altem Backend funktioniert. `LAB_KINDS` und `RUNNER_KINDS` dabei zusammen pflegen. Läuft das Lab nicht, entfällt dieser Schritt.
7. **Deployen und Start beobachten.** Beim ersten Start laufen die ausstehenden Migrationen, darunter `a6b7c8d9e0f1` (Kennungen und Quiz-Erklärung), `b7c8d9e0f1a2` (`goals_en`), `c8d9e0f1a2b3` (Live-Abstimmung), `3f9a1c7e2b40` (Trainer-Rolle) und `9f3e7a1c5b2d` (Abstimmungsarten). Danach: `alembic_version` entspricht dem Head (laut Repository `9f3e7a1c5b2d`), und der zweite Start zeigt keine „Running upgrade“-Zeile mehr.
8. **Content-Sync-Log prüfen.** Erwartet wird `Content-Sync: N Module auf Auslieferungsstand aktualisiert: …` und ein Audit-Eintrag `content.sync`. Eine Meldung „konnte nicht aktualisiert werden“ bitte melden.
9. **Trainer-editierte Module nachziehen.** Module, die ein Trainer verändert hat, bleiben unangetastet und stehen in der Meldung „weichen vom Auslieferungsstand ab“. Wer die neuen Inhalte will: im Modul-Editor „Auslieferungszustand laden“ und eigene Änderungen danach wieder einpflegen. Wer seinen Stand behalten will, muss nichts tun.
10. **Modul-Auswahl der Kurse prüfen.** Abgewählte Module bleiben seit v1.42.0 nach einem Neustart abgewählt (Tabelle `module_disabled`). Die Modul-Auswahl jedes Kurses einmal kontrollieren. Neue Module rücken automatisch in bestehende Kurse nach.
11. **Teilnehmer ohne Wiederaufnahme-Code identifizieren.** Zählen mit `SELECT count(*) FROM participant WHERE resume_code IS NULL;`. Diese Teilnehmer kommen seit v1.43 nicht mehr allein über ihren Namen hinein. Der Trainer vergibt im Kurs-Detail „Code zurücksetzen“ und gibt den Code persönlich weiter.
12. **Header-Check nach dem Deploy.** Für die Startseite `curl -sI https://<host>/ | grep -i -E "cache-control|content-security"` und für eine Asset-Datei dasselbe mit `https://<host>/assets/<datei>.js`. Erwartet: `no-cache` bei `index.html`, lange `immutable`-Dauer bei Dateien mit Hash im Namen, CSP auf beiden.
13. **OpenSSL im Runner prüfen** (nur bei aktivem Lab mit `openssl`): `docker exec <runner-container> openssl version` muss mindestens 3.5 zeigen.
14. **Trainer informieren: offene Editor-Tabs neu laden.** Ein Modul-Editor von vor dem Deploy wird beim Speichern mit `409` abgelehnt (`base_version` fehlt oder ist veraltet); nichts wird gespeichert. Eigene Skripte gegen `PUT /api/trainer/content/modules/{key}` senden erst GET, dann PUT mit `base_version`.
15. **Fragenstatistik beachten.** Bei geänderter Lösung oder geänderter Optionsreihenfolge einer Frage startet deren Statistik in der Trainer-Ansicht und in „Üben: zuletzt falsch“ neu (neue Zeile, siehe „Geänderter Lösungsschlüssel“). Punktzahl, „bestanden“ und Teilnahmebestätigungen bleiben unberührt.
16. **Standardprüfung ausführen:** Abschnitt „Nach jedem Deploy“ (Health, Login, Beitritt, Quiz; bei aktivem Lab `NetworkMode` prüfen).

Hinweis für Teilnehmer während des Updates: Wer ein Quiz vor dem Deploy geladen hat und danach abgibt, bekommt neue Fragen als nicht beantwortet gewertet; Seite neu laden und wiederholen.
