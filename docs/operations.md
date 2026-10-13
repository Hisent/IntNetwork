# Betrieb: Mindestkontrollen und Wiederherstellung

Diese Checks ergänzen die Container-Limits. Sie sind absichtlich kurz, damit
sie bei jedem Rollout tatsächlich durchgeführt werden.

## Nach jedem Deploy

1. `GET /api/health` muss erfolgreich antworten.
2. Trainer-Login, Kursbeitritt und ein Quiz einmal im Browser prüfen.
3. Falls das Lab aktiv ist: einen harmlosen Lauf zweimal ausführen und im
   Runner prüfen, dass `NetworkMode` weiterhin `none` ist (Details in
   `docs/lab-sicherheit.md`).
4. Die CI muss grün sein. `pip-audit` und `npm audit --omit=dev` sind bewusst
   blockierend; ein Advisory wird vor dem Deploy bewertet und nicht übergangen.

## Content-Sync: geänderte Kursinhalte nach einem Deploy

Kursinhalte liegen im Code (`backend/app/content/*.py`), ausgeliefert wird aus
der Datenbank. Beim Start gleicht `seed_missing_content()` beides ab
(`backend/app/content/sync.py`): Jedes mitgelieferte Modul, das kein Trainer
verändert hat, wird auf den Stand der Quelle gebracht — Texte, Blöcke,
Quizfragen (samt Erklärungen), Titel, Lernziele (deutsch und, seit der Migration
`b7c8d9e0f1a2`, englisch in `content_module.goals_en`), Reihenfolge und
Voraussetzungen. Ein Modul ohne `goals_en` behält seinen bisherigen Hash, gilt
also weiter als unverändert; kommt `goals_en` mit einem Release dazu, wird es
wie jede andere Inhaltsänderung eingespielt. Ein
zweiter Start ändert nichts mehr.

Zugeordnet wird über Kennungen: jeder Block und jede Frage trägt eine je Modul
eindeutige `id` in der Quelle (Spalte `uid` in `content_block` und
`content_quiz_question`, seit v1.43.0; Regeln für Autoren in
`docs/content-authoring.md`). Daraus folgt, auch wenn Teilnehmerdaten am Modul
hängen:

- **bekannte Kennung** — die Zeile wird überschrieben und behält ihre
  Datenbank-id. Quiz-Abgaben, Fragenstatistik und Kommentare bleiben dran.
  Ausnahme Fragen mit geändertem Lösungsschlüssel, siehe unten.
- **neue Kennung** — Block/Frage wird an der Stelle der Quelle eingefügt.
- **Kennung entfällt** — die Zeile wird gelöscht. Kommentare an einem
  entfallenen Block werden nicht gelöscht, sondern hängen danach am nächsten
  verbliebenen Block davor (Logzeile `… Kommentar(e) an entfallenen Blöcken`).
- **Reihenfolge** — wie in der Quelle; Kommentare wandern mit ihrem Block.

Was mit Quiz-Ergebnissen passiert: nichts rückwirkend. `quiz_result` speichert
Punktzahl und Gesamtzahl zum Zeitpunkt der Abgabe; „bestanden“, Fortschritt,
Bestwert und Zertifikate ändern sich nicht, wenn Fragen hinzukommen oder
entfallen. Neue Fragen zählen ab der nächsten Abgabe; in der Fragenstatistik
der Trainer-Ansicht zählt je Frage nur als Versuch, wer sie in seiner Abgabe
hatte. Wer das Quiz vor dem Deploy geladen hat und danach abgibt, bekommt die
neuen Fragen als nicht beantwortet gewertet (Abhilfe: Seite neu laden,
wiederholen).

