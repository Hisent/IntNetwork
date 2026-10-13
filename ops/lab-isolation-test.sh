#!/usr/bin/env bash
# Echte Pruefung der Trennung der Lab-Laeufe (docs/lab-sicherheit.md,
# "Trennung nachpruefen"). Baut Runner- und Backend-Image, startet den Runner
# mit GENAU der Haertung aus docker-compose.yml in einem eigenen
# Compose-Projekt (eigenes Volume - ein laufendes System bleibt unberuehrt) und
# laesst runner/tests/isolation_check.py aus dem Backend-Image heraus echte
# Auftraege stellen. Laeuft so auch in der CI (Job "runner-isolation").
#
#   bash ops/lab-isolation-test.sh
#
# Ende mit 0, wenn alles stimmt. Sonst steht je Befund eine Zeile "FEHLER ..."
# in der Ausgabe, gefolgt vom Runner-Log.
set -euo pipefail
cd "$(dirname "$0")/.."

export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-nur-fuer-die-pruefung}"  # Pflichtwert der Compose-Datei, hier ungenutzt
export LAB_QUEUE_DIR=/queue
export RUNNER_KINDS=ansible,openssl,git
export RUNNER_TIMEOUT="${RUNNER_TIMEOUT:-30}"

dc() { docker compose -p intlab-isolationspruefung "$@"; }

schluss() {
  rc=$?
  if [ "$rc" -ne 0 ]; then
    echo
    echo "=== FEHLGESCHLAGEN (Exit $rc) - Runner-Log ==="
    dc logs --no-color --tail 200 runner || true
    dc ps -a || true
  fi
  dc down --volumes --remove-orphans >/dev/null 2>&1 || true
  exit "$rc"
}
trap schluss EXIT

fehler() { echo "FEHLER  $*"; exit 1; }
# Log erst vollstaendig holen, dann durchsuchen: "logs | grep -q" bricht unter
# pipefail mit SIGPIPE ab, sobald grep fuendig wird.
im_log() { local log; log="$(dc logs --no-color runner 2>&1)"; grep -qF -- "$1" <<<"$log"; }

echo "=== 1/5 Images bauen ==="
dc build runner backend

echo "=== 2/5 Runner starten ==="
dc up -d --no-deps runner
for _ in $(seq 1 60); do
  if im_log "Lab-Runner bereit"; then break; fi
  sleep 1
done
dc logs --no-color runner
im_log "Lab-Runner bereit" || fehler "Runner meldet nach 60 s kein 'Lab-Runner bereit'"
im_log "Trennung aktiv" \
  || fehler "Runner meldet kein 'Trennung aktiv' - Startpruefung gescheitert (Ursache: Zeile 'ANSIBLE-LAB DEAKTIVIERT' oben)"

echo "=== 3/5 Haertung des Containers (docker inspect) ==="
cid="$(dc ps -q runner)"
[ -n "$cid" ] || fehler "Runner-Container laeuft nicht"
hostconfig="$(docker inspect "$cid" --format \
  'net={{.HostConfig.NetworkMode}} ro={{.HostConfig.ReadonlyRootfs}} drop={{.HostConfig.CapDrop}} add={{.HostConfig.CapAdd}} sec={{.HostConfig.SecurityOpt}} pids={{.HostConfig.PidsLimit}} tmpfs={{json .HostConfig.Tmpfs}} user={{.Config.User}}')"
echo "$hostconfig"
for erwartet in "net=none" "ro=true" "drop=[ALL]" "no-new-privileges" "pids=128" "noexec" "user=0:0" \
                CHOWN DAC_OVERRIDE SETUID SETGID KILL; do
  if grep -qiF -- "$erwartet" <<<"$hostconfig"; then
    echo "OK      Haertung: $erwartet"
  else
    fehler "Haertung fehlt am laufenden Container: $erwartet"
  fi
done
# Genau fuenf Capabilities, nicht mehr.
anzahl="$(docker inspect "$cid" --format '{{len .HostConfig.CapAdd}}')"
[ "$anzahl" = "5" ] || fehler "cap_add hat $anzahl Eintraege statt 5"

echo "=== 4/5 Auftraege aus dem Backend-Image (uid/gid des Backends) ==="
dc run --rm --no-deps -T \
  -v "$PWD/runner/tests/isolation_check.py:/pruefung/isolation_check.py:ro" \
  backend python /pruefung/isolation_check.py --zeitgrenze "$RUNNER_TIMEOUT"

echo "=== 5/5 Nachschau von aussen ==="
dc exec -T runner openssl version
# Nach allen Laeufen darf unter keiner Job-uid mehr ein Prozess existieren.
dc exec -T runner python -c '
import worker
reste = [pid for uid in worker.JOB_UIDS for pid in worker._prozesse_der_uid(uid)]
print("Prozesse unter Job-uids:", reste)
raise SystemExit(1 if reste else 0)' || fehler "Nach den Laeufen laufen noch Prozesse unter einer Job-uid"
# Der Worker hat alle Angriffe ueberlebt und keinen Slot sperren muessen.
[ "$(docker inspect "$cid" --format '{{.State.Running}} {{.RestartCount}}')" = "true 0" ] \
  || fehler "Runner-Container ist waehrend der Pruefung abgestuerzt oder neu gestartet"
if im_log "GESPERRT"; then fehler "Runner hat einen Job-Slot gesperrt (siehe Log)"; fi

echo "=== Trennung der Laeufe: alle Pruefungen bestanden ==="
