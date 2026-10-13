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
# in der Ausgabe, gefolgt vom Runner-Log des betroffenen Schritts. Ein FEHLER
# bricht NICHT ab: alle sieben Schritte laufen, am Ende steht die Liste aller
# Befunde und der Exit-Code 1. Abgebrochen wird nur, wenn nichts mehr
# pruefbar ist (Images bauen nicht).
# Bewusst ohne "set -e": jeder Befehl, dessen Scheitern zaehlt, steht in einem
# "|| fehler".
set -uo pipefail
cd "$(dirname "$0")/.."

export POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-nur-fuer-die-pruefung}"  # Pflichtwert der Compose-Datei, hier ungenutzt
export LAB_QUEUE_DIR=/queue
export RUNNER_KINDS=ansible,openssl,git
export RUNNER_TIMEOUT="${RUNNER_TIMEOUT:-30}"

dc() { docker compose -p intlab-isolationspruefung "$@"; }

BEFUNDE=()
GEMELDET=0
fehler() { echo "FEHLER  $*"; BEFUNDE+=("$*"); }

# Nach jedem Schritt: gab es darin neue Befunde, das Runner-Log JETZT zeigen -
# die Schritte 6 und 7 starten den Runner neu, danach ist es weg.
schritt_ende() {
  if [ "${#BEFUNDE[@]}" -gt "$GEMELDET" ]; then
    echo "--- Runner-Log zu den Befunden aus Schritt $1 ---"
    dc logs --no-color --tail 120 runner 2>&1 || true
    dc ps -a 2>&1 || true
    GEMELDET="${#BEFUNDE[@]}"
  fi
}

schluss() {
  dc down --volumes --remove-orphans >/dev/null 2>&1 || true
}
trap schluss EXIT
# Log erst vollstaendig holen, dann durchsuchen: "logs | grep -q" bricht unter
# pipefail mit SIGPIPE ab, sobald grep fuendig wird.
im_log() { local log; log="$(dc logs --no-color runner 2>&1)"; grep -qF -- "$1" <<<"$log"; }
ok() { echo "OK      $*"; }

# Startet den Runner frisch (neuer Container, leeres Log) und wartet auf die
# Bereit-Meldung. Argumente: zusaetzliche Compose-Dateien als "-f datei".
runner_neu() {
  dc kill runner >/dev/null 2>&1 || true
  dc rm -f runner >/dev/null 2>&1 || true
  dc -f docker-compose.yml "$@" up -d --no-deps runner
  for _ in $(seq 1 60); do
    if im_log "Lab-Runner bereit"; then break; fi
    sleep 1
  done
  dc logs --no-color runner
  im_log "Lab-Runner bereit" || { fehler "Runner meldet nach 60 s kein 'Lab-Runner bereit'"; return 1; }
}

# Prueft im Runner-Container, dass /queue, in/ und out/ ECHTE Verzeichnisse mit
# root:10001 und 0750/0770 sind. Mit Argument "bestand" zusaetzlich: das Ziel
# des untergeschobenen Symlinks ist unberuehrt, in/ ist abgearbeitet.
queue_pruefen() {
  dc exec -T runner python - "$@" <<'PY'
import os, stat, sys, time

def zustand(pfad):
    st = os.lstat(pfad)
    art = "verzeichnis" if stat.S_ISDIR(st.st_mode) else "symlink" if stat.S_ISLNK(st.st_mode) else "anderes"
    return "%s %d:%d %o" % (art, st.st_uid, st.st_gid, st.st_mode & 0o7777)

erwartet = {"/queue": "verzeichnis 0:10001 750", "/queue/in": "verzeichnis 0:10001 770",
            "/queue/out": "verzeichnis 0:10001 770"}
bestand = sys.argv[1:] == ["bestand"]
if bestand:
    erwartet["/queue/ziel"] = "verzeichnis 10001:10001 777"   # NICHT an root:10001 0770 umgehaengt
    erwartet["/queue/ziel/datei"] = "anderes 10001:10001 644"
    ende = time.time() + 20
    while os.listdir("/queue/in") and time.time() < ende:      # FIFO, Symlink, Verzeichnis abgearbeitet?
        time.sleep(0.5)
fehler = 0
for pfad, soll in erwartet.items():
    ist = zustand(pfad)
    print("%s  (7) %s: %s" % ("OK    " if ist == soll else "FEHLER", pfad, ist) + ("" if ist == soll else " statt " + soll))
    fehler += ist != soll
if bestand:
    rest = os.listdir("/queue/in")
    print("%s  (7) liegengebliebenes FIFO/Symlink/Verzeichnis in in/ entfernt, Worker haengt nicht: %s" % ("FEHLER" if rest else "OK    ", rest))
    inhalt = open("/queue/ziel/datei").read().strip()
    print("%s  (7) Datei im Symlink-Ziel unveraendert: %s" % ("OK    " if inhalt == "liegengeblieben" else "FEHLER", inhalt))
    fehler += bool(rest) + (inhalt != "liegengeblieben")
sys.exit(1 if fehler else 0)
PY
}

