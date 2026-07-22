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
