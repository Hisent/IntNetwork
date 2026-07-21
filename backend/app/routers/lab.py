"""Ansible-Lab: leitet Teilnehmer-Playbooks an den Runner-Dienst weiter.

Das Backend fuehrt selbst NICHTS aus. Es kennt die Geheimnisse (SECRET_KEY,
Datenbank) und waere damit das falsche Ziel fuer fremden Code — die Ausfuehrung
liegt bewusst im separaten Runner-Container (siehe runner/app.py).

Ohne konfigurierten Runner ist das Lab schlicht aus: die Endpunkte antworten
mit 503 und das Widget zeigt einen Hinweis. Der Kurs bleibt benutzbar.
"""
import hashlib
import hmac

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.config import settings
from app.models.participant import Participant
from app.services.deps import get_participant
from app.services.ratelimit import rate_limit

router = APIRouter(prefix="/lab", tags=["lab"])


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


@router.get("/status")
def lab_status(_p: Participant = Depends(get_participant)) -> dict:
    """Sagt dem Widget, ob es einen Runner gibt — ohne ihn zu kontaktieren."""
    return {"enabled": bool(settings.lab_runner_url and settings.lab_runner_token)}


def _workspace_kennung(teilnehmer: Participant) -> str:
    """Stabile, undurchsichtige Kennung für das Arbeitsverzeichnis im Runner.

    Der Runner soll Läufe desselben Menschen wiedererkennen (die Idempotenz-
    Übung braucht den Zustand des vorherigen Laufs), aber weder Namen noch IDs
    erfahren. Deshalb ein HMAC über die Teilnehmer-ID mit dem SECRET_KEY.
    """
    roh = hmac.new(settings.secret_key.encode(), f"lab:{teilnehmer.id}".encode(),
                   hashlib.sha256).hexdigest()
    return roh[:32]


@router.post("/run", response_model=LabRunResponse,
             dependencies=[Depends(rate_limit(20, 60))])
async def lab_run(data: LabRunRequest, teilnehmer: Participant = Depends(get_participant)) -> LabRunResponse:
    if not (settings.lab_runner_url and settings.lab_runner_token):
        raise HTTPException(status_code=503, detail="Das Lab ist auf diesem Server nicht aktiviert.")
    if not data.playbook.strip():
        raise HTTPException(status_code=422, detail="Das Playbook ist leer.")

    # Etwas mehr Geduld als der Runner selbst: der bricht nach seiner eigenen
    # Zeitgrenze ab und liefert dann noch eine Antwort, die wir durchreichen wollen.
    zeitlimit = settings.lab_timeout_seconds + 10
    try:
        async with httpx.AsyncClient(timeout=zeitlimit) as client:
            antwort = await client.post(
                f"{settings.lab_runner_url.rstrip('/')}/run",
                json={**data.model_dump(), "workspace": _workspace_kennung(teilnehmer)},
                headers={"X-Runner-Token": settings.lab_runner_token},
            )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Der Lab-Dienst hat nicht rechtzeitig geantwortet.")
    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="Der Lab-Dienst ist gerade nicht erreichbar.")

    if antwort.status_code >= 400:
        raise HTTPException(status_code=502,
                            detail=f"Der Lab-Dienst meldet einen Fehler ({antwort.status_code}).")
    return LabRunResponse(**antwort.json())
