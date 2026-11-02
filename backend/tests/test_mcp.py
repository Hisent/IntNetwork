import json
import uuid

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.workshop import Workshop


def _login(c, email, password):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": email, "password": password}).json()["access_token"]}


def _token(c, h, name="MCP"):
    return c.post("/api/trainer/api-tokens", json={"name": name}, headers=h).json()["token"]


def _new_trainer_token(c):
    admin = _login(c, "trainer@test.de", "trainerpass1")
    email = f"mcp-{uuid.uuid4().hex[:8]}@test.de"
    assert c.post("/api/trainer/accounts", json={"email": email, "name": email, "password": "pass1234"},
                  headers=admin).status_code == 200
    return _token(c, _login(c, email, "pass1234"))


def _rpc(c, token, method, params=None, id=1):
    body = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        body["params"] = params
    if id is not None:
        body["id"] = id
    return c.post("/api/mcp", json=body, headers={"Authorization": f"Bearer {token}"})


def _call(c, token, tool, **args):
    """tools/call → (Ergebnis-Objekt, isError)."""
    r = _rpc(c, token, "tools/call", {"name": tool, "arguments": args})
    assert r.status_code == 200 and "result" in r.json(), r.text
    res = r.json()["result"]
    text = res["content"][0]["text"]
    return (text if res.get("isError") else json.loads(text)), bool(res.get("isError"))


def _ok(c, token, tool, **args):
    out, err = _call(c, token, tool, **args)
    assert not err, out
    return out


def _ws(c, token):
    key = f"mcp-{uuid.uuid4().hex[:8]}"
    _ok(c, token, "create_workshop", key=key, title_de="Lehrgang", title_en="Course",
        summary_de="S", summary_en="S", theme="network")
    return key


def _example(c, token):
    return _ok(c, token, "get_authoring_guide")["example_module"]


