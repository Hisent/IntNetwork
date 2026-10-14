"""Fehlermeldungen zweisprachig: Deutsch bleibt Standard und unverändert, mit
Accept-Language: en liefert der HTTPException-Handler die englische Fassung."""
import ast
import pathlib

from fastapi.testclient import TestClient

from app.main import app
from app.services import messages
from tests.test_polls import MOD, _course, _join, _trainer

EN = {"Accept-Language": "en"}


def _template(node: ast.expr) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value if isinstance(v, ast.Constant) else "{}" for v in node.values)
    return None  # Variable (z. B. str(e)) — deren Quelle prüft der Test selbst


def test_jede_detail_meldung_hat_eine_englische_fassung():
    """Neue Meldung ohne Übersetzung -> dieser Test schlägt fehl (statt still deutsch zu bleiben)."""
    app_dir = pathlib.Path(__file__).resolve().parents[1] / "app"
    missing = []
    for path in [*app_dir.glob("routers/*.py"), *app_dir.glob("services/*.py")]:
        if path.name == "block_validation.py":  # Autoren-Prüftexte, siehe messages.py
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if not isinstance(node, ast.Call):
                continue
            name = getattr(node.func, "id", None) or getattr(node.func, "attr", None)
            texts = [k.value for k in node.keywords if k.arg == "detail"] if name == "HTTPException" else []
            if name == "ValueError" and path.name == "poll_tally.py":  # landet per str(e) im detail
                texts = node.args[:1]
            for text in filter(None, map(_template, texts)):
                if text not in messages.EN:
                    missing.append(f"{path.name}: {text}")
    assert not missing, missing
    assert "Passkey-Anmeldung fehlgeschlagen" in messages.EN  # _LOGIN_FEHLER (Konstante, nicht per AST erfasst)


def test_to_en_setzt_platzhalter_ein_und_uebersetzt_verschachtelt():
    assert messages.to_en("Unbekannte Voraussetzung: vlan") == "Unknown prerequisite: vlan"
    assert messages.to_en("Die Datei 'a b.yml' ist groesser als 64 KB.") == "The file 'a b.yml' is larger than 64 KB."
    assert messages.to_en("Unbekannter Text") == "Unbekannter Text"
    assert messages.wants_en("en-US,en;q=0.9") and not messages.wants_en("de-DE,en;q=0.8")
    assert not messages.wants_en(None)


def test_endpunkte_antworten_in_der_angefragten_sprache():
    with TestClient(app) as c:
        # Teilnehmer-Beitritt
        r = c.post("/api/join", json={"code": "XXXXXX", "name": "Ada"})
        assert (r.status_code, r.json()["detail"]) == (404, "Kurs-Code ungültig")
        r = c.post("/api/join", json={"code": "XXXXXX", "name": "Ada"}, headers=EN)
        assert (r.status_code, r.json()["detail"]) == (404, "Invalid course code")
        # Trainer-Login
        bad = {"email": "trainer@test.de", "password": "falsch-falsch"}
        assert c.post("/api/trainer/login", json=bad).json()["detail"] == "Login fehlgeschlagen"
        assert c.post("/api/trainer/login", json=bad, headers={"Accept-Language": "en-GB,de"}).json()["detail"] \
            == "Login failed"
        # Rollenprüfung (Dependency) und Platzhalter-Meldung aus poll_tally über str(e)
        h = _trainer(c)
        code, cid = _course(c, h, "Sprachen")
        p = _join(c, code, "Sprach-Susi")
        assert c.get("/api/courses", headers={**p, **EN}).json()["detail"] == "Trainers only"
        poll = c.post(f"/api/trainer/courses/{cid}/poll", headers=h, json={
            "module_key": MOD, "source": "adhoc", "kind": "text", "prompt": "Was?"}).json()
        vote = {"poll_id": poll["id"], "choice": " "}
        assert c.post(f"/api/modules/{MOD}/poll/vote", headers=p, json=vote).json()["detail"] \
            == "Antwort leer oder länger als 280 Zeichen"
        assert c.post(f"/api/modules/{MOD}/poll/vote", headers={**p, **EN}, json=vote).json()["detail"] \
            == "Answer empty or longer than 280 characters"
