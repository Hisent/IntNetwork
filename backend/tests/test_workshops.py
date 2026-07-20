from fastapi.testclient import TestClient

from app.content.registry import MODULES
from app.content.workshops import WORKSHOPS, seed_workshops, workshop_for_order
from app.database import SessionLocal
from app.main import app
from app.models.content import ContentModule
from app.models.course import Course
from app.models.course_module import CourseModule


def _trainer(client):
    token = client.post("/api/trainer/login", json={
        "email": "trainer@test.de", "password": "trainerpass1",
    }).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_every_seeded_module_maps_to_exactly_one_section():
    """Regression zu v1.19.0: neue Module dürfen nicht still in keinem Abschnitt
    landen (Ursache: Module 116–118 ohne passende Section). Jedes ausgelieferte
    Modul muss über seine order in genau einen Abschnitt seines Workshops fallen."""
    for key, module in MODULES.items():
        workshop_key = workshop_for_order(module["order"])
        sections = WORKSHOPS[workshop_key]["sections"]
        hits = [s for s in sections if s["from"] <= module["order"] <= s["to"]]
        assert len(hits) == 1, (
            f"Modul {key!r} (order {module['order']}) fällt in {len(hits)} "
            f"Abschnitte von Workshop {workshop_key!r}, erwartet genau 1")


def test_workshop_catalog_and_code_bound_join():
    with TestClient(app) as client:
        workshops = client.get("/api/workshops")
        assert workshops.status_code == 200
        assert {workshop["key"] for workshop in workshops.json()} >= {"network", "claude-code"}

        claude = client.get("/api/workshops/claude-code").json()
        assert claude["theme"] == "claude"
        assert claude["modules"]

        trainer = _trainer(client)
        course = client.post("/api/courses", json={
            "name": "Claude Team", "workshop_key": "claude-code",
        }, headers=trainer).json()
        assert course["workshop_key"] == "claude-code"

        wrong = client.post("/api/join", json={
            "code": course["join_code"], "name": "Ada", "workshop_key": "network",
        })
        assert wrong.status_code == 404

        joined = client.post("/api/join", json={
            "code": course["join_code"], "name": "Ada", "workshop_key": "claude-code",
        }).json()
        participant = {"Authorization": f"Bearer {joined['access_token']}"}
        visible = client.get("/api/modules", headers=participant).json()
        assert {module["key"] for module in visible} == {module["key"] for module in claude["modules"]}
        me = client.get("/api/me", headers=participant).json()
        assert me["workshop"]["key"] == "claude-code"
        assert {progress["module_key"] for progress in me["progress"]} == {module["key"] for module in visible}


def test_new_content_is_opt_in_for_existing_course():
    with TestClient(app) as client:
        trainer = _trainer(client)
        course = client.post("/api/courses", json={
            "name": "Network Opt-in", "workshop_key": "network",
        }, headers=trainer).json()
        created = client.post("/api/trainer/content/modules", json={
            "key": "network-opt-in-test", "title_de": "Opt-in Test", "workshop_key": "network",
        }, headers=trainer)
        assert created.status_code == 200

        modules = client.get(f"/api/courses/{course['id']}/modules", headers=trainer).json()
        added = next(module for module in modules if module["key"] == "network-opt-in-test")
        assert added["active"] is False

        token = client.post("/api/join", json={"code": course["join_code"], "name": "Bea"}).json()["access_token"]
        participant = {"Authorization": f"Bearer {token}"}
        assert client.get("/api/modules/network-opt-in-test", headers=participant).status_code == 404


def test_legacy_course_migrates_to_network_only():
    db = SessionLocal()
    try:
        network_keys = {module.key for module in db.query(ContentModule)
                        .filter(ContentModule.workshop_key == "network")}
        claude_key = db.query(ContentModule).filter(
            ContentModule.workshop_key == "claude-code").first().key
        legacy = Course(name="Legacy", join_code="LEGACY")
        db.add(legacy)
        db.flush()
        db.add(CourseModule(course_id=legacy.id, module_key=claude_key))
        db.commit()

        seed_workshops(db)
        db.refresh(legacy)
        active = {row.module_key for row in db.query(CourseModule).filter(
            CourseModule.course_id == legacy.id)}
        assert legacy.workshop_key == "network"
        assert active == network_keys
    finally:
        db.close()


def test_existing_course_receives_new_seeded_modules_but_not_trainer_opt_ins():
    db = SessionLocal()
    course = None
    try:
        seeded_key = next(key for key in MODULES if MODULES[key]["order"] < 100)
        course = Course(name="Existing", join_code="EXISTING", workshop_key="network")
        db.add(course)
        db.flush()
        db.query(CourseModule).filter(CourseModule.course_id == course.id,
                                      CourseModule.module_key == seeded_key).delete()
        custom = ContentModule(key="trainer-only-sync-test", workshop_key="network", order=999,
                               title_de="Trainer", title_en="Trainer", goals=[],
                               scenario_de="", scenario_en="")
        db.add(custom)
        db.commit()

        seed_workshops(db)

        active = {row.module_key for row in db.query(CourseModule)
                  .filter(CourseModule.course_id == course.id).all()}
        assert seeded_key in active
        assert custom.key not in active
    finally:
        if course is not None:
            db.query(CourseModule).filter(CourseModule.course_id == course.id).delete()
            db.query(Course).filter(Course.id == course.id).delete()
        db.query(ContentModule).filter(ContentModule.key == "trainer-only-sync-test").delete()
        db.commit()
        db.close()
