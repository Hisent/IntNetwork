"""Kurse auf fremden Entwürfen sind für andere Trainer unsichtbar (404), sonst
verraten Dashboard/Module/Polls die Modul-Keys und Titel des Entwurfs."""
from fastapi.testclient import TestClient

from app.main import app
from tests.test_workshop_ownership import _admin, _draft, _new_trainer


def _single_course_routes(c, cid, mod, h):
    """Alle Trainer-Routen, die einen einzelnen Kurs adressieren -> Statuscodes."""
    return {
        "dashboard": c.get(f"/api/courses/{cid}/dashboard", headers=h).status_code,
        "modules": c.get(f"/api/courses/{cid}/modules", headers=h).status_code,
        "put_modules": c.put(f"/api/courses/{cid}/modules", json={"module_key": mod, "active": False},
                             headers=h).status_code,
        "approval": c.patch(f"/api/courses/{cid}/approval", json={"require_approval": True},
                            headers=h).status_code,
        "poll": c.get(f"/api/trainer/courses/{cid}/poll", headers=h).status_code,
        "poll_close": c.delete(f"/api/trainer/courses/{cid}/poll", headers=h).status_code,
        "comments": c.get(f"/api/trainer/courses/{cid}/comments", headers=h).status_code,
        "add_comment": c.post(f"/api/trainer/courses/{cid}/modules/{mod}/comments",
                              json={"block_index": 0, "body": "x"}, headers=h).status_code,
        "presence": c.get(f"/api/trainer/courses/{cid}/presence", headers=h).status_code,
        "quiz_stats": c.get(f"/api/trainer/modules/vlan/quiz-stats?course_id={cid}",
                            headers=h).status_code,
    }


def _ids(c, h):
    return {x["id"] for x in c.get("/api/courses", headers=h).json()}


def test_kurs_auf_fremdem_entwurf_ist_unsichtbar_bis_zur_veroeffentlichung():
    with TestClient(app) as c:
        admin = _admin(c)
        owner_id, _, owner = _new_trainer(c, admin)
        _, _, other = _new_trainer(c, admin)
        key, mod = _draft(c, admin, owner_id)
        r = c.post("/api/courses", json={"name": "Testlauf", "workshop_key": key}, headers=owner)
        assert r.status_code == 200, r.text
        cid = r.json()["id"]

        assert cid not in _ids(c, other)
        blocked = _single_course_routes(c, cid, mod, other)
        assert set(blocked.values()) == {404}, blocked
        r = c.get(f"/api/courses/{cid}/dashboard", headers=other)
        assert r.json()["detail"] == "Kurs nicht gefunden"
        assert c.post(f"/api/courses/{cid}/participants/1/approve", json={"approved": True},
                      headers=other).status_code == 404
        assert c.delete(f"/api/courses/{cid}", headers=other).status_code == 404

        # Besitzer und Admin sehen alles wie bisher
        for h in (owner, admin):
            assert cid in _ids(c, h)
            assert c.get(f"/api/courses/{cid}/dashboard", headers=h).status_code == 200
            assert c.get(f"/api/courses/{cid}/modules", headers=h).status_code == 200
            assert c.get(f"/api/trainer/courses/{cid}/poll", headers=h).status_code == 200
            assert c.get(f"/api/trainer/courses/{cid}/comments", headers=h).status_code == 200
            assert c.get(f"/api/trainer/courses/{cid}/presence", headers=h).status_code == 200

        assert c.post(f"/api/trainer/workshops/{key}/publish", headers=admin).status_code == 200
        assert cid in _ids(c, other)
        assert c.get(f"/api/courses/{cid}/dashboard", headers=other).status_code == 200
        assert c.get(f"/api/courses/{cid}/modules", headers=other).status_code == 200
        assert c.get(f"/api/trainer/courses/{cid}/presence", headers=other).status_code == 200
        assert c.delete(f"/api/courses/{cid}", headers=other).status_code == 200


def test_kurse_auf_veroeffentlichten_workshops_bleiben_fuer_alle_sichtbar():
    with TestClient(app) as c:
        admin = _admin(c)
        _, _, other = _new_trainer(c, admin)
        cid = c.post("/api/courses", json={"name": "Netz"}, headers=admin).json()["id"]
        assert cid in _ids(c, other)
        assert c.get(f"/api/courses/{cid}/dashboard", headers=other).status_code == 200
        assert c.get(f"/api/trainer/courses/{cid}/presence", headers=other).status_code == 200
        assert c.get(f"/api/trainer/modules/vlan/quiz-stats?course_id={cid}",
                     headers=other).status_code == 200
