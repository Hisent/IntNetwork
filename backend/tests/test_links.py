from fastapi.testclient import TestClient
from app.main import app
from app.content.links import CLAUDE_LINKS, LINKS_BY_WORKSHOP, NETWORK_LINKS


def _trainer(c):
    tok = c.post("/api/trainer/login", json={
        "email": "trainer@test.de", "password": "trainerpass1"}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def _join(c, workshop_key: str):
    h = _trainer(c)
    course = c.post("/api/courses", json={"name": f"Links {workshop_key}", "workshop_key": workshop_key}, headers=h).json()
    tok = c.post("/api/join", json={"code": course["join_code"], "name": "Lea", "workshop_key": workshop_key}).json()["access_token"]
    return {"Authorization": f"Bearer {tok}"}


def test_links_are_workshop_specific():
    with TestClient(app) as c:
        # ohne Login -> geschützt
        assert c.get("/api/links").status_code in (401, 403)

        net = c.get("/api/links", headers=_join(c, "network"))
        assert net.status_code == 200 and net.json() == NETWORK_LINKS

        claude = c.get("/api/links", headers=_join(c, "claude-code"))
        assert claude.status_code == 200 and claude.json() == CLAUDE_LINKS
        assert claude.json() != NETWORK_LINKS


def test_links_data_consistency():
    for collection in LINKS_BY_WORKSHOP.values():
        assert len(collection) > 0
        for cat in collection:
            assert cat["category"]["de"] and cat["category"]["en"]
            assert len(cat["items"]) > 0
            for item in cat["items"]:
                assert item["url"].startswith("https://")
                assert item["title"]
                assert item["desc"]["de"] and item["desc"]["en"]
