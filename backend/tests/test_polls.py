"""Live-Abstimmung: Endpunkte und Sicherheitsgrenzen (routers/polls.py)."""
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.live_poll import LivePoll, LivePollVote
from app.models.progress import Progress
from app.models.quiz_result import QuizResult

MOD = "vlan"


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _course(c, h, name):
    course = c.post("/api/courses", json={"name": name}, headers=h).json()
    return course["join_code"], course["id"]


def _join(c, code, name):
    return {"Authorization": "Bearer " + c.post(
        "/api/join", json={"code": code, "name": name}).json()["access_token"]}


def _single(c, h, key=MOD):
    """Erste Single-Choice-Quizfrage des Moduls aus der Trainer-Ansicht (mit Lösung)."""
    return next(q for q in c.get(f"/api/trainer/modules/{key}", headers=h).json()["quiz"]["questions"]
                if q["type"] == "single")


def _start(c, h, cid, q, key=MOD):
    r = c.post(f"/api/trainer/courses/{cid}/poll", headers=h,
               json={"module_key": key, "source": "quiz", "ref": q["id"]})
    assert r.status_code == 200, r.text
    return r.json()


def _vote(c, p, poll_id, choice, key=MOD):
    return c.post(f"/api/modules/{key}/poll/vote", headers=p, json={"poll_id": poll_id, "choice": choice})


def test_ablauf_start_abstimmen_umentscheiden_aufloesen_beenden():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollAblauf")
        anna, bert = _join(c, code, "Anna"), _join(c, code, "Bert")
        q = _single(c, h)
        wrong = (q["answer"] + 1) % len(q["options"])

        assert c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json() is None
        assert c.get(f"/api/modules/{MOD}/poll", headers=anna).json() is None

        poll = _start(c, h, cid, q)
        assert poll["status"] == "open" and poll["votes"] == 0 and poll["source"] == "quiz"
        assert poll["options"] == q["options"]  # feste Reihenfolge wie gespeichert

        seen = c.get(f"/api/modules/{MOD}/poll", headers=anna).json()
        assert seen["prompt"] == q["prompt"] and seen["options"] == q["options"] and seen["my_choice"] is None

        assert _vote(c, anna, poll["id"], wrong).status_code == 200
        assert _vote(c, anna, poll["id"], q["answer"]).status_code == 200  # umentscheiden
        assert _vote(c, bert, poll["id"], wrong).status_code == 200
        assert _vote(c, bert, poll["id"], len(q["options"])).status_code == 422  # Index außerhalb
        assert _vote(c, bert, poll["id"], -1).status_code == 422
        assert c.get(f"/api/modules/{MOD}/poll", headers=anna).json()["my_choice"] == q["answer"]

        live = c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json()
        assert live["votes"] == 2 and live["counts"][q["answer"]] == 1 and live["counts"][wrong] == 1

        revealed = c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=h).json()
        assert revealed["status"] == "revealed"
        assert _vote(c, anna, poll["id"], wrong).status_code == 409
        done = c.get(f"/api/modules/{MOD}/poll", headers=bert).json()
        assert done["answer"] == q["answer"] and done["counts"] == live["counts"] and done["votes"] == 2
        assert done["explanation"] == q.get("explanation")

        assert c.delete(f"/api/trainer/courses/{cid}/poll", headers=h).json() == {"ok": True}
        assert c.get(f"/api/modules/{MOD}/poll", headers=anna).json() is None
        assert c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json() is None
        assert _vote(c, anna, poll["id"], wrong).status_code == 409
        assert c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=h).status_code == 404

        audit = c.get("/api/trainer/audit?action=poll.start", headers=h).json()
        assert any(e["target"] == f"course:{cid}" for e in audit)


def test_keine_loesung_vor_dem_aufloesen():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollGeheim")
        p = _join(c, code, "P")
        q = _single(c, h)
        poll = _start(c, h, cid, q)
        _vote(c, p, poll["id"], q["answer"])
        # Weder Lösung noch Erklärung noch Verteilung/Stimmenzahl (indirekter Hinweis) noch die Referenz.
        assert set(c.get(f"/api/modules/{MOD}/poll", headers=p).json()) == {
            "id", "kind", "status", "prompt", "options", "my_choice"}
        assert set(_vote(c, p, poll["id"], q["answer"]).json()) == {"ok", "my_choice"}