Geänderter Lösungsschlüssel unter gleicher Kennung (Sync, Speichern im Editor,
„Auslieferungszustand laden“, Wiederherstellen): Eine Fragezeile wird nur
wiederverwendet, wenn Fragetyp und Lösung gleich sind und kein weiter
vorhandener Optionstext (deutsch oder englisch) an einer anderen Position
steht. Sonst entsteht eine neue Zeile mit neuer Datenbank-id und die alte
entfällt: alte Abgaben (gespeichert ist nur der gewählte Index) zählen für
diese Frage dann weder in der Fragenstatistik noch in „Üben: zuletzt falsch“.
Punktzahl, „bestanden“ und Zertifikate bleiben unberührt. Textkorrekturen an
Frage, Erklärung und Optionswortlaut sowie eine hinten angefügte oder
gestrichene Option behalten die Zeile samt Statistik. Nicht erkennbar ist ein
Umsortieren, bei dem zugleich alle Optionen umformuliert werden — dafür
vergeben Autoren eine neue Kennung (`docs/content-authoring.md`, Regel 5/6).

Gleichzeitiges Speichern: Die Prüfung „unverändert“ sperrt die Modulzeilen
(Postgres, `FOR NO KEY UPDATE`) bis zum Commit des Syncs; dieselbe Sperre nimmt
der Editor beim Speichern. Ein Trainer, der während des Starts speichert,
wartet kurz und bekommt 409, falls der Sync sein Modul geändert hat. Speichert
er über einen noch laufenden ALTEN Container (Rolling-Deploy, kennt die Sperre
nicht), liest der Sync vor dem Einspielen frisch und lässt das Modul als „vom
Trainer geändert“ aus. Ausgenommen sind Module, die eine Seed-Migration
desselben Starts selbst angefasst hat.

Datenbanken bis v1.42.0 haben noch keine Kennungen. Beim ersten Start mit
v1.43.0 legt die Migration `a6b7c8d9e0f1` die Spalten an, und der Sync trägt
die Kennungen einmalig ein — für jedes Modul, auch für vom Trainer geänderte:
anhand des Stands v1.42.0 (`"structure"` in `sync_baseline.json`), Widgets über
ihre Widget-id, andere Blöcke als n-ter Block ihres Typs, Fragen über ihre
Position. Was dazu nicht passt (eigene Blöcke/Fragen, eigene Module), bekommt
eine zufällige Kennung (`x…`).

Als unverändert gilt ein Modul, wenn sein Stand noch dem beim letzten Sync
gespeicherten Hash entspricht (Tabelle `setting`, Schlüssel
`content-sync:<modul>`). Datenbanken aus der Zeit vor dem Sync haben diesen
Hash nicht; dort zählt ein Modul als unverändert, wenn es nie im Editor
gespeichert wurde (kein Eintrag in `content_module_snapshot`) oder sein Stand
ein bekannter Auslieferungsstand bis v1.42.0 ist
(`backend/app/content/sync_baseline.json`, erzeugt von
`backend/build_content_baseline.py`).

Im Log (Logger `app.content.sync`, Stufe WARNING) steht nach einem Deploy:

- `Content-Sync: N Module auf Auslieferungsstand aktualisiert: …` — einmal je
  Release, dazu ein Eintrag `content.sync` im Audit-Log der Trainer-Oberfläche
  (Benutzer `system`).
- `Content-Sync: N Module weichen vom Auslieferungsstand ab und bleiben
  unangetastet: <modul> (<Grund>); …` — bei jedem Start, solange es zutrifft.
  Kommt für ein solches Modul neuer Inhalt mit einem Release, entsteht einmalig
  der Audit-Eintrag `content.sync.skipped` mit dem Grund.
- `Content-Sync: Modul <modul> konnte nicht aktualisiert werden` mit
  Traceback — nur dieses Modul bleibt auf dem alten Stand, der Start läuft
  weiter. Bitte melden.

Ausgelassene Module und was zu tun ist:

