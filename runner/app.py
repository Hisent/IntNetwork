"""Ansible-Lab-Runner — führt Teilnehmer-Playbooks aus.

Bedrohungsmodell (bitte vor Änderungen lesen):
Ein Playbook ist ausführbarer Code. Module wie `command`, `shell` oder `script`
sind Teil von Ansible und lassen sich nicht sinnvoll wegfiltern — wer ein
Playbook schreiben darf, darf in diesem Container Code ausführen. Das ist
Absicht, deshalb ist der Container die Sicherheitsgrenze und nicht eine
Filterliste:

- eigener Dienst, NICHT das Backend: hier liegen keine Geheimnisse, keine
  Datenbank, keine Nutzerdaten;
- im Compose auf einem `internal`-Netz, also ohne Weg ins Internet;
- unprivilegierter Benutzer, `cap_drop: ALL`, `no-new-privileges`, Speicher-,
  CPU- und PID-Grenzen;
- jeder Lauf in einem frischen Temp-Verzeichnis, das danach gelöscht wird;
- harte Zeit- und Ausgabegrenze, begrenzte Parallelität.

Was damit NICHT abgedeckt ist: ein Ausbruch aus dem Container über eine
Kernel-Lücke. Wer das im Modell braucht, muss auf eine VM- oder
gVisor-Isolierung wechseln.
"""
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

TOKEN = os.getenv("RUNNER_TOKEN", "")
TIMEOUT_SECONDS = float(os.getenv("RUNNER_TIMEOUT", "30"))
MAX_OUTPUT_BYTES = int(os.getenv("RUNNER_MAX_OUTPUT", "65536"))
MAX_PARALLEL = int(os.getenv("RUNNER_MAX_PARALLEL", "2"))
ANSIBLE_BIN = os.getenv("ANSIBLE_PLAYBOOK_BIN", "ansible-playbook")

_slots = asyncio.Semaphore(MAX_PARALLEL)

app = FastAPI(title="IntLab Ansible Runner")


class RunRequest(BaseModel):
    playbook: str = Field(max_length=16_000)
    # Optionales Inventar; ohne Angabe läuft alles lokal im Container.
    inventory: str | None = Field(default=None, max_length=4_000)
    extra_vars: str | None = Field(default=None, max_length=1_000)
    check: bool = False
    # Stabile, undurchsichtige Kennung des Teilnehmers (vom Backend gesetzt).
    # Sie bestimmt das Arbeitsverzeichnis, das ZWISCHEN Läufen bestehen bleibt —
    # ohne das wäre die Idempotenz-Übung wertlos: Der zweite Lauf braucht den
    # Zustand des ersten. Gleichzeitig darf ein Teilnehmer den Zustand eines
    # anderen weder sehen noch erben, deshalb ein Verzeichnis je Kennung.
    workspace: str = Field(default="gast", max_length=64, pattern=r"^[A-Za-z0-9_-]+$")


class RunResult(BaseModel):
    rc: int
    output: str
    truncated: bool
    duration_ms: int
    timed_out: bool


DEFAULT_INVENTORY = "[lab]\nlabhost ansible_connection=local\n"

# Arbeitsverzeichnisse der Teilnehmer. Liegen im tmpfs (siehe docker-compose),
# sind also nach einem Neustart des Containers weg — das ist gewollt, es ist
# eine Übungsumgebung und kein Speicher.
WORKSPACE_ROOT = Path(os.getenv("RUNNER_WORKSPACE_ROOT", "/tmp/lab-workspaces"))
WORKSPACE_MAX_AGE_SECONDS = float(os.getenv("RUNNER_WORKSPACE_MAX_AGE", str(12 * 3600)))


def _workspace(kennung: str) -> Path:
    """Liefert das (dauerhafte) Arbeitsverzeichnis eines Teilnehmers.

    Räumt dabei alte Verzeichnisse weg: Das tmpfs ist klein, und ein Kurs von
    gestern muss nicht bis zum Neustart Platz belegen.
    """
    WORKSPACE_ROOT.mkdir(parents=True, exist_ok=True)
    jetzt = time.time()
    for eintrag in WORKSPACE_ROOT.iterdir():
        try:
            if eintrag.is_dir() and jetzt - eintrag.stat().st_mtime > WORKSPACE_MAX_AGE_SECONDS:
                shutil.rmtree(eintrag, ignore_errors=True)
        except OSError:
            pass
    verzeichnis = WORKSPACE_ROOT / kennung
    verzeichnis.mkdir(parents=True, exist_ok=True)
    return verzeichnis


