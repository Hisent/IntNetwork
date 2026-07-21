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
OUT_FILE="$BACKUP_DIR/intnetwork-$STAMP.sql.gz"

docker compose exec -T db pg_dump -U intnetwork intnetwork | gzip > "$OUT_FILE"

echo "Backup geschrieben: $OUT_FILE"

find "$BACKUP_DIR" -name 'intnetwork-*.sql.gz' -mtime "+$RETENTION_DAYS" -delete
