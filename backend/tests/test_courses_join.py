from fastapi.testclient import TestClient
from app.main import app


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_course_and_join_flow():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "Netzwerk Q3"}, headers=h).json()["join_code"]

        r = c.post("/api/join", json={"code": code, "name": "Anna"})
        assert r.status_code == 200
        tok = r.json()["access_token"]

        r2 = c.post("/api/join", json={"code": code, "name": "Anna"})
        assert r2.status_code == 200

        me = c.get("/api/me", headers={"Authorization": f"Bearer {tok}"})
        assert me.status_code == 200
        assert me.json()["name"] == "Anna"
        assert any(p["module_key"] == "vlan" for p in me.json()["progress"])

        assert c.post("/api/join", json={"code": "ZZZZZZ", "name": "X"}).status_code == 404
        assert c.post("/api/courses", json={"name": "x"},
                      headers={"Authorization": f"Bearer {tok}"}).status_code == 403


def test_company_endpoint():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "CoKurs"}, headers=h).json()["join_code"]
        tok = c.post("/api/join", json={"code": code, "name": "Cara"}).json()["access_token"]
        r = c.get("/api/company", headers={"Authorization": f"Bearer {tok}"})
        assert r.status_code == 200
        assert r.json()["name"] == "Nordwind Logistik GmbH"