def _clip(text: str) -> tuple[str, bool]:
    raw = text.encode("utf-8", "replace")
    if len(raw) <= MAX_OUTPUT_BYTES:
        return text, False
    gekappt = raw[:MAX_OUTPUT_BYTES].decode("utf-8", "ignore")
    return gekappt + "\n\n[Ausgabe gekürzt]", True


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "ansible": shutil.which(ANSIBLE_BIN) is not None}


@app.post("/run", response_model=RunResult)
async def run(req: RunRequest, x_runner_token: str = Header(default="")) -> RunResult:
    if not TOKEN or x_runner_token != TOKEN:
        raise HTTPException(status_code=401, detail="Runner-Token fehlt oder passt nicht")
    if not req.playbook.strip():
        raise HTTPException(status_code=422, detail="Playbook ist leer")

    async with _slots:
        arbeitsverzeichnis = Path(tempfile.mkdtemp(prefix="lab-"))
        begonnen = time.monotonic()
        timed_out = False
        try:
            (arbeitsverzeichnis / "playbook.yml").write_text(req.playbook, encoding="utf-8")
            (arbeitsverzeichnis / "inventory.ini").write_text(
                req.inventory or DEFAULT_INVENTORY, encoding="utf-8")

            # lab_dir zeigt auf das teilnehmereigene, dauerhafte Verzeichnis.
            # Die Übungs-Playbooks schreiben ausschließlich dorthin — mit einem
            # festen Pfad wie /tmp/uebung würden sich Teilnehmer gegenseitig den
            # Zustand überschreiben und die Idempotenz-Übung wäre beim zweiten
            # Menschen schon „nichts geändert".
            arbeitsplatz = _workspace(req.workspace)
            argumente = [ANSIBLE_BIN, "-i", "inventory.ini", "playbook.yml",
                         "--extra-vars", f"lab_dir={arbeitsplatz}"]
            if req.check:
                argumente.append("--check")
            if req.extra_vars:
                # Nach lab_dir gesetzt: eigene Angaben der Teilnehmenden gewinnen.
                argumente += ["--extra-vars", req.extra_vars]

            # Bewusst minimale Umgebung: nichts aus dem Runner-Prozess wird
            # durchgereicht, HOME und Temp liegen im Lauf-Verzeichnis.
            umgebung = {
                "PATH": os.getenv("PATH", "/usr/local/bin:/usr/bin:/bin"),
                "HOME": str(arbeitsverzeichnis),
                "TMPDIR": str(arbeitsverzeichnis),
                "LANG": "C.UTF-8",
                "ANSIBLE_LOCAL_TEMP": str(arbeitsverzeichnis / ".ansible-tmp"),
                "ANSIBLE_REMOTE_TEMP": str(arbeitsverzeichnis / ".ansible-tmp"),
                "ANSIBLE_RETRY_FILES_ENABLED": "0",
                "ANSIBLE_HOST_KEY_CHECKING": "False",
                "ANSIBLE_NOCOLOR": "1",
                "ANSIBLE_DEPRECATION_WARNINGS": "0",
                "ANSIBLE_SYSTEM_WARNINGS": "0",
                # Nur Interpreter-Rauschen unterdrücken (neuere Python-Versionen
                # melden SyntaxWarnings aus mitgelieferten Modulen). Ansibles
                # eigene Meldungen bleiben sichtbar — sie sind Lernstoff.
                "PYTHONWARNINGS": "ignore::SyntaxWarning",
            }

            prozess = await asyncio.create_subprocess_exec(
                *argumente,
                cwd=arbeitsverzeichnis,
                env=umgebung,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            try:
                ausgabe, _ = await asyncio.wait_for(prozess.communicate(), timeout=TIMEOUT_SECONDS)
                rc = prozess.returncode or 0
                text = ausgabe.decode("utf-8", "replace")
            except asyncio.TimeoutError:
                timed_out = True
                prozess.kill()
                await prozess.wait()
                rc = 124
                text = (f"Abgebrochen: Der Lauf hat die Zeitgrenze von "
                        f"{TIMEOUT_SECONDS:.0f} Sekunden überschritten.")

            text, gekappt = _clip(text)
            return RunResult(
                rc=rc,
                output=text,
                truncated=gekappt,
                duration_ms=int((time.monotonic() - begonnen) * 1000),
                timed_out=timed_out,
            )
        finally:
            shutil.rmtree(arbeitsverzeichnis, ignore_errors=True)
