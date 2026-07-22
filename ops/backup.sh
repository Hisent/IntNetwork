#!/bin/sh
# Postgres-Backup des Compose-DB-Containers.
#
# Aufruf (aus dem Projekt-Root, wo docker-compose.yml liegt):
#   ops/backup.sh [ziel-verzeichnis]
#
# Cron-Beispiel (täglich 03:00, Projekt unter /opt/intnetwork):
#   0 3 * * * cd /opt/intnetwork && ops/backup.sh /var/backups/intnetwork >> /var/log/intnetwork-backup.log 2>&1
#
# Dumps liegen 14 Tage vor (gzip), ältere werden automatisch gelöscht.

set -eu

BACKUP_DIR="${1:-./backups}"
RETENTION_DAYS=14

mkdir -p "$BACKUP_DIR"

STAMP=$(date +%Y%m%d-%H%M%S)
DUMP_FILE="$BACKUP_DIR/intnetwork-$STAMP.sql"
OUT_FILE="$DUMP_FILE.gz"

# Zweistufig statt "pg_dump | gzip > datei": in einer Pipe unter
# dash/#!/bin/sh (kein pipefail) sieht set -e nur den Exit-Code von gzip, nie
# den von pg_dump -- scheitert pg_dump, entsteht trotzdem eine (leere/kaputte)
# .gz-Datei und das Skript meldet "Erfolg". Erst in eine Datei dumpen (set -e
# greift auf den echten pg_dump-Exit-Code), dann separat komprimieren.
docker compose exec -T db pg_dump -U intnetwork intnetwork > "$DUMP_FILE"
gzip "$DUMP_FILE"

echo "Backup geschrieben: $OUT_FILE"

find "$BACKUP_DIR" -name 'intnetwork-*.sql.gz' -mtime "+$RETENTION_DAYS" -delete
