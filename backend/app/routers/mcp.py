"""MCP-Endpunkt (Streamable HTTP, zustandslos): ein JSON-RPC-2.0-Objekt je POST,
Antwort als JSON, ohne SSE und ohne Sitzung. Authentifizierung nur per
persönlichem API-Token (`lgt_…`). Die Tools stehen in services/mcp_tools.py."""
# ponytail: bewusst ohne das mcp-SDK (~10 transitive Abhängigkeiten in der
# gepinnten requirements.lock); umsteigen, sobald Ressourcen, Prompts oder
# Streaming gebraucht werden.
import json

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.config import APP_VERSION
from app.database import get_db
from app.services.api_tokens import resolve_token
from app.services.content_editor import EditorError
from app.services.mcp_tools import TOOLS
from app.services.ratelimit import rate_limit

router = APIRouter(tags=["mcp"])

PROTOCOL_VERSIONS = ("2025-06-18", "2025-03-26")
INSTRUCTIONS = ("Lehrgänge der Schulungsplattform als Entwurf erstellen und bearbeiten. Zuerst "
                "get_authoring_guide aufrufen; vor Änderungen an einem Modul get_module und dessen "
                "version als base_version an save_module übergeben.")
_TYPES = {"string": str, "object": dict, "array": list, "integer": int, "boolean": bool}


async def _raw_body(request: Request) -> bytes:
    return await request.body()


def _result(id_, result) -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": id_, "result": result})


def _error(id_, code: int, message: str, status: int = 200) -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}},
                        status_code=status)


def _bad_args(schema: dict, args) -> str | None:
    """Prüft nur die oberste Ebene (Pflichtfelder, Typen, unbekannte Felder);
    den Modulinhalt prüfen ModuleIn und validate_module."""
    if not isinstance(args, dict):
        return "arguments muss ein Objekt sein"
    props = schema["properties"]
    for name in schema["required"]:
        if name not in args:
            return f"Pflichtargument fehlt: {name}"
    for name, value in args.items():
        if name not in props:
            return f"Unbekanntes Argument: {name}"
        expected = _TYPES[props[name]["type"]]
        if not isinstance(value, expected) or (expected is int and isinstance(value, bool)):
            return f"Argument {name} muss vom Typ {props[name]['type']} sein"
    return None


def _call_tool(db: Session, trainer: dict, id_, params: dict) -> JSONResponse:
    name = params.get("name")
    tool = TOOLS.get(name) if isinstance(name, str) else None
    if tool is None:
        return _error(id_, -32602, f"Unbekanntes Tool: {params.get('name')}")
    args = params.get("arguments") or {}
    if problem := _bad_args(tool.input_schema, args):
        return _error(id_, -32602, problem)
    try:
        out = tool.handler(db, trainer, args)
    except ValidationError as e:
        return _error(id_, -32602,
                       "; ".join(f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors()))
    except EditorError as e:
        return _result(id_, {"content": [{"type": "text", "text": e.message}], "isError": True})
    return _result(id_, {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False, default=str)}]})


@router.post("/mcp", dependencies=[Depends(rate_limit(120, 60))])
def mcp(request: Request, body: bytes = Depends(_raw_body), db: Session = Depends(get_db)):
    scheme, _, raw = request.headers.get("authorization", "").partition(" ")
    trainer = resolve_token(db, raw) if scheme.lower() == "bearer" and raw.startswith("lgt_") else None
    if trainer is None:
        return Response(status_code=401, headers={"WWW-Authenticate": "Bearer"})

    try:
        msg = json.loads(body)
    except ValueError:
        return _error(None, -32700, "Parse error", status=400)
    if not isinstance(msg, dict) or not isinstance(msg.get("method"), str):
        return _error(None, -32600, "Invalid Request: genau ein JSON-RPC-Objekt erwartet", status=400)
    if "id" not in msg:
        return Response(status_code=202)  # Benachrichtigung (z.B. notifications/initialized)

    id_, method, params = msg["id"], msg["method"], msg.get("params") or {}
    if not isinstance(params, dict):
        return _error(id_, -32602, "params muss ein Objekt sein")
    if method == "initialize":
        version = params.get("protocolVersion")
        return _result(id_, {
            "protocolVersion": version if version in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "lehrgang", "version": APP_VERSION},
            "instructions": INSTRUCTIONS})
    if method == "ping":
        return _result(id_, {})
    if method == "tools/list":
        return _result(id_, {"tools": [{"name": n, "description": t.description, "inputSchema": t.input_schema}
                                       for n, t in TOOLS.items()]})
    if method == "tools/call":
        return _call_tool(db, trainer, id_, params)
    return _error(id_, -32601, f"Methode nicht unterstützt: {method}")
