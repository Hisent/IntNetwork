import uuid

import pytest
from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models.content import ContentBlock, ContentModule
from app.models.course import Course
from app.models.course_module import CourseModule
from app.services.content_editor import EditorError, create_module, delete_module
from app.services.workshop_editor import create_workshop, sections_view, update_workshop

T = {"trainer_id": 1, "is_admin": True}


@pytest.fixture(autouse=True, scope="module")
def _startup():
    with TestClient(app):  # Startup legt Schema/Seed an
        yield


def _ws(db, **kw):
    key = f"w-{uuid.uuid4().hex[:8]}"
    args = dict(key=key, title_de="T", title_en="T", summary_de="S", summary_en="S",
                theme="network", context=None)
    args.update(kw)
    return create_workshop(db, T, **args)


def test_create_workshop_ist_entwurf_mit_besitzer():
    with SessionLocal() as db:
        ws = _ws(db)
        assert ws.status == "draft" and ws.owner_trainer_id == 1 and ws.sections == []


def test_create_workshop_lehnt_unbekanntes_theme_ab():
    with SessionLocal() as db, pytest.raises(EditorError) as e:
        _ws(db, theme="pink")
    assert e.value.status == 422


def test_sections_vergeben_order_und_bereiche():
    with SessionLocal() as db:
        ws = _ws(db)
        for n in "abc":
            create_module(db, f"{ws.key}-{n}", ws.key, n)
        k = [f"{ws.key}-{n}" for n in "abc"]
        update_workshop(db, T, ws.key, {}, [
            {"title_de": "A", "title_en": "A", "modules": [k[2], k[0]]},
            {"title_de": "B", "title_en": "B", "modules": [k[1]]}])
        db.refresh(ws)
        assert [(s["from"], s["to"]) for s in ws.sections] == [(1, 2), (3, 3)]
        assert [db.get(ContentModule, x).order for x in k] == [2, 3, 1]
        assert [s["modules"] for s in sections_view(db, ws)] == [[k[2], k[0]], [k[1]]]


def test_sections_lehnen_fehlende_doppelte_fremde_module_ab():
    with SessionLocal() as db:
        ws = _ws(db)
        a, b = f"{ws.key}-a", f"{ws.key}-b"
        create_module(db, a, ws.key, "a")
        create_module(db, b, ws.key, "b")
        for mods in ([a], [a, a, b], [a, b, "fremd"]):
            with pytest.raises(EditorError) as e:
                update_workshop(db, T, ws.key, {"title_de": "Neu"},
                                [{"title_de": "A", "title_en": "A", "modules": mods}])
            assert e.value.status == 422 and "genau einmal" in e.value.message
        db.refresh(ws)
        assert ws.title_de == "T" and ws.sections == []
        assert db.get(ContentModule, a).order == 1


def test_mitgelieferter_workshop_nicht_aenderbar():
    from app.content.workshops import WORKSHOPS
    key = next(iter(WORKSHOPS))
    with SessionLocal() as db, pytest.raises(EditorError) as e:
        update_workshop(db, T, key, {"title_de": "x"}, None)
    assert e.value.status == 422 and "im Code" in e.value.message


def test_delete_module_nur_im_entwurf():
    with SessionLocal() as db:
        ws = _ws(db)
        m = f"{ws.key}-m"
        create_module(db, m, ws.key, "m")
        db.add(ContentBlock(module_key=m, **_block_kw(db)))
        c = Course(name="C", join_code=uuid.uuid4().hex[:8], workshop_key=ws.key)
        db.add(c)
        db.flush()
        db.add(CourseModule(course_id=c.id, module_key=m))
        db.commit()
        ws.status = "published"
        db.commit()
        with pytest.raises(EditorError) as e:
            delete_module(db, m)
        assert e.value.status == 422
        ws.status = "draft"
        db.commit()
        delete_module(db, m)
        assert db.get(ContentModule, m) is None
        assert db.query(ContentBlock).filter_by(module_key=m).count() == 0
        assert db.query(CourseModule).filter_by(module_key=m).count() == 0


def _block_kw(db):
    cols = {c.name: c for c in ContentBlock.__table__.columns}
    kw = {}
    for n, c in cols.items():
        if n in ("id", "module_key") or c.nullable or c.default is not None or c.server_default is not None:
            continue
        kw[n] = 0 if c.type.python_type is int else ({} if c.type.python_type is dict else "x")
    return kw


def test_delete_module_raeumt_abhaengige_daten_und_voraussetzungen_auf():
    from app.models.comment import Comment
    from app.models.live_poll import LivePoll, LivePollVote
    from app.models.module_disabled import ModuleDisabled
    from app.models.participant import Participant
    from app.models.progress import Progress
    from app.models.quiz_result import QuizResult
    from app.services.content_editor import ModuleIn, module_state, save_module

    with SessionLocal() as db:
        ws = _ws(db)
        a, b = f"{ws.key}-a", f"{ws.key}-b"
        create_module(db, a, ws.key, "a")
        create_module(db, b, ws.key, "b")
        db.get(ContentModule, b).prerequisites = [a]
        c = Course(name="C", join_code=uuid.uuid4().hex[:8], workshop_key=ws.key)
        db.add(c)
        db.flush()
        p = Participant(course_id=c.id, name="P", current_module_key=a)
        db.add(p)
        db.flush()
        poll = LivePoll(course_id=c.id, module_key=a, source="adhoc", ref="r")
        db.add(poll)
        db.flush()
        db.add_all([
            Progress(participant_id=p.id, module_key=a),
            QuizResult(participant_id=p.id, module_key=a, score=1, total=1, answers={}),
            Comment(course_id=c.id, module_key=a, block_index=0, body="x",
                    author_kind="participant", author_name="P", participant_id=p.id),
            ModuleDisabled(course_id=c.id, module_key=a),
            LivePollVote(poll_id=poll.id, participant_id=p.id, choice=0),
        ])
        db.commit()
        pid, poll_id = p.id, poll.id

        delete_module(db, a)

        for model in (Progress, QuizResult, Comment, ModuleDisabled, LivePoll):
            assert db.query(model).filter_by(module_key=a).count() == 0, model
        assert db.query(LivePollVote).filter_by(poll_id=poll_id).count() == 0
        assert db.get(Participant, pid).current_module_key is None
        db.refresh(db.get(ContentModule, b))
        assert db.get(ContentModule, b).prerequisites == []
        _, state, version = module_state(db, b)
        save_module(db, b, ModuleIn(**state), version)