def test_kurs_isolation():
    with TestClient(app) as c:
        h = _trainer(c)
        code_a, cid_a = _course(c, h, "PollA")
        code_b, cid_b = _course(c, h, "PollB")
        a, b = _join(c, code_a, "A"), _join(c, code_b, "B")
        poll = _start(c, h, cid_a, _single(c, h))
        assert c.get(f"/api/modules/{MOD}/poll", headers=b).json() is None  # sieht nicht
        assert _vote(c, b, poll["id"], 0).status_code == 404               # stimmt nicht
        assert c.get(f"/api/trainer/courses/{cid_b}/poll", headers=h).json() is None
        assert _vote(c, a, poll["id"], 0).status_code == 200
        assert c.get(f"/api/trainer/courses/{cid_a}/poll", headers=h).json()["votes"] == 1


def test_rollen_trainer_stimmt_nicht_teilnehmer_steuert_nicht():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollRollen")
        p = _join(c, code, "P")
        q = _single(c, h)
        poll = _start(c, h, cid, q)
        assert _vote(c, h, poll["id"], 0).status_code == 403
        assert c.get(f"/api/modules/{MOD}/poll", headers=h).status_code == 403
        body = {"module_key": MOD, "source": "quiz", "ref": q["id"]}
        assert c.post(f"/api/trainer/courses/{cid}/poll", headers=p, json=body).status_code == 403
        assert c.get(f"/api/trainer/courses/{cid}/poll", headers=p).status_code == 403
        assert c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=p).status_code == 403
        assert c.delete(f"/api/trainer/courses/{cid}/poll", headers=p).status_code == 403
        assert c.get(f"/api/trainer/courses/{cid}/poll").status_code in (401, 403)
        assert c.get(f"/api/trainer/courses/{cid}/poll", headers=h).json()["status"] == "open"


def test_stimmen_bleiben_gegenueber_dem_trainer_anonym():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollAnonym")
        p = _join(c, code, "Geheimnisvoll")
        poll = _start(c, h, cid, _single(c, h))
        _vote(c, p, poll["id"], 0)
        for r in (c.get(f"/api/trainer/courses/{cid}/poll", headers=h),
                  c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=h)):
            assert set(r.json()) == {"id", "kind", "status", "prompt", "options", "counts", "votes", "answer",
                                     "explanation", "module_key", "source", "ref"}
            assert "Geheimnisvoll" not in r.text and "participant" not in r.text


def test_deaktiviertes_modul_404():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollAus")
        p = _join(c, code, "P")
        q = _single(c, h)
        poll = _start(c, h, cid, q)
        c.put(f"/api/courses/{cid}/modules", headers=h, json={"module_key": MOD, "active": False})
        assert c.get(f"/api/modules/{MOD}/poll", headers=p).status_code == 404
        assert _vote(c, p, poll["id"], 0).status_code == 404
        r = c.post(f"/api/trainer/courses/{cid}/poll", headers=h,
                   json={"module_key": MOD, "source": "quiz", "ref": q["id"]})
        assert r.status_code == 404


def test_start_prueft_referenz_und_typ():
    with TestClient(app) as c:
        h = _trainer(c)
        _code, cid = _course(c, h, "PollPruef")
        start = lambda **kw: c.post(f"/api/trainer/courses/{cid}/poll", headers=h,  # noqa: E731
                                    json={"module_key": MOD, "source": "quiz", "ref": "x", **kw}).status_code
        assert start(ref="gibt-es-nicht") == 422
        assert start(source="umfrage") == 422
        assert start(module_key="gibt-es-nicht") == 404
        assert c.post("/api/trainer/courses/999999/poll", headers=h,
                      json={"module_key": MOD, "source": "quiz", "ref": "x"}).status_code == 404
        # Frage eines anderen Moduls zählt nicht für dieses Modul
        assert start(ref=_single(c, h, "dns")["id"]) == 422
        mods = [c.get(f"/api/trainer/modules/{m['key']}", headers=h).json()
                for m in c.get("/api/trainer/modules", headers=h).json() if m["workshop_key"] == "network"]
        # Zahlenfragen und Zahlen-Checks sind keine Abstimmung
        numq = next(((m["key"], q) for m in mods for q in m["quiz"]["questions"] if q["type"] == "number"), None)
        if numq:
            assert start(module_key=numq[0], ref=numq[1]["id"]) == 422
        number = next((m["key"], b) for m in mods for b in m["blocks"]
                      if b["type"] == "check" and b["kind"] == "number")
        assert start(module_key=number[0], source="check", ref=number[1]["uid"]) == 422