def test_ohne_token_401():
    with TestClient(app) as c:
        for headers in ({}, {"Authorization": "Bearer lgt_unbekannt"}, {"Authorization": "Bearer kaputt"}):
            r = c.post("/api/mcp", content=b"kein json", headers=headers)
            assert r.status_code == 401 and r.headers["www-authenticate"] == "Bearer"
        # Ein normales Login-JWT ist kein API-Token.
        jwt = _login(c, "trainer@test.de", "trainerpass1")
        assert c.post("/api/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                      headers=jwt).status_code == 401


def test_get_405():
    with TestClient(app) as c:
        assert c.get("/api/mcp").status_code == 405


def test_initialize_und_tools_list():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        r = _rpc(c, token, "initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                          "clientInfo": {"name": "t", "version": "1"}})
        res = r.json()["result"]
        assert r.json()["id"] == 1 and res["protocolVersion"] == "2025-03-26"
        assert res["capabilities"] == {"tools": {}}
        assert _rpc(c, token, "initialize", {"protocolVersion": "1999-01-01"}).json()["result"][
            "protocolVersion"] == "2025-06-18"
        assert _rpc(c, token, "ping").json()["result"] == {}

        tools = _rpc(c, token, "tools/list").json()["result"]["tools"]
        assert {t["name"] for t in tools} == {
            "get_authoring_guide", "list_workshops", "get_workshop", "create_workshop", "update_workshop",
            "get_module", "save_module", "restore_module", "delete_module"}
        assert all(t["description"] and t["inputSchema"]["type"] == "object" for t in tools)


def test_notification_202():
    with TestClient(app) as c:
        r = _rpc(c, _new_trainer_token(c), "notifications/initialized", id=None)
        assert r.status_code == 202 and r.content == b""


def test_unbekannte_methode_32601():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        assert _rpc(c, token, "resources/list").json()["error"]["code"] == -32601
        r = c.post("/api/mcp", content=b"{kaputt", headers={"Authorization": f"Bearer {token}"})
        assert r.json()["error"]["code"] == -32700
        assert _rpc(c, token, "tools/call", {"name": "gibt_es_nicht", "arguments": {}}).json()[
            "error"]["code"] == -32602
        # Pflichtargument fehlt / falscher Typ
        assert _rpc(c, token, "tools/call", {"name": "get_module", "arguments": {}}).json()[
            "error"]["code"] == -32602
        assert _rpc(c, token, "tools/call", {"name": "get_module", "arguments": {"key": 1}}).json()[
            "error"]["code"] == -32602


def test_create_workshop_ist_entwurf():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        key = _ws(c, token)
        mine = [w for w in _ok(c, token, "list_workshops") if w["key"] == key]
        assert len(mine) == 1 and mine[0]["status"] == "draft" and mine[0]["editable"] is True
        _, err = _call(c, token, "create_workshop", key=key, title_de="X", title_en="X",
                       summary_de="S", summary_en="S", theme="network")
        assert err


def test_save_module_legt_an_und_liefert_version():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        ws = _ws(c, token)
        mod = f"{ws}-m1"
        out = _ok(c, token, "save_module", key=mod, workshop_key=ws, module=_example(c, token))
        got = _ok(c, token, "get_module", key=mod)
        assert out["version"] == got["version"] and got["workshop_key"] == ws and got["order"] == 1
        assert [b["type"] for b in got["blocks"]] == ["text", "check"] and len(got["quiz"]) == 1

        # Zweites Modul hängt sich hinten an; Abschnitte setzen die Reihenfolge.
        _ok(c, token, "save_module", key=f"{ws}-m2", workshop_key=ws, module=_example(c, token))
        _ok(c, token, "update_workshop", key=ws, title_de="Neu", sections=[
            {"title_de": "A", "title_en": "A", "modules": [f"{ws}-m2", mod]}])
        view = _ok(c, token, "get_workshop", key=ws)
        assert view["title_de"] == "Neu" and view["sections"][0]["modules"] == [f"{ws}-m2", mod]

        _ok(c, token, "delete_module", key=f"{ws}-m2")
        assert "existiert nicht" in _call(c, token, "get_module", key=f"{ws}-m2")[0]


def test_save_module_ohne_base_version_auf_bestehendes_modul_ist_fehler():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        ws = _ws(c, token)
        mod = f"{ws}-m1"
        _ok(c, token, "save_module", key=mod, workshop_key=ws, module=_example(c, token))
        before = _ok(c, token, "get_module", key=mod)
        text, err = _call(c, token, "save_module", key=mod, workshop_key=ws,
                          module={**_example(c, token), "title_de": "Überschrieben"})
        assert err and text == ("Modul existiert bereits. Erst get_module aufrufen und dessen "
                                "version als base_version mitgeben.")
        assert _ok(c, token, "get_module", key=mod) == before


def test_save_module_validierungsfehler_nennt_block():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        ws = _ws(c, token)
        diagram = {"uid": "ablauf", "type": "diagram", "payload": {
            "kind": "sequence", "actors": [{"id": "a", "label": "x" * 40}, {"id": "b", "label": "B"}],
            "messages": [{"from": "a", "to": "b", "label": "hallo"}]}}
        text, err = _call(c, token, "save_module", key=f"{ws}-m1", workshop_key=ws,
                          module={**_example(c, token), "blocks": [diagram]})
        assert err and "ablauf" in text and "actors[0]" in text
        # Kein halb angelegtes Modul bleibt zurück.
        assert "existiert nicht" in _call(c, token, "get_module", key=f"{ws}-m1")[0]


def test_save_module_veraltete_version_konflikttext():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        ws = _ws(c, token)
        mod = f"{ws}-m1"
        first = _ok(c, token, "save_module", key=mod, workshop_key=ws, module=_example(c, token))
        second = _ok(c, token, "save_module", key=mod, workshop_key=ws, base_version=first["version"],
                     module={**_example(c, token), "title_de": "Zwei"})
        assert second["version"] != first["version"]
        text, err = _call(c, token, "save_module", key=mod, workshop_key=ws, base_version=first["version"],
                          module={**_example(c, token), "title_de": "Drei"})
        assert err and text == ("Modul wurde inzwischen geändert. Erst get_module aufrufen, dann "
                                "Änderungen auf der neuen version erneut anwenden.")
        assert _ok(c, token, "get_module", key=mod)["title_de"] == "Zwei"
        _ok(c, token, "restore_module", key=mod)
        assert _ok(c, token, "get_module", key=mod)["title_de"] != "Zwei"


def test_fremder_lehrgang_rechtefehler():
    with TestClient(app) as c:
        owner, other = _new_trainer_token(c), _new_trainer_token(c)
        ws = _ws(c, owner)
        mod = f"{ws}-m1"
        v = _ok(c, owner, "save_module", key=mod, workshop_key=ws, module=_example(c, owner))["version"]
        # Entwurf ist für den Kollegen unsichtbar.
        assert all(w["key"] != ws for w in _ok(c, other, "list_workshops"))
        assert _call(c, other, "get_workshop", key=ws) == (f"Workshop/Modul ‚{ws}‘ existiert nicht.", True)
        assert _call(c, other, "get_module", key=mod) == (f"Workshop/Modul ‚{mod}‘ existiert nicht.", True)
        # Veröffentlichter fremder Lehrgang: sichtbar, aber nicht bearbeitbar.
        with SessionLocal() as db:
            db.get(Workshop, ws).status = "published"
            db.commit()
        assert _ok(c, other, "get_module", key=mod)["version"] == v
        denied = f"Lehrgang ‚{ws}‘ gehört einem anderen Trainer."
        assert _call(c, other, "save_module", key=mod, workshop_key=ws, base_version=v,
                     module=_example(c, other)) == (denied, True)
        assert _call(c, other, "save_module", key=f"{ws}-m9", workshop_key=ws,
                     module=_example(c, other)) == (denied, True)
        assert _call(c, other, "update_workshop", key=ws, title_de="X") == (denied, True)
        assert _call(c, other, "delete_module", key=mod) == (denied, True)
        assert _call(c, other, "restore_module", key=mod) == (denied, True)
        # Mitgelieferte Lehrgänge gehören den Admins.
        assert _call(c, other, "update_workshop", key="network", title_de="X") == (
            "Lehrgang ‚network‘ gehört einem anderen Trainer.", True)


def test_kein_tool_veroeffentlicht():
    with TestClient(app) as c:
        tools = _rpc(c, _new_trainer_token(c), "tools/list").json()["result"]["tools"]
        assert not [t["name"] for t in tools if "publish" in t["name"]]


def test_audit_eintrag_via_mcp():
    with TestClient(app) as c:
        token = _new_trainer_token(c)
        ws = _ws(c, token)
        _ok(c, token, "save_module", key=f"{ws}-m1", workshop_key=ws, module=_example(c, token))
        with SessionLocal() as db:
            rows = db.query(AuditLog).filter(AuditLog.target.in_([f"workshop:{ws}", f"module:{ws}-m1"])).all()
            assert {r.action for r in rows} == {"workshop.create", "content.create", "content.save"}
            assert all(r.detail == "via=mcp, token=MCP" for r in rows)
