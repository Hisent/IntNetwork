"""Fehlerberichte aus dem Browser (ErrorBoundary, window.onerror,
unhandledrejection) -- landen nur im Backend-Log, kein externer Dienst.

Ohne Anmeldung (Fehler passieren auch vor Login/Beitritt), daher eng begrenzt:
Rate-Limit je IP, feste Feldlängen (zu lang = 422), keine Speicherung. Das
Frontend schickt bewusst keine Namen, Tokens oder Request-Inhalte mit
(frontend/src/lib/errorReport.ts); repr() hält jeden Bericht auf einer Logzeile.
Der Körper wird VOR dem JSON-Parsen auf MAX_BODY Bytes begrenzt (Content-Length
und gezählt beim Lesen) -- sonst parste die API bis zur nginx-Grenze (1 MB).
"""
import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError

from app.services.ratelimit import rate_limit

router = APIRouter(tags=["client-errors"])
logger = logging.getLogger(__name__)


class ClientError(BaseModel):
    message: str = Field(max_length=500)
    stack: str = Field("", max_length=4000)
    route: str = Field("", max_length=300)
    version: str = Field("", max_length=40)


# Größter gültiger Bericht: 4840 Zeichen, auch komplett als JSON-Escape (6 Byte je Zeichen) knapp 30 KB.
MAX_BODY = 32 * 1024


async def _bounded_body(request: Request) -> bytes:
    too_large = HTTPException(status_code=413, detail="Fehlerbericht zu groß")
    try:
        declared = int(request.headers.get("content-length", 0))
    except ValueError:
        raise HTTPException(status_code=400, detail="Ungültige Content-Length") from None
    if declared > MAX_BODY:
        raise too_large
    body = b""
    async for chunk in request.stream():  # Content-Length kann fehlen (chunked) oder lügen
        body += chunk
        if len(body) > MAX_BODY:
            raise too_large
    return body


@router.post("/client-errors", status_code=204, dependencies=[Depends(rate_limit(10, 60))])
async def report_client_error(request: Request) -> Response:
    try:
        data = ClientError.model_validate_json(await _bounded_body(request))
    except ValidationError as e:
        raise RequestValidationError(e.errors(include_url=False)) from None
    logger.warning("Client-Fehler version=%r route=%r message=%r stack=%r",
                   data.version, data.route, data.message, data.stack)
    return Response(status_code=204)
