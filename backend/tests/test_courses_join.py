from concurrent.futures import ThreadPoolExecutor

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
        resume = r.json()["resume_code"]
        assert resume  # Erstbeitritt liefert den persönlichen Wiederaufnahme-Code

        # Wiederaufnahme unter gleichem Namen braucht jetzt den Code ...
        assert c.post("/api/join", json={"code": code, "name": "Anna"}).status_code == 403
        # ... mit korrektem Code klappt sie (auch klein geschrieben).
        r2 = c.post("/api/join", json={"code": code, "name": "Anna", "resume_code": resume.lower()})
        assert r2.status_code == 200

        me = c.get("/api/me", headers={"Authorization": f"Bearer {tok}"})
        assert me.status_code == 200
        assert me.json()["name"] == "Anna"
        assert any(p["module_key"] == "vlan" for p in me.json()["progress"])

        # Kursliste zeigt Teilnehmerzahl (für die Trainer-Kurskarten)
        listed = next(x for x in c.get("/api/courses", headers=h).json() if x["join_code"] == code)
        assert listed["participant_count"] == 1

        assert c.post("/api/join", json={"code": "ZZZZZZ", "name": "X"}).status_code == 404
        assert c.post("/api/courses", json={"name": "x"},
                      headers={"Authorization": f"Bearer {tok}"}).status_code == 403


def test_list_courses_pagination_and_order():
    with TestClient(app) as c:
        h = _trainer(c)
        created_ids = [c.post("/api/courses", json={"name": f"PagKurs{i}"}, headers=h).json()["id"]
                      for i in range(3)]

        full = c.get("/api/courses", headers=h).json()
        ids_full = [x["id"] for x in full]
        # Default schneidet nichts ab -- alle drei eben angelegten Kurse sind dabei,
        # neuester zuerst.
        assert ids_full.index(created_ids[2]) < ids_full.index(created_ids[1]) < ids_full.index(created_ids[0])

        limited = c.get("/api/courses?limit=1", headers=h).json()
        assert len(limited) == 1
        assert limited[0]["id"] == ids_full[0]

        offset_page = c.get("/api/courses?limit=1&offset=1", headers=h).json()
        assert offset_page[0]["id"] == ids_full[1]


def test_dashboard_aggregates_progress_and_best():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/courses", json={"name": "DashKurs"}, headers=h).json()
        code = created["join_code"]
        cid = next(x["id"] for x in c.get("/api/courses", headers=h).json() if x["join_code"] == code)

        p = {"Authorization": "Bearer " + c.post(
            "/api/join", json={"code": code, "name": "Dana"}).json()["access_token"]}
        mod = c.get("/api/modules/vlan", headers=p).json()
        ids = [q["id"] for q in mod["quiz"]["questions"]]
        # Reihenfolge/Antworten wie in app/content/vlan.py (vgl. test_modules_quiz)
        good = {ids[0]: 1, ids[1]: 1, ids[2]: [0, 1, 3], ids[3]: 20}
        assert c.post("/api/modules/vlan/quiz", json={"answers": good}, headers=p).json()["passed"] is True
        # zweiter, schlechterer Versuch darf best nicht verschlechtern
        c.post("/api/modules/vlan/quiz", json={"answers": {ids[0]: 0}}, headers=p)

        dash = c.get(f"/api/courses/{cid}/dashboard", headers=h).json()
        row = next(r for r in dash["participants"] if r["name"] == "Dana")
        assert row["cells"]["vlan"] == {"done": True, "best": 100}
        assert row["cells"]["paket"] == {"done": False, "best": None}

        assert c.get("/api/courses/999999/dashboard", headers=h).status_code == 404


def test_concurrent_join_same_name_never_500s():
    """Zwei gleichzeitige Joins mit demselben Namen (z.B. Doppelklick) duerfen
    nie mit 500 crashen -> beide bekommen einen gueltigen Token fuer denselben
    Teilnehmer-Datensatz."""
    with TestClient(app, raise_server_exceptions=False) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "RaceKurs"}, headers=h).json()["join_code"]

        results = []

        def join():
            r = c.post("/api/join", json={"code": code, "name": "Racer"})
            results.append(r)

        with ThreadPoolExecutor(max_workers=8) as ex:
            list(ex.map(lambda _: join(), range(8)))

        # Kein 500 im Rennen. Späte Threads, die die schon committete Zeile sehen,
        # dürfen mit 403 (Name vergeben, Code nötig) antworten — nur nie crashen.
        assert all(r.status_code in (200, 403) for r in results)
        assert any(r.status_code == 200 for r in results)
        assert all(r.json()["name"] == "Racer" for r in results if r.status_code == 200)


def test_changelog_trainer_only():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "ClKurs"}, headers=h).json()["join_code"]
        tok = c.post("/api/join", json={"code": code, "name": "Dora"}).json()["access_token"]
        assert c.get("/api/changelog", headers=h).status_code == 200
        assert len(c.get("/api/changelog", headers=h).json()) > 0
        # Teilnehmer darf nicht
        assert c.get("/api/changelog", headers={"Authorization": f"Bearer {tok}"}).status_code == 403


def test_company_endpoint():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "CoKurs"}, headers=h).json()["join_code"]
        tok = c.post("/api/join", json={"code": code, "name": "Cara"}).json()["access_token"]
        r = c.get("/api/company", headers={"Authorization": f"Bearer {tok}"})
        assert r.status_code == 200
        assert r.json()["name"] == "Nordwind Logistik GmbH"


def test_participant_language_default_and_patch():
    with TestClient(app) as c:
        h = _trainer(c)
        code = c.post("/api/courses", json={"name": "KursLang"}, headers=h).json()["join_code"]
        p = {"Authorization": "Bearer " + c.post(
            "/api/join", json={"code": code, "name": "P1"}).json()["access_token"]}

        assert c.get("/api/me", headers=p).json()["language"] == "de"
        assert c.get("/api/company", headers=p).json()["blurb"]

        r = c.patch("/api/me/language", json={"language": "en"}, headers=p)
        assert r.status_code == 200 and r.json() == {"language": "en"}
        assert c.get("/api/me", headers=p).json()["language"] == "en"

        en_blurb = c.get("/api/company", headers=p).json()["blurb"]
        c.patch("/api/me/language", json={"language": "de"}, headers=p)
        de_blurb = c.get("/api/company", headers=p).json()["blurb"]
        assert en_blurb != de_blurb

        assert c.patch("/api/me/language", json={"language": "fr"}, headers=p).status_code == 422