- **vom Trainer geändert** — der Trainer-Stand hat Vorrang; das ist der einzige
  Grund, aus dem ein Modul ausgelassen wird. Wer die neuen Inhalte will: im
  Modul-Editor „Auslieferungszustand laden“ und die eigenen Änderungen danach
  wieder einpflegen (die vorherige Fassung liegt eine Stufe tief unter
  „Vorherige Version wiederherstellen“). Seit v1.43.0 arbeiten Speichern,
  „Auslieferungszustand laden“ und Wiederherstellen ebenfalls über die
  Kennungen: Fragen und Blöcke, die es vorher schon gab, behalten ihre Zeile —
  laufende Abgaben und die Fragenstatistik bleiben gültig. Nur an einem dabei
  entfernten Block gehen die Kommentare verloren. Ist das Modul wieder auf
  Auslieferungsstand, nimmt es ab dem nächsten Start wieder am Sync teil. Wer
  seinen Stand behalten will, muss nichts tun.

Inhaltsänderungen brauchen damit keine handgeschriebene Text-Migration in
`seed.py` mehr. Die vorhandenen Migrationen bleiben für alte Datenbanken
bestehen und laufen vor dem Sync.

## Modul-Editor: Speichern, Sperre, Kennungen

- **`base_version` ist Pflicht** (`PUT /api/trainer/content/modules/{key}?base_version=…`,
  Wert = `version` aus dem GET). Fehlt sie oder ist sie veraltet, antwortet die
  API mit 409 und speichert nichts. Hintergrund: ein Editor-Tab von vor einem
  Update kennt neuere Felder (Erklärungen, `goals_en`) nicht und hätte sie beim
  Speichern still gelöscht. **Rollout:** Trainer mit offenem Editor müssen nach
  dem Deploy die Seite neu laden; eigene Skripte gegen diese API müssen erst
  GET, dann PUT mit `base_version` senden.
- **Atomar:** Speichern, „Auslieferungszustand laden“ und Wiederherstellen
  sperren unter Postgres die Modulzeile (`SELECT … FOR NO KEY UPDATE`). Zwei
  gleichzeitige PUTs laufen nacheinander; der zweite scheitert an
  `base_version` (409). Unter SQLite (nur Entwicklung/Tests) gibt es die
  Zeilensperre nicht.
- **Kein Unique-Index auf `(module_key, uid)` (bewusst, Plan):** Die
  Eindeutigkeit der Kennungen stellt der Code sicher (`_write_rows` vergibt bei
  doppelt gelieferter Kennung eine neue). Ein Index per Migration könnte an
  Bestandsdaten scheitern und den Start blockieren. Falls gewünscht: zuerst
  `SELECT module_key, uid, count(*) FROM content_block WHERE uid IS NOT NULL
  GROUP BY 1, 2 HAVING count(*) > 1` (ebenso `content_quiz_question`); die
  Migration legt den Index nur an, wenn beide Abfragen leer sind, und warnt
  sonst im Log, statt zu scheitern.
- Leere optionale Textfelder (`note`, `value_de/en`, `widget_id`, Erklärungen,
  `goals_en`) werden als „nicht gesetzt“ gespeichert; ein unverändertes
  Speichern macht ein Modul nicht zu einem Trainer-Stand.

## Zeitstempel der API

Alle Zeitfelder (`created_at`, `issued_at`, `last_used_at`) kommen als ISO 8601
in UTC mit Offset, z. B. `2026-10-13T11:50:00.123456+00:00` (`iso_utc` in
`backend/app/utils.py`). Die Datenbankspalten bleiben zeitzonenlos und
enthalten UTC; damit das nicht von der Zeitzone des Postgres-Servers abhängt,
setzt das Backend für seine Sitzungen `timezone=UTC` (`backend/app/database.py`).
Prüfen vor dem Deploy: `SHOW timezone;` — stand der Server bisher NICHT auf UTC,
enthalten Bestandszeilen Ortszeit und werden um den Versatz falsch angezeigt
(neue Zeilen stimmen).

## Bekannte Eigenschaften (bewusst so)

