import uuid

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.workshop import Workshop
from tests.conftest import put_module


def _login(c, email, password):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": email, "password": password}).json()["access_token"]}


def _admin(c):
    return _login(c, "trainer@test.de", "trainerpass1")


def _new_trainer(c, admin):
    email = f"t-{uuid.uuid4().hex[:8]}@test.de"
    r = c.post("/api/trainer/accounts", json={"email": email, "name": "Kollege " + email[:10],
                                              "password": "pass1234"}, headers=admin)
    assert r.status_code == 200
    return r.json()["id"], r.json()["name"], _login(c, email, "pass1234")


def _draft(c, admin, owner_id):
    """Entwurf direkt in der DB plus ein Modul darin (Admin darf alles anlegen)."""
    key = f"draft-{uuid.uuid4().hex[:8]}"
    with SessionLocal() as db:
        db.add(Workshop(key=key, title_de="Entwurf", title_en="Draft", summary_de="S", summary_en="S",
                        theme="network", sections=[], context=None,
                        status="draft", owner_trainer_id=owner_id))
        db.commit()
    mod = f"{key}-m1"
    r = c.post("/api/trainer/content/modules",
               json={"key": mod, "title_de": "Modul", "workshop_key": key}, headers=admin)
    assert r.status_code == 200, r.text
    return key, mod


def _body(title="Neu"):
    return {"title_de": title, "title_en": title, "order": 1, "prerequisites": [], "goals": [],
            "scenario_de": "", "scenario_en": "", "blocks": [], "quiz": []}


def _vlan_body(c, h):
    data = c.get("/api/trainer/content/modules/vlan", headers=h).json()
    return {k: data[k] for k in ("title_de", "title_en", "order", "prerequisites", "goals", "goals_en",
                                 "scenario_de", "scenario_en", "blocks", "quiz") if k in data}


def test_trainer_kann_mitgeliefertes_modul_nicht_speichern():
    with TestClient(app) as c:
        admin = _admin(c)
        _, _, trainer = _new_trainer(c, admin)
        body = _vlan_body(c, admin)
        url = "/api/trainer/content/modules/vlan"
        r = put_module(c, url, json=body, headers=trainer)
        assert r.status_code == 403
        assert "gehört einem anderen Trainer" in r.json()["detail"]
        assert c.post(f"{url}/reseed", headers=trainer).status_code == 403
        assert c.post(f"{url}/restore", headers=trainer).status_code == 403
        assert c.post("/api/trainer/content/modules", json={
            "key": f"x-{uuid.uuid4().hex[:6]}", "title_de": "X", "workshop_key": "network"},
            headers=trainer).status_code == 403
        assert put_module(c, url, json=body, headers=admin).status_code == 200
        # unbekanntes Modul bleibt 404 (vor der Rechteprüfung)
        assert put_module(c, "/api/trainer/content/modules/gibt-es-nicht", json=body,
                          headers=trainer).status_code == 404


def test_besitzer_speichert_eigenes_modul():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, _, owner = _new_trainer(c, admin)
        _, _, other = _new_trainer(c, admin)
        key, mod = _draft(c, admin, owner_id)
        url = f"/api/trainer/content/modules/{mod}"
        assert put_module(c, url, json=_body(), headers=owner).status_code == 200
        assert put_module(c, url, json=_body(), headers=other).status_code == 403
        # Besitzer legt weitere Module im eigenen Entwurf an, Fremder nicht
        assert c.post("/api/trainer/content/modules", json={
            "key": f"{key}-m2", "title_de": "Zwei", "workshop_key": key}, headers=owner).status_code == 200
        assert c.post("/api/trainer/content/modules", json={
            "key": f"{key}-m3", "title_de": "Drei", "workshop_key": key}, headers=other).status_code == 403
        # Entwurf taucht in den Modullisten des Fremden nicht auf, beim Besitzer schon
        assert mod not in {m["key"] for m in c.get("/api/trainer/modules", headers=other).json()}
        assert mod not in {m["key"] for m in c.get("/api/trainer/content/modules", headers=other).json()}
        assert mod in {m["key"] for m in c.get("/api/trainer/modules", headers=owner).json()}
        assert mod in {m["key"] for m in c.get("/api/trainer/content/modules", headers=owner).json()}
        assert c.get(url, headers=other).status_code == 404
        assert c.get(f"/api/trainer/modules/{mod}", headers=other).status_code == 404


def test_entwurf_fehlt_oeffentlich():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, _, _ = _new_trainer(c, admin)
        key, _ = _draft(c, admin, owner_id)
        assert key not in {w["key"] for w in c.get("/api/workshops").json()}
        assert c.get(f"/api/workshops/{key}").status_code == 404
        assert c.get("/api/workshops/network").status_code == 200


def test_kurs_auf_entwurf_nur_besitzer_oder_admin():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, _, owner = _new_trainer(c, admin)
        _, _, other = _new_trainer(c, admin)
        key, _ = _draft(c, admin, owner_id)
        body = {"name": "Testkurs", "workshop_key": key}
        assert c.post("/api/courses", json=body, headers=other).status_code == 403
        assert c.post("/api/courses", json=body, headers=owner).status_code == 200
        assert c.post("/api/courses", json=body, headers=admin).status_code == 200


def test_publish_nur_admin():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, _, owner = _new_trainer(c, admin)
        key, _ = _draft(c, admin, owner_id)
        url = f"/api/trainer/workshops/{key}/publish"
        assert c.post(url, headers=owner).status_code == 403
        r = c.post(url, headers=admin)
        assert r.status_code == 200
        assert r.json()["status"] == "published"
        assert c.post(url, headers=admin).status_code == 200  # idempotent
        assert c.post("/api/trainer/workshops/gibt-es-nicht/publish", headers=admin).status_code == 404
        assert key in {w["key"] for w in c.get("/api/workshops").json()}
        audit = c.get("/api/trainer/audit", params={"action": "workshop.publish"}, headers=admin).json()
        assert any(e["target"] == f"workshop:{key}" for e in audit)


def test_trainer_workshops_liefert_editable_und_status():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, owner_name, owner = _new_trainer(c, admin)
        _, _, other = _new_trainer(c, admin)
        key, _ = _draft(c, admin, owner_id)

        mine = {w["key"]: w for w in c.get("/api/trainer/workshops", headers=owner).json()}
        assert mine[key]["status"] == "draft"
        assert mine[key]["editable"] is True
        assert mine[key]["owner_name"] == owner_name
        assert mine[key]["title"] == {"de": "Entwurf", "en": "Draft"}
        assert mine["network"]["editable"] is False
        assert mine["network"]["status"] == "published"
        assert mine["network"]["owner_name"] is None

        theirs = {w["key"]: w for w in c.get("/api/trainer/workshops", headers=other).json()}
        assert key not in theirs
        assert "network" in theirs

        everything = {w["key"]: w for w in c.get("/api/trainer/workshops", headers=admin).json()}
        assert everything[key]["editable"] is True
        assert everything["network"]["editable"] is True
        assert c.get("/api/trainer/workshops").status_code in (401, 403)
