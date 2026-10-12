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
Quizfragen, Titel, Reihenfolge und Voraussetzungen. Fragen und Blöcke werden
dabei in ihren vorhandenen Zeilen überschrieben; Frage-ids, Quiz-Abgaben,
Fortschritt, Kurs-Aktivierungen und Kommentare bleiben erhalten. Ein zweiter
Start ändert nichts mehr.

Als unverändert gilt ein Modul, wenn sein Stand noch dem beim letzten Sync
gespeicherten Hash entspricht (Tabelle `setting`, Schlüssel
`content-sync:<modul>`). Datenbanken aus der Zeit vor dem Sync haben diesen
Hash nicht; dort zählt ein Modul als unverändert, wenn es nie im Editor
gespeichert wurde (kein Eintrag in `content_module_snapshot`) oder sein Stand
ein bekannter Auslieferungsstand bis v1.41.1 ist
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

Gründe für ein ausgelassenes Modul und was zu tun ist:

- **vom Trainer geändert** — der Trainer-Stand hat Vorrang. Wer die neuen
  Inhalte will: im Modul-Editor „Auslieferungszustand laden“ und die eigenen
  Änderungen danach wieder einpflegen (die vorherige Fassung liegt eine Stufe
  tief unter „Vorherige Version wiederherstellen“). Achtung: Dieser Weg legt die Quizfragen neu
  an, frühere Abgaben erscheinen danach nicht mehr in der Fragenstatistik.
  Ist das Modul wieder auf Auslieferungsstand, nimmt es ab dem nächsten Start
  wieder am Sync teil. Wer seinen Stand behalten will, muss nichts tun.
- **Blöcke sind hinzugekommen oder entfallen und es gibt Kommentare** —
  Kommentare hängen an der Blockposition; statt sie an einen fremden Block zu
  hängen, bleibt das Modul stehen. Reines Umsortieren ist kein Problem, die
  Kommentare wandern mit. Abhilfe: Kommentare des Moduls klären/löschen oder
  das Modul wie oben von Hand laden.
- **Quizstruktur weicht ab und es gibt Quiz-Abgaben** — Anzahl oder Typ der
  Fragen passen nicht mehr zu den Fragen, an denen Abgaben hängen. Abhilfe wie
  oben; im laufenden Kurs besser bis zum Kursende warten.

Inhaltsänderungen brauchen damit keine handgeschriebene Text-Migration in
`seed.py` mehr. Die vorhandenen Migrationen bleiben für alte Datenbanken
bestehen und laufen vor dem Sync.

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

- **Kein Healthcheck für backend/frontend.** Nur der `db`-Service hat einen
  Compose-Healthcheck. Traefik hat backend/frontend deshalb schon einmal als
  "up" behandelt, während der Container intern nicht mehr antwortete
  (Vorfall 2026-07-21). Bis das nachgerüstet ist: Monitoring auf
  `GET /api/health` (siehe oben) ist die einzige externe Absicherung — nicht
  auf Traefiks eigene Zustandsanzeige verlassen.
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
