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

## Monitoring

Ein externer Monitor soll mindestens `/api/health` im Minutenintervall
aufrufen und bei zwei aufeinanderfolgenden Fehlschlägen alarmieren. Die
Einrichtung erfolgt in der jeweiligen Hosting-Plattform; dieses Repository
kann keinen externen Alarmkanal mit Zugangsdaten konfigurieren.

## Backups und Restore-Test

`ops/restore.sh` beschreibt das Einspielen eines PostgreSQL-Dumps. Mindestens
vierteljährlich einen aktuellen Dump in eine isolierte Testdatenbank
wiederherstellen und dort Login, Kursdaten, Fortschritt und Kommentare prüfen.
Ein Backup ohne erfolgreichen Restore-Test gilt nicht als verifiziert.
