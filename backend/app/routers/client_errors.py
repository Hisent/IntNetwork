"""Fehlerberichte aus dem Browser (ErrorBoundary, window.onerror,
unhandledrejection) -- landen nur im Backend-Log, kein externer Dienst.

Ohne Anmeldung (Fehler passieren auch vor Login/Beitritt), daher eng begrenzt:
Rate-Limit je IP, feste Feldlängen (zu lang = 422), keine Speicherung. Das
Frontend schickt bewusst keine Namen, Tokens oder Request-Inhalte mit
(frontend/src/lib/errorReport.ts); repr() hält jeden Bericht auf einer Logzeile.
ponytail: der Rohkörper wird vor der Längenprüfung gelesen; die Obergrenze
dafür setzt nginx (client_max_body_size, Standard 1 MB). Eigene Byte-Grenze
erst, wenn das Backend ohne den nginx davor erreichbar ist.
"""
import logging

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, Field

from app.services.ratelimit import rate_limit

router = APIRouter(tags=["client-errors"])
logger = logging.getLogger(__name__)


class ClientError(BaseModel):
    message: str = Field(max_length=500)
    stack: str = Field("", max_length=4000)
    route: str = Field("", max_length=300)
    version: str = Field("", max_length=40)


@router.post("/client-errors", status_code=204, dependencies=[Depends(rate_limit(10, 60))])
def report_client_error(data: ClientError) -> Response:
    logger.warning("Client-Fehler version=%r route=%r message=%r stack=%r",
                   data.version, data.route, data.message, data.stack)
    return Response(status_code=204)