- **Üben ist ein Lösungs-Orakel für bereits abgegebene Module.**
  `POST /api/practice/check` sagt je Frage richtig/falsch und liefert die
  Erklärung — wie das Quiz nach jeder Abgabe, und das Quiz ist beliebig
  wiederholbar. Wer ein Modul einmal abgegeben hat, kann sich die Lösungen
  also erarbeiten; das ist konstruktionsbedingt (Lernplattform, keine Prüfung).
  Mögliche Abhilfe, falls das Zertifikat härter werden soll: Üben erst für
  BESTANDENE Module öffnen (`_last_answers` in `routers/learning.py`).
- **Die Reihenfolge-Sperre der Module ist nur Anzeige.** Voraussetzungen
  (`prerequisites`) sperren Module im Frontend; die API liefert jedes im Kurs
  freigeschaltete Modul auch ohne erfüllte Voraussetzung aus. Das ist
  didaktische Führung, keine Zugriffskontrolle — die Zugriffskontrolle ist die
  Freischaltung je Kurs.
- **Namen im Kurs sind beim Beitritt erkennbar.** Der Beitritt unter einem
  vergebenen Namen verlangt den Wiederaufnahme-Code; daran lässt sich mit dem
  Kurscode ablesen, ob ein Name im Kurs existiert. Der Kurscode ist das
  Geheimnis des Kurses; Rate-Limit je IP begrenzt das Durchprobieren.
- **Abgewähltes Modul:** `GET /api/modules/{key}`, `/heartbeat` und `/quiz`
  antworten mit 404 und einem Feld `code` neben `detail`:
  `module_not_enabled` (im Kurs abgewählt) bzw. `module_unknown`.

## Alembic-Downgrade

Der Downgrade von `b7c8d9e0f1a2` (entfernt `goals_en`) und `a6b7c8d9e0f1`
(entfernt Kennungen und Erklärungen) löscht die gespeicherten Sync-Hashes
(`setting`, Schlüssel `content-sync:*`). Ohne das gälte nach einem erneuten
Upgrade jedes Modul dauerhaft als „vom Trainer geändert“. Folge: nach
Downgrade + Upgrade greift die Bootstrap-Regel des Syncs (nie im Editor
gespeichert oder bekannter Stand bis v1.42.0 = unverändert); Module, die je im
Editor gespeichert wurden, bleiben vorsichtshalber Trainer-Stand
(„Auslieferungszustand laden“ holt sie zurück).

## Live-Abstimmung

Zwei Tabellen (Migration `c8d9e0f1a2b3`): `live_poll` (je Kurs höchstens eine
nicht geschlossene Zeile) und `live_poll_vote` (eine Zeile je Teilnehmer und
Abstimmung). Beide hängen per `ON DELETE CASCADE` am Kurs bzw. Teilnehmer; ein
Aufräumjob ist nicht nötig (wenige Zeilen je Workshop-Tag). Der Zustand liegt
ausschließlich in der DB, mehrere Worker sind unkritisch.

Last: Jeder Teilnehmer mit offenem, sichtbarem Modul fragt alle 5 s
`GET /api/modules/{key}/poll` ab (n Teilnehmer ÷ 5 Anfragen/s — 20 Teilnehmer
≈ 4/s, je eine Handvoll kleiner Lesezugriffe); im Hintergrund-Tab ruht die
Abfrage. Der Beamer lädt nur während einer laufenden Abstimmung alle 2 s nach.
Bleibt eine Abstimmung offen (Browser geschlossen), beendet sie der Trainer im
Beamer-Modus desselben Kurses oder die nächste Abstimmung schließt sie.

## Monitoring

Ein externer Monitor soll mindestens `/api/health` im Minutenintervall
aufrufen und bei zwei aufeinanderfolgenden Fehlschlägen alarmieren. Die
Einrichtung erfolgt in der jeweiligen Hosting-Plattform; dieses Repository
kann keinen externen Alarmkanal mit Zugangsdaten konfigurieren.

## Backups und Restore-Test

`ops/restore.sh` spielt einen PostgreSQL-Dump ein (ersetzt das Schema `public` in
einer Transaktion; Backend vorher stoppen). Mindestens
vierteljährlich einen aktuellen Dump in eine isolierte Testdatenbank
wiederherstellen und dort Login, Kursdaten, Fortschritt und Kommentare prüfen.
Ein Backup ohne erfolgreichen Restore-Test gilt nicht als verifiziert.

