from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_per_course_activation():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a = c.post("/api/courses", json={"name": "KursA"}, headers=h).json()["join_code"]
        code_b = c.post("/api/courses", json={"name": "KursB"}, headers=h).json()["join_code"]
        courses = {x["join_code"]: x["id"] for x in c.get("/api/courses", headers=h).json()}
        id_a = courses[code_a]

        mods = c.get(f"/api/courses/{id_a}/modules", headers=h).json()
        assert all(m["active"] for m in mods)

        assert c.put(f"/api/courses/{id_a}/modules", headers=h,
                     json={"module_key": "vlan", "active": False}).status_code == 200

        tok_a = c.post("/api/join", json={"code": code_a, "name": "A1"}).json()["access_token"]
        tok_b = c.post("/api/join", json={"code": code_b, "name": "B1"}).json()["access_token"]
        ha = {"Authorization": f"Bearer {tok_a}"}
        hb = {"Authorization": f"Bearer {tok_b}"}

        keys_a = [m["key"] for m in c.get("/api/modules", headers=ha).json()]
        assert "vlan" not in keys_a and "paket" in keys_a
        assert c.get("/api/modules/vlan", headers=ha).status_code == 404
        assert c.post("/api/modules/vlan/quiz", json={"answers": {}}, headers=ha).status_code == 404

        keys_b = [m["key"] for m in c.get("/api/modules", headers=hb).json()]
        assert "vlan" in keys_b

        c.put(f"/api/courses/{id_a}/modules", headers=h, json={"module_key": "vlan", "active": True})
        assert "vlan" in [m["key"] for m in c.get("/api/modules", headers=ha).json()]

        assert c.put(f"/api/courses/{id_a}/modules", headers=ha,
                     json={"module_key": "vlan", "active": False}).status_code == 403


def test_deactivation_survives_restart_seed():
    """seed_workshops() läuft bei jedem Start und reiht fehlende Seed-Module
    nach -- eine bewusste Abwahl darf dabei nicht wieder aktiv werden."""
    from app.content.workshops import seed_workshops
    from app.database import SessionLocal

    def restart():
        db = SessionLocal()
        try:
            seed_workshops(db)
        finally:
            db.close()

    with TestClient(app) as c:
        h = _trainer(c)
        cid = c.post("/api/courses", json={"name": "Restart"}, headers=h).json()["id"]
        active = lambda: {m["key"]: m["active"] for m in  # noqa: E731
                          c.get(f"/api/courses/{cid}/modules", headers=h).json()}
        c.put(f"/api/courses/{cid}/modules", headers=h, json={"module_key": "vlan", "active": False})
        restart()
        assert active()["vlan"] is False
        c.put(f"/api/courses/{cid}/modules", headers=h, json={"module_key": "vlan", "active": True})
        restart()
        assert active()["vlan"] is True
        assert c.delete(f"/api/courses/{cid}", headers=h).status_code == 200