def test_check_block_und_teilnehmersprache():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollCheck")
        p = _join(c, code, "P")
        key, block = next(
            (m["key"], b)
            for m in c.get("/api/trainer/modules", headers=h).json() if m["workshop_key"] == "network"
            for b in c.get(f"/api/trainer/modules/{m['key']}", headers=h).json()["blocks"]
            if b["type"] == "check" and b["kind"] == "choice")
        r = c.post(f"/api/trainer/courses/{cid}/poll", headers=h,
                   json={"module_key": key, "source": "check", "ref": block["uid"]})
        assert r.status_code == 200 and r.json()["options"] == block["options"]
        assert r.json()["answer"] == block["answer"] and r.json()["ref"] == block["uid"]
        de = c.get(f"/api/modules/{key}/poll", headers=p).json()
        assert de["prompt"] == block["prompt"]
        # Abstimmung gehört zum Modul: in einem anderen Modul erscheint sie nicht
        other = "dns" if key != "dns" else "vlan"
        assert c.get(f"/api/modules/{other}/poll", headers=p).json() is None
        assert _vote(c, p, r.json()["id"], 0, key=other).status_code == 404
        c.patch("/api/me/language", headers=p, json={"language": "en"})
        en = c.get(f"/api/modules/{key}/poll", headers=p).json()
        assert en["prompt"] != de["prompt"] and len(en["options"]) == len(de["options"])


def test_neue_abstimmung_schliesst_die_alte():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollEine")
        p = _join(c, code, "P")
        q = _single(c, h)
        first = _start(c, h, cid, q)
        _vote(c, p, first["id"], 0)
        second = _start(c, h, cid, q)
        assert second["id"] != first["id"] and second["votes"] == 0
        assert _vote(c, p, first["id"], 0).status_code == 409
        with SessionLocal() as db:
            rows = db.query(LivePoll).filter(LivePoll.course_id == cid, LivePoll.status != "closed").all()
            assert [r.id for r in rows] == [second["id"]]


def test_abstimmung_beeinflusst_weder_quiz_noch_fortschritt_und_kurs_loeschen_raeumt_auf():
    with TestClient(app) as c:
        h = _trainer(c)
        code, cid = _course(c, h, "PollWertung")
        p = _join(c, code, "P")
        q = _single(c, h)
        poll = _start(c, h, cid, q)
        before = c.get("/api/me", headers=p).json()["progress"]
        assert _vote(c, p, poll["id"], q["answer"]).status_code == 200
        c.post(f"/api/trainer/courses/{cid}/poll/reveal", headers=h)
        me = c.get("/api/me", headers=p).json()
        assert me["progress"] == before and not any(x["done"] for x in me["progress"])
        with SessionLocal() as db:
            pid = me["participant_id"]
            assert db.query(QuizResult).filter(QuizResult.participant_id == pid).count() == 0
            assert db.query(Progress).filter(Progress.participant_id == pid).count() == 0
            assert db.query(LivePollVote).filter(LivePollVote.poll_id == poll["id"]).count() == 1
        assert c.post("/api/certificate", headers=p).status_code != 200
        # ON DELETE CASCADE: mit dem Kurs verschwinden Abstimmung und Stimmen
        assert c.delete(f"/api/courses/{cid}", headers=h).status_code == 200
        with SessionLocal() as db:
            assert db.query(LivePoll).filter(LivePoll.course_id == cid).count() == 0
            assert db.query(LivePollVote).filter(LivePollVote.poll_id == poll["id"]).count() == 0