## Bekannte Fallstricke / Vorfälle

- **Kein Healthcheck für backend/frontend (bewusst).** Nur der `db`-Service
  hat einen Compose-Healthcheck. Coolify/Traefik routet nur auf Container im
  Zustand „healthy“; ein Check, der in der Umgebung anders ausfällt als lokal
  gedacht, nimmt den Dienst komplett vom Netz („no available server“, Vorfall
  2026-07-21). `docker-compose.yml` sagt deshalb ausdrücklich: keinen
  Healthcheck eintragen; falls doch gewünscht, erst in Coolify gegen einen
  Test-Deploy verifizieren. Bis dahin ist das Monitoring auf `GET /api/health`
  (siehe oben) die einzige externe Absicherung; nicht auf Traefiks eigene
  Zustandsanzeige verlassen.
- **`LAB_KINDS` (Backend) und `RUNNER_KINDS` (Runner) laufen auseinander.**
  Es gibt keinen Netzweg, der diese beiden Listen automatisch synchron hält —
  wird im Backend ein neuer Lab-Kind hinzugefügt, muss der Runner von Hand
  nachgezogen werden (und umgekehrt). Bei neuen Lab-Typen immer beide Stellen
  prüfen.
- **Passkey-Domainwechsel entwertet alle Passkeys.** `WEBAUTHN_RP_ID` und
  `WEBAUTHN_ORIGIN` müssen die öffentliche Adresse sein, mit der Trainer und
  Teilnehmer tatsächlich im Browser arbeiten — nicht der interne
  Containername. Ändert sich die öffentliche Domain (Umzug, neuer Reverse
  Proxy, Test- vs. Prod-Domain), sind alle bestehenden Passkeys ungültig und
  müssen neu registriert werden.
- **Migrationen persistierten auf Postgres nicht (v1.24.1 bis v1.41.1).**
  `migrations/env.py` setzte `lock_timeout` in einer Transaktion, die nie
  committet wurde; Alembic meldete „Running upgrade“, Postgres rollte beim
  Verbindungsende alles zurück. Folge: `alembic_version` blieb auf dem Stand vor
  v1.24.1 stehen, jede Migration lief bei jedem Start erneut ins Leere (Ursache
  der Crashloops vom 22./23.07.2026). Der Fix lässt die ausstehenden Migrationen
  beim **ersten Start danach erstmals wirklich** wirken. Vor diesem Deploy:
  1. Backup ziehen (`pg_dump`) — Pflicht, nicht Kür.
  2. Ausgangslage notieren: `SELECT version_num FROM alembic_version;`
  3. `75aeb8d5399c` löscht verwaiste Zeilen jetzt tatsächlich (Teilnehmer,
     Kurs-Module, Kommentare ohne Kurs; Fortschritt, Quiz-Ergebnisse, Kommentare
     ohne Teilnehmer). Vorher zählen, z. B.
     `SELECT count(*) FROM participant WHERE course_id NOT IN (SELECT id FROM course);`
  4. Nach dem Deploy: `alembic_version` = Head, und der zweite Start zeigt
     keine „Running upgrade“-Zeile mehr.
- **Migrations-Guard nicht vergessen.** Jede neue Migration, die eine Tabelle
  per `create_table` anlegt, braucht den `has_table`-Guard (idempotent
  gegen bereits vorhandene Tabellen). Ohne Guard gab es bereits einen
  Crashloop, weil eine Migration beim Neustart erneut gegen eine schon
  existierende Tabelle lief.
