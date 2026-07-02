from fastapi.testclient import TestClient
from app.main import app
from app.content.links import LINKS


def test_links_endpoint_public():
    with TestClient(app) as c:
        r = c.get("/api/links")
        assert r.status_code == 200
        assert r.json() == LINKS


def test_links_data_consistency():
    assert len(LINKS) > 0
    for cat in LINKS:
        assert cat["category"]["de"] and cat["category"]["en"]
        assert len(cat["items"]) > 0
        for item in cat["items"]:
            assert item["url"].startswith("https://")
            assert item["title"]
            assert item["desc"]["de"] and item["desc"]["en"]
