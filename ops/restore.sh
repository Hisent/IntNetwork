#!/bin/sh
# Postgres-Restore in den Compose-DB-Container.
#
# ACHTUNG: überschreibt die laufende Datenbank. Vorher ggf. selbst ein
# frisches Backup ziehen (ops/backup.sh).
#
# Aufruf (aus dem Projekt-Root, wo docker-compose.yml liegt):
#   ops/restore.sh pfad/zum/dump.sql.gz
#
# Cron ist hier bewusst nicht vorgesehen — Restore ist ein manueller Akt.

set -eu

DUMP_FILE="${1:-}"

if [ -z "$DUMP_FILE" ]; then
    echo "Nutzung: $0 <dump.sql.gz>" >&2
    exit 1
fi

if [ ! -f "$DUMP_FILE" ]; then
    echo "Datei nicht gefunden: $DUMP_FILE" >&2
    exit 1
fi

echo "WARNUNG: Dies überschreibt die Datenbank 'intnetwork' im laufenden db-Container"
echo "mit dem Inhalt von: $DUMP_FILE"
printf "Fortfahren? Tippe 'ja' zum Bestätigen: "
read -r CONFIRM
if [ "$CONFIRM" != "ja" ]; then
    echo "Abgebrochen."
    exit 1
fi

gunzip -c "$DUMP_FILE" | docker compose exec -T db psql -U intnetwork intnetwork

echo "Restore abgeschlossen."