- **Rate-Limit hinter Proxy — Vertrauensannahme dokumentieren.** Das
  Rate-Limiting (`app/services/ratelimit.py`) nimmt die Client-IP aus
  `X-Forwarded-For`. Das ist nur sicher, weil nginx (per `real_ip`-Modul) die
  echte Client-IP aus der Proxy-Kette Traefik/Coolify → nginx ermittelt und
  dabei private Ranges als "trusted" behandelt (recursive) — nginx reicht den
  vom Client selbst gesendeten `X-Forwarded-For` also NICHT ungeprüft durch.
  Ändert sich die Proxy-Kette (anderer Ingress, nginx wird direkt exponiert,
  ein Hop entfällt), muss diese Annahme neu geprüft werden — sonst kann ein
  Angreifer den Header fälschen und das Rate-Limit umgehen bzw. anderen
  Nutzern deren Limit unterschieben. Die nginx-Konfiguration selbst liegt
  außerhalb dieses Dokuments; hier steht nur die Betriebsannahme, die dabei
  nicht verletzt werden darf.
  **Bewertung der `set_real_ip_from`-Zeilen (Stand v1.43, nicht geändert):**
  `frontend/nginx.conf` vertraut allen privaten Netzen (10/8, 172.16/12,
  192.168/16), nicht nur der Adresse von Traefik. Das ist bewusst so gelassen,
  weil das Docker-Subnetz des Ingress je Coolify-Installation anders ist und
  sich ändern kann — ein fest eingetragenes Subnetz, das nicht mehr stimmt,
  wirft alle Nutzer in EINEN Rate-Limit-Eimer (schlimmer als der Ist-Zustand).
  Daraus folgen zwei Grenzen, die man kennen muss:
  1. Jeder Container im selben Docker-Netz wie das Frontend kann nginx direkt
     ansprechen und `X-Forwarded-For` frei setzen. Betroffen ist nur das
     Rate-Limit (und die IP im Log), keine Anmeldung. Der Lab-Runner hat kein
     Netz und scheidet aus.
  2. Kommen die **Nutzer selbst aus einem privaten Netz** (Intranet, VPN, also
     Client-IP 10.x/172.16–31.x/192.168.x), überspringt `real_ip_recursive`
     auch deren echte Adresse und nimmt den Wert links davon — den der Client
     frei wählen kann. In so einem Betrieb ist das IP-Rate-Limit umgehbar.
     Abhilfe dann: die drei Zeilen durch das konkrete Subnetz bzw. die Adresse
     des Ingress ersetzen (`docker network inspect <netz>`), danach mit zwei
     Clients prüfen, dass das Backend unterschiedliche IPs sieht.
- **Frontend-Cache nach Deploy.** `index.html` wird mit `Cache-Control:
  no-cache` ausgeliefert (Browser fragt jedes Mal nach, 304 wenn unverändert),
  die Dateien mit Hash im Namen ein Jahr `immutable`. Die Sicherheits-Header
  liegen in `frontend/nginx-security-headers.conf` und werden in jedem
  `location`-Block mit eigenem `add_header` erneut eingebunden — nginx vererbt
  `add_header` sonst nicht (vor v1.43 fehlten CSP/HSTS auf allen JS/CSS-Dateien).
  Nach einem Deploy prüfen: `curl -sI https://<host>/ | grep -i -E
  "cache-control|content-security"` und dasselbe für eine `/assets/*.js`.
- **Kurs löschen und Zertifikate.** Zertifikate überleben das Löschen eines
  Kurses standardmäßig und bleiben mit Namen unter `/verify/<id>` öffentlich.
  Der Lösch-Dialog nennt die Zahl und bietet „Zertifikate mitlöschen" an
  (`DELETE /api/courses/{id}?delete_certificates=true`); das Audit-Log hält
  fest, wie viele gelöscht bzw. behalten wurden.
- **Teilnehmer ohne Wiederaufnahme-Code (Beitritt vor v1.20).** Sie kommen
  seit v1.43 nicht mehr allein über ihren Namen hinein (das ließ eine Übernahme
  durch jeden zu, der Kurs-Code und Namen kannte). Der Trainer vergibt im
  Kurs-Detail über „Code zurücksetzen" einen Code und gibt ihn persönlich
  weiter. Wie viele betroffen sind:
  `SELECT count(*) FROM participant WHERE resume_code IS NULL;`
