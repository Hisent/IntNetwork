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
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.models.participant import Participant
from app.services.deps import get_participant
from app.services.ratelimit import rate_limit

router = APIRouter(prefix="/lab", tags=["lab"])

ABFRAGE_INTERVALL = 0.15


class LabRunRequest(BaseModel):
    playbook: str = Field(max_length=16_000)
    inventory: str | None = Field(default=None, max_length=4_000)
    extra_vars: str | None = Field(default=None, max_length=1_000)
    check: bool = False


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


@router.get("/status")
def lab_status(_p: Participant = Depends(get_participant)) -> dict:
    warteschlange = _queue()
    return {"enabled": bool(warteschlange and (warteschlange / "in").is_dir())}


@router.post("/run", response_model=LabRunResponse,
             dependencies=[Depends(rate_limit(20, 60))])
async def lab_run(data: LabRunRequest,
                  teilnehmer: Participant = Depends(get_participant)) -> LabRunResponse:
    warteschlange = _queue()
    if not warteschlange or not (warteschlange / "in").is_dir():
        raise HTTPException(status_code=503, detail="Das Lab ist auf diesem Server nicht aktiviert.")
    if not data.playbook.strip():
        raise HTTPException(status_code=422, detail="Das Playbook ist leer.")

    auftrags_id = uuid.uuid4().hex
    auftrag = {**data.model_dump(), "workspace": _workspace_kennung(teilnehmer)}
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