echo "=== 1/7 Images bauen ==="
dc build runner backend || { echo "FEHLER  Images lassen sich nicht bauen - nichts pruefbar"; exit 1; }

pruefung() {
  dc run --rm --no-deps -T \
    -v "$PWD/runner/tests/isolation_check.py:/pruefung/isolation_check.py:ro" \
    backend python /pruefung/isolation_check.py --zeitgrenze "$RUNNER_TIMEOUT" "$@"
}

echo "=== 2/7 Runner starten ==="
LAEUFT=0
if runner_neu; then
  LAEUFT=1
  im_log "Trennung aktiv" \
    || fehler "Runner meldet kein 'Trennung aktiv' - Startpruefung gescheitert (Ursache: Zeile 'ANSIBLE-LAB DEAKTIVIERT' oben)"
fi
schritt_ende 2

echo "=== 3/7 Haertung des Containers (docker inspect, /proc/mounts) ==="
cid="$(dc ps -q runner)"
if [ "$LAEUFT" = 1 ] && [ -n "$cid" ]; then
  hostconfig="$(docker inspect "$cid" --format \
    'net={{.HostConfig.NetworkMode}} ro={{.HostConfig.ReadonlyRootfs}} drop={{.HostConfig.CapDrop}} add={{.HostConfig.CapAdd}} sec={{.HostConfig.SecurityOpt}} pids={{.HostConfig.PidsLimit}} user={{.Config.User}}')"
  echo "$hostconfig"
  for erwartet in "net=none" "ro=true" "drop=[ALL]" "no-new-privileges" "pids=128" "user=0:0" \
                  CHOWN DAC_OVERRIDE SETUID SETGID KILL; do
    if grep -qiF -- "$erwartet" <<<"$hostconfig"; then
      ok "Haertung: $erwartet"
    else
      fehler "Haertung fehlt am laufenden Container: $erwartet"
    fi
  done
  # Genau fuenf Capabilities, nicht mehr.
  anzahl="$(docker inspect "$cid" --format '{{len .HostConfig.CapAdd}}')"
  [ "$anzahl" = "5" ] || fehler "cap_add hat $anzahl Eintraege statt 5"
  # tmpfs: was Compose verlangt hat UND was im Container wirklich eingehaengt ist.
  mounts="$(dc exec -T runner cat /proc/mounts)"
  for ort_groesse in /tmp:65536k /dev/shm:16384k; do
    ort="${ort_groesse%%:*}"
    verlangt="$(docker inspect "$cid" --format "{{index .HostConfig.Tmpfs \"$ort\"}}")"
    zeile="$(awk -v ort="$ort" '$2 == ort' <<<"$mounts" | tail -n 1)"
    echo "$ort: verlangt '$verlangt', eingehaengt '$zeile'"
    for option in noexec nosuid nodev; do
      if grep -qF -- "$option" <<<"$verlangt" && grep -qF -- "$option" <<<"$zeile"; then
        ok "Haertung: tmpfs $ort mit $option"
      else
        fehler "tmpfs $ort: $option fehlt (Compose: '$verlangt', im Container: '$zeile')"
      fi
    done
    # Die Groesse belegt, dass wirklich UNSERE Deklaration eingehaengt ist (und
    # nicht z. B. Dockers Standard-/dev/shm mit 64 MB).
    if grep -qF -- " tmpfs " <<<"$zeile" && grep -qF -- "size=${ort_groesse##*:}" <<<"$zeile"; then
      ok "Haertung: tmpfs $ort mit size=${ort_groesse##*:}"
    else
      fehler "tmpfs $ort: nicht mit der Groesse aus docker-compose.yml eingehaengt (${ort_groesse##*:})"
    fi
  done
else
  fehler "Schritt 3 uebersprungen: Runner laeuft nicht"
fi
schritt_ende 3

echo "=== 4/7 Auftraege aus dem Backend-Image (uid/gid des Backends) ==="
if [ "$LAEUFT" = 1 ]; then
  pruefung || fehler "Schritt 4: isolation_check.py meldet Befunde (Zeilen 'FEHLER' oben)"
else
  fehler "Schritt 4 uebersprungen: Runner laeuft nicht"
fi
schritt_ende 4

echo "=== 5/7 Nachschau von aussen ==="
if [ "$LAEUFT" = 1 ]; then
  dc exec -T runner openssl version
  # Nach allen Laeufen darf unter keiner Job-uid mehr ein Prozess existieren.
  if dc exec -T runner python -c '
import worker
reste = [pid for uid in worker.JOB_UIDS for pid in worker._prozesse_der_uid(uid)]
print("Prozesse unter Job-uids:", reste)
raise SystemExit(1 if reste else 0)'; then
    ok "keine Prozesse unter Job-uids"
  else
    fehler "Nach den Laeufen laufen noch Prozesse unter einer Job-uid"
  fi
  # Der Worker hat alle Angriffe ueberlebt und keinen Slot sperren muessen.
  if [ "$(docker inspect "$cid" --format '{{.State.Running}} {{.RestartCount}}')" = "true 0" ]; then
    ok "Worker lief ohne Absturz durch"
  else
    fehler "Runner-Container ist waehrend der Pruefung abgestuerzt oder neu gestartet"
  fi
  if im_log "GESPERRT"; then
    fehler "Runner hat einen Job-Slot gesperrt - ein Lauf konnte das Aufraeumen blockieren (Zeile 'GESPERRT' im Log)"
  else
    ok "kein Job-Slot gesperrt"
  fi
  if im_log "wird verworfen"; then
    fehler "Runner musste ein Arbeitsverzeichnis verwerfen (Zeile 'wird verworfen' im Log)"
  else
    ok "kein Arbeitsverzeichnis verworfen"
  fi
  echo "Was der Worker beim Aufraeumen entfernt hat:"
  dc logs --no-color runner 2>&1 | grep -F -e "entfernt" || echo "  (nichts)"
  queue_pruefen || fehler "/queue ist nach den Laeufen nicht mehr im Sollzustand"
else
  fehler "Schritt 5 uebersprungen: Runner laeuft nicht"
fi
schritt_ende 5

echo "=== 6/7 Start gegen ein praepariertes Bestands-Volume ==="
# So kann ein Volume aus der Zeit vor der Trennung aussehen (alles uid 10001,
# 0777), nachdem ein boesartiger Lauf sich daran zu schaffen gemacht hat:
# out/ ist ein Symlink auf ein fremdes Verzeichnis, in in/ liegen ein FIFO, ein
# Symlink und ein Verzeichnis mit Auftragsnamen.
dc kill runner >/dev/null 2>&1 || true
dc rm -f runner >/dev/null 2>&1 || true
if dc run --rm --no-deps -T --entrypoint sh runner -c '
  set -e
  cd /queue
  rm -rf in out ziel
  mkdir in ziel in/ordner.json
  mkfifo in/fifo.json
  ln -s /etc/hostname in/link.json
  echo liegengeblieben > ziel/datei
  ln -s /queue/ziel out
  chmod 0777 /queue in ziel
  chmod 0644 ziel/datei
  chown -R -h 10001:10001 /queue
  ls -la /queue /queue/in' && runner_neu; then
  im_log "Trennung aktiv" || fehler "(7) Runner startet gegen das Bestands-Volume nicht mit aktiver Trennung"
  queue_pruefen bestand || fehler "(7) Bestands-Volume wurde nicht sauber korrigiert"
  dc logs --no-color --tail 8 runner
  if im_log "wird ersetzt"; then
    ok "(7) Symlink out/ erkannt und durch ein Verzeichnis ersetzt"
  else
    fehler "(7) Runner hat den Symlink out/ nicht als solchen erkannt und ersetzt"
  fi
  for name in fifo link ordner; do
    if im_log "Auftrag unlesbar: $name.claimed"; then
      ok "(7) $name.json abgewiesen"
    else
      fehler "(7) liegengebliebener Eintrag $name.json wurde nicht abgewiesen"
    fi
  done
else
  fehler "(7) Bestands-Volume liess sich nicht praeparieren oder der Runner startet damit nicht"
fi
schritt_ende 6

echo "=== 7/7 Fail-closed: derselbe Runner ohne root ==="
if runner_neu -f ops/lab-isolation-failclosed.override.yml; then
  if im_log "ANSIBLE-LAB DEAKTIVIERT (fail-closed)" && ! im_log "Trennung aktiv"; then
    ok "(8) Log: ANSIBLE-LAB DEAKTIVIERT (fail-closed), keine 'Trennung aktiv'"
  else
    fehler "(8) Runner ohne root meldet kein 'ANSIBLE-LAB DEAKTIVIERT (fail-closed)' oder behauptet 'Trennung aktiv'"
  fi
  pruefung --modus failclosed || fehler "Schritt 7: isolation_check.py --modus failclosed meldet Befunde"
else
  fehler "(8) Runner startet ohne root nicht"
fi
schritt_ende 7

echo
if [ "${#BEFUNDE[@]}" -eq 0 ]; then
  echo "=== Trennung der Laeufe: alle Pruefungen bestanden ==="
  exit 0
fi
echo "=== ${#BEFUNDE[@]} BEFUNDE (Einzelheiten: Zeilen 'FEHLER' oben) ==="
printf '  - %s\n' "${BEFUNDE[@]}"
exit 1
