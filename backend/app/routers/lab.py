"""Ansible-Lab: reicht Playbooks über eine Datei-Warteschlange an den Runner.

Warum Dateien statt HTTP (Stand 2026-07-21):
Der Runner lief zuerst als HTTP-Dienst in einem internen Docker-Netz. Auf dem
Zielsystem (Coolify) hängt aber jeder Dienst zusätzlich im Projekt-Netz, und
das ist nicht intern — aus dem Runner heraus waren Internet, Datenbank und
Backend erreichbar. Jetzt hat der Runner-Container `network_mode: none`, also
gar kein Netz; Auftrag und Ergebnis laufen über ein gemeinsames Volume.

Das Backend führt weiterhin selbst nichts aus. Es kennt SECRET_KEY und die
Datenbank und wäre das falsche Ziel für fremden Code.

Ohne konfiguriertes Warteschlangen-Verzeichnis ist das Lab schlicht aus: die
Endpunkte antworten mit 503 und das Widget zeigt einen Hinweis.
"""
import asyncio
import hashlib
import hmac
import json
import os
import re
import uuid
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.models.participant import Participant
from app.services.deps import get_participant
from app.services.ratelimit import rate_limit

router = APIRouter(prefix="/lab", tags=["lab"])

ABFRAGE_INTERVALL = 0.15

# Grenzen fuer die Werkzeug-Arten (openssl/git). Gelten zusaetzlich im Runner,
# der dem Backend nicht vertraut — hier pruefen wir frueh, damit die
# Teilnehmerin eine verstaendliche 422-Meldung bekommt statt rc=2 vom Runner.
MAX_BEFEHLE = 6
MAX_BEFEHLSLAENGE = 512
MAX_DATEIEN = 10
MAX_DATEIGROESSE = 32_768
DATEINAME_MUSTER = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


class LabRunRequest(BaseModel):
    kind: Literal["ansible", "openssl", "git"] = "ansible"
    # Ansible-Felder: bleiben unveraendert optional (playbook wird fuer
    # kind="ansible" im Router auf Pflicht und Nicht-Leere geprueft).
    playbook: str | None = Field(default=None, max_length=16_000)
    inventory: str | None = Field(default=None, max_length=4_000)
    extra_vars: str | None = Field(default=None, max_length=1_000)
    check: bool = False
    # Werkzeug-Felder (openssl/git): siehe _validiere_werkzeug_auftrag.
    files: dict[str, str] | None = None
    commands: list[str] | None = None


class LabRunResponse(BaseModel):
    rc: int
    output: str
    truncated: bool
    duration_ms: int
    timed_out: bool


def _queue() -> Path | None:
    """Verzeichnis der Warteschlange, oder None wenn das Lab aus ist."""
    if not settings.lab_queue_dir:
        return None
    return Path(settings.lab_queue_dir)


def _workspace_kennung(teilnehmer: Participant) -> str:
    """Stabile, undurchsichtige Kennung für das Arbeitsverzeichnis im Runner.

    Der Runner soll Läufe desselben Menschen wiedererkennen — die Idempotenz-
    Übung braucht den Zustand des vorherigen Laufs — aber weder Namen noch IDs
    erfahren. Deshalb ein HMAC über die Teilnehmer-ID mit dem SECRET_KEY.
    """
    roh = hmac.new(settings.secret_key.encode(), f"lab:{teilnehmer.id}".encode(),
                   hashlib.sha256).hexdigest()
    return roh[:32]


def _validiere_werkzeug_auftrag(data: LabRunRequest) -> None:
    """Prueft commands/files fuer kind in (openssl, git). Wirft 422 mit
    verstaendlicher deutscher Meldung, sobald eine Grenze verletzt ist."""
    if not data.commands:
        raise HTTPException(status_code=422, detail="Es muss mindestens ein Befehl angegeben werden.")
    if len(data.commands) > MAX_BEFEHLE:
        raise HTTPException(
            status_code=422,
            detail=f"Hoechstens {MAX_BEFEHLE} Befehle je Lauf sind erlaubt.")
    for befehl in data.commands:
        if len(befehl) > MAX_BEFEHLSLAENGE:
            raise HTTPException(
                status_code=422,
                detail=f"Ein Befehl darf hoechstens {MAX_BEFEHLSLAENGE} Zeichen lang sein.")
    if data.files:
        if len(data.files) > MAX_DATEIEN:
            raise HTTPException(
                status_code=422,
                detail=f"Hoechstens {MAX_DATEIEN} Dateien je Lauf sind erlaubt.")
        for name, inhalt in data.files.items():
            if not DATEINAME_MUSTER.match(name):
                raise HTTPException(
                    status_code=422,
                    detail=f"Der Dateiname '{name}' ist nicht erlaubt "
                           "(nur Buchstaben, Ziffern, Punkt, Unter- und Bindestrich).")
            if len(inhalt.encode("utf-8")) > MAX_DATEIGROESSE:
                raise HTTPException(
                    status_code=422,
                    detail=f"Die Datei '{name}' ist groesser als {MAX_DATEIGROESSE // 1024} KB.")


