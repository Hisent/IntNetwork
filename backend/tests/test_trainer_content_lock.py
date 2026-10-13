"""Optimistische Sperre des Modul-Editors: Wer auf einem veralteten Stand
speichert, bekommt 409 statt den Stand des anderen Trainers zu überschreiben."""
from fastapi.testclient import TestClient

from app.main import app
from tests.test_trainer_content import _minimal_module, _trainer

URL = "/api/trainer/content/modules/lockmod"


def test_save_with_stale_version_is_rejected_and_changes_nothing():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "lockmod", "title_de": "Sperre"}, headers=h)
        geladen = c.get(URL, headers=h).json()["version"]

        # Trainer A speichert auf dem geladenen Stand -> ok, neue Version.
        erster = c.put(f"{URL}?base_version={geladen}", json={**_minimal_module(), "title_de": "von A"}, headers=h)
        assert erster.status_code == 200, erster.text
        neu = erster.json()["version"]
        assert neu != geladen and neu == c.get(URL, headers=h).json()["version"]

        # Trainer B hatte denselben Stand geladen und speichert danach -> 409.
        zweiter = c.put(f"{URL}?base_version={geladen}", json={**_minimal_module(), "title_de": "von B"}, headers=h)
        assert zweiter.status_code == 409
        assert c.get(URL, headers=h).json()["title_de"] == "von A"

        # Mit aktueller Version klappt es.
        assert c.put(f"{URL}?base_version={neu}", json=_minimal_module(), headers=h).status_code == 200


def test_save_without_base_version_is_rejected_and_keeps_explanations_and_goals_en():
    """Ein Editor-Tab von vor dem Update schickt weder base_version noch die
    neueren Felder — sein PUT würde Erklärungen und goals_en still löschen."""
    url = "/api/trainer/content/modules/arp"
    with TestClient(app) as c:
        h = _trainer(c)
        before = c.get(url, headers=h).json()
        assert before["goals_en"] and any(q["explanation_de"] for q in before["quiz"])
        old_tab = {k: v for k, v in before.items() if k not in ("goals_en", "version")}
        old_tab["quiz"] = [{k: v for k, v in q.items() if not k.startswith("explanation_")} for q in before["quiz"]]

        r = c.put(url, json=old_tab, headers=h)

        assert r.status_code == 409 and "neu laden" in r.json()["detail"]
        assert c.get(url, headers=h).json() == before


def test_emptied_optional_text_fields_do_not_mark_a_shipped_module_as_edited():
    """Der Editor schickt für ein leeres Notizfeld "" — das darf den Stand nicht
    vom Auslieferungsstand (None) abweichen lassen."""
    from app.content import sync
    from app.database import SessionLocal
    url = "/api/trainer/content/modules/arp"
    with TestClient(app) as c:
        h = _trainer(c)
        loaded = c.get(url, headers=h).json()
        with SessionLocal() as db:
            before = sync.content_hash(sync.db_state(*sync.load_all(db)["arp"]))
        for b in loaded["blocks"]:
            for field in ("note", "value_de", "value_en", "widget_id"):
                if b[field] is None:
                    b[field] = ""
        assert c.put(f"{url}?base_version={loaded['version']}", json=loaded, headers=h).status_code == 200
        with SessionLocal() as db:
            assert sync.content_hash(sync.db_state(*sync.load_all(db)["arp"])) == before
        assert all(b["note"] is None for b in c.get(url, headers=h).json()["blocks"] if b["type"] == "text")


def test_concurrent_saves_are_serialized_by_row_lock():
    """Zwei PUTs im selben Augenblick lasen früher beide den alten Stand und
    kamen beide durch (doppelte Kennungen möglich). Unter Postgres sperrt das
    Speichern die Modulzeile: der zweite wartet, liest dann den neuen Stand und
    bekommt 409. SQLite kennt keine Zeilensperre (nur Entwicklung/Tests)."""
    import time
    from concurrent.futures import ThreadPoolExecutor

    import pytest
    from sqlalchemy import text

    from app.database import engine
    if engine.dialect.name != "postgresql":
        pytest.skip("Zeilensperre gibt es nur unter Postgres")
    url = "/api/trainer/content/modules/sperrmod"
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "sperrmod", "title_de": "Sperre"}, headers=h)
        version = c.get(url, headers=h).json()["version"]

        def save(title):
            return c.put(f"{url}?base_version={version}", json={**_minimal_module(), "title_de": title},
                         headers=h).status_code

        with engine.connect() as holder, ThreadPoolExecutor(2) as pool:
            holder.execute(text("SELECT 1 FROM content_module WHERE key = 'sperrmod' FOR NO KEY UPDATE"))
            saves = [pool.submit(save, title) for title in ("von A", "von B")]
            time.sleep(0.5)
            assert not any(s.done() for s in saves)  # beide warten auf die Zeilensperre
            holder.rollback()
            assert sorted(s.result() for s in saves) == [200, 409]
