from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content import registry


def test_public_module_strips_answers_keeps_scenario():
    with TestClient(app):
        db = SessionLocal()
        try:
            pub = registry.public_module(db, "vlan")
            assert pub is not None
            for q in pub["quiz"]["questions"]:
                assert "answer" not in q
            assert pub["prerequisites"] == ["paket", "switching"]
            assert "scenario" in pub
            assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]
        finally:
            db.close()


def test_module_meta_has_prereqs_and_order():
    with TestClient(app):
        db = SessionLocal()
        try:
            metas = registry.module_meta(db)
            assert metas[0]["key"] == "paket"
            assert any(m["key"] == "switching" and m["order"] == 2 for m in metas)
            assert any(m["key"] == "subnetting" and m["order"] == 4 for m in metas)
            assert any(m["key"] == "arp" and m["order"] == 5 for m in metas)
            assert any(m["key"] == "routing" and m["order"] == 6 for m in metas)
            assert any(m["key"] == "nat" and m["order"] == 7 for m in metas)
            assert any(m["key"] == "dns" and m["order"] == 8 for m in metas)
            assert any(m["key"] == "dhcp" and m["order"] == 9 for m in metas)
            assert any(m["key"] == "ports" and m["order"] == 10 for m in metas)
            assert any(m["key"] == "icmp" and m["order"] == 11 for m in metas)
            assert any(m["key"] == "firewall" and m["order"] == 12 for m in metas)
            assert any(m["key"] == "ipv6" and m["order"] == 13 for m in metas)
            assert any(m["key"] == "wlan" and m["order"] == 14 for m in metas)
            assert any(m["key"] == "vpn" and m["order"] == 15 for m in metas)
            vlan = next(m for m in metas if m["key"] == "vlan")
            assert vlan["prerequisites"] == ["paket", "switching"]
            assert registry.public_module(db, "nope") is None
        finally:
            db.close()


def test_public_module_strips_notes_and_goals():
    with TestClient(app):
        db = SessionLocal()
        try:
            pub = registry.public_module(db, "switching")
            assert "goals" not in pub
            for b in pub["blocks"]:
                assert "note" not in b
            for q in pub["quiz"]["questions"]:
                assert "answer" not in q
        finally:
            db.close()


def test_every_module_has_goals_and_notes():
    for key, m in registry.MODULES.items():
        assert m.get("goals"), f"{key} ohne goals"
        assert any("note" in b for b in m["blocks"]), f"{key} ohne Block-Notiz"


def test_public_module_resolves_language():
    with TestClient(app):
        db = SessionLocal()
        try:
            de = registry.public_module(db, "switching", "de")
            en = registry.public_module(db, "switching", "en")
            assert de["scenario"] != en["scenario"]
            assert de["blocks"][0]["value"] != en["blocks"][0]["value"]
            assert de["quiz"]["questions"][0]["prompt"] != en["quiz"]["questions"][0]["prompt"]
            assert de["quiz"]["questions"][0]["options"] != en["quiz"]["questions"][0]["options"]
            assert len(de["quiz"]["questions"][0]["options"]) == len(en["quiz"]["questions"][0]["options"])
            assert isinstance(de["scenario"], str)
            assert isinstance(en["blocks"][0]["value"], str)
        finally:
            db.close()


def test_public_module_defaults_to_de_and_falls_back_on_unknown_lang():
    with TestClient(app):
        db = SessionLocal()
        try:
            default = registry.public_module(db, "switching")
            de = registry.public_module(db, "switching", "de")
            assert default["scenario"] == de["scenario"]
            unknown = registry.public_module(db, "switching", "fr")
            assert unknown["scenario"] == de["scenario"]
        finally:
            db.close()


def test_quiz_answers_are_index_based():
    m = registry.MODULES["switching"]
    for q in m["quiz"]["questions"]:
        if q["type"] == "single":
            assert isinstance(q["answer"], int)
            assert 0 <= q["answer"] < len(q["options"]["de"])
        if q["type"] == "multi":
            assert all(isinstance(a, int) for a in q["answer"])


def test_every_module_is_bilingual_with_index_answers():
    for key, m in registry.MODULES.items():
        assert isinstance(m["scenario"], dict) and "de" in m["scenario"] and "en" in m["scenario"], key
        for b in m["blocks"]:
            if "value" in b:
                assert isinstance(b["value"], dict) and "de" in b["value"] and "en" in b["value"], f"{key} block"
        for q in m["quiz"]["questions"]:
            assert isinstance(q["prompt"], dict) and "de" in q["prompt"] and "en" in q["prompt"], f"{key} {q['id']}"
            if q["type"] in ("single", "multi"):
                opts = q["options"]
                assert isinstance(opts, dict) and len(opts["de"]) == len(opts["en"]), f"{key} {q['id']}"
                if q["type"] == "single":
                    assert isinstance(q["answer"], int), f"{key} {q['id']}"
                else:
                    assert all(isinstance(a, int) for a in q["answer"]), f"{key} {q['id']}"


def test_trainer_module_keeps_notes_answers_goals():
    with TestClient(app):
        db = SessionLocal()
        try:
            m = registry.trainer_module(db, "switching")
            assert m["goals"]
            assert any("note" in b for b in m["blocks"])
            assert m["quiz"]["questions"][0]["answer"] is not None
            assert isinstance(m["scenario"], str)
            assert isinstance(m["blocks"][0]["value"], str)
            assert registry.trainer_module(db, "nope") is None
        finally:
            db.close()