def _auftragsfelder(data: LabRunRequest) -> dict:
    """Prueft die Anfrage und gibt genau die Felder zurueck, die zur Art
    gehoeren. Felder der jeweils anderen Art werden ignoriert statt abgelehnt —
    aber auch nicht in den Auftrag uebernommen (kein `playbook: null` bei
    einem openssl-Auftrag)."""
    if data.kind == "ansible":
        if not data.playbook or not data.playbook.strip():
            raise HTTPException(status_code=422, detail="Das Playbook ist leer.")
        return {
            "playbook": data.playbook,
            "inventory": data.inventory,
            "extra_vars": data.extra_vars,
            "check": data.check,
        }
    # kind in (openssl, git): gleiche Form, gleiche Grenzen.
    _validiere_werkzeug_auftrag(data)
    felder: dict = {"commands": data.commands}
    if data.files:
        felder["files"] = data.files
    return felder


@router.get("/status")
def lab_status(_p: Participant = Depends(get_participant)) -> dict:
    warteschlange = _queue()
    aktiv = bool(warteschlange and (warteschlange / "in").is_dir())
    # Das Backend kennt RUNNER_KINDS des Runners nicht — lab_kinds ist eine
    # eigene, separat gepflegte Einstellung (siehe config.py).
    return {"enabled": aktiv, "kinds": settings.lab_kinds_list if aktiv else []}


@router.post("/run", response_model=LabRunResponse,
             dependencies=[Depends(rate_limit(20, 60))])
async def lab_run(data: LabRunRequest,
                  teilnehmer: Participant = Depends(get_participant)) -> LabRunResponse:
    warteschlange = _queue()
    if not warteschlange or not (warteschlange / "in").is_dir():
        raise HTTPException(status_code=503, detail="Das Lab ist auf diesem Server nicht aktiviert.")
    # LAB_KINDS ist nicht nur ein Hinweis fuer die Oberflaeche, sondern eine
    # Freigabe: Ohne diese Pruefung liesse sich per API eine Art nutzen, die der
    # Betrieb bewusst nicht anbieten wollte — es genuegte, dass der Runner sie
    # freigegeben hat. Die beiden Listen werden getrennt gepflegt (kein Netzweg
    # zwischen den Diensten, siehe config.py), also muss jede Seite ihre eigene
    # durchsetzen.
    if data.kind not in settings.lab_kinds_list:
        raise HTTPException(
            status_code=403,
            detail=f"Die Lab-Art '{data.kind}' ist auf diesem Server nicht freigegeben.")

    felder = _auftragsfelder(data)
    auftrags_id = uuid.uuid4().hex
    auftrag = {"kind": data.kind, **felder, "workspace": _workspace_kennung(teilnehmer)}
    eingang = warteschlange / "in" / f"{auftrags_id}.json"
    ausgang = warteschlange / "out" / f"{auftrags_id}.json"

    try:
        vorlaeufig = eingang.with_suffix(".json.tmp")
        vorlaeufig.write_text(json.dumps(auftrag), encoding="utf-8")
        # Atomar umbenennen: Der Runner darf nie eine halb geschriebene Datei sehen.
        os.replace(vorlaeufig, eingang)
    except OSError as err:
        # Ursache mitgeben: Ob das Volume fehlt, voll ist oder die Rechte nicht
        # stimmen, steht nur im OSError — genau das braucht die Fehlersuche.
        raise HTTPException(
            status_code=502, detail="Der Lab-Dienst ist gerade nicht erreichbar.") from err

    # Etwas mehr Geduld als der Runner selbst: Der bricht nach seiner eigenen
    # Zeitgrenze ab und schreibt dann noch ein Ergebnis, das wir ausliefern wollen.
    frist = asyncio.get_event_loop().time() + settings.lab_timeout_seconds + 15
    while asyncio.get_event_loop().time() < frist:
        if ausgang.exists():
            try:
                ergebnis = json.loads(ausgang.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                await asyncio.sleep(ABFRAGE_INTERVALL)
                continue
            ausgang.unlink(missing_ok=True)
            return LabRunResponse(**ergebnis)
        await asyncio.sleep(ABFRAGE_INTERVALL)

    # Nichts gekommen: eigenen Auftrag zurückziehen, damit er nicht später noch
    # ins Leere läuft, und ehrlich melden.
    eingang.unlink(missing_ok=True)
    raise HTTPException(status_code=504, detail="Der Lab-Dienst hat nicht rechtzeitig geantwortet.")
