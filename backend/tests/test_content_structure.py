"""Struktureller Konsistenztest über ALLE ausgelieferten Module (app/content).

Prüft, was sonst erst im Betrieb auffällt: fehlende Übersetzung, Quiz ohne
gültige Lösung, doppelte Frage-/Block-ids, Voraussetzungen über Lehrgangsgrenzen,
Module außerhalb jeder Sektion (unsichtbar in der Navigation) und eine README,
die andere Modulzahlen nennt als der Code.

Die Blockstruktur selbst prüft bewusst derselbe Code wie der Modul-Editor
(`_validate`) -- ein Seed-Modul, das dort durchfällt, ließe sich im Editor weder
speichern noch per "Auslieferungszustand laden" zurückholen.
"""
import copy
import re
from collections import Counter
from pathlib import Path

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.content.registry import MODULES
from app.content.workshops import WORKSHOPS, workshop_for_order
from app.database import SessionLocal
from app.main import app
from app.routers.trainer_content import KEY_RE, _seed_to_module_in, _validate

INTERAKTIV = {"widget", "check", "order", "debug", "reveal", "reflect",
              "diagram", "terminal", "match", "cloze", "scenario"}


ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def _leer(value) -> bool:
    return not isinstance(value, str) or not value.strip()


def _zweisprachig(value) -> bool:
    return isinstance(value, dict) and not _leer(value.get("de")) and not _leer(value.get("en"))


def _kennung_fehler(was: str, eintraege: list[dict]) -> list[str]:
    """Jeder Block und jede Frage braucht eine je Modul eindeutige id: über sie
    ordnet der Content-Sync DB-Zeilen zu (docs/content-authoring.md). Ein Widget
    kann deshalb je Modul nur einmal vorkommen (seine id ist die Widget-id)."""
    out = []
    for i, e in enumerate(eintraege):
        if not isinstance(e.get("id"), str) or not ID_RE.match(e["id"]):
            out.append(f"{was} {i} ({e.get('type')}): id fehlt oder ist ungültig (a-z, 0-9, -; max. 64): {e.get('id')!r}")
    out += [f"{was}-id '{eid}' {n}-fach" for eid, n in Counter(e.get("id") for e in eintraege).items()
            if n > 1 and eid is not None]
    return out


def _modul_fehler(key: str, m: dict) -> list[str]:
    out = []
    if m.get("key") != key or not KEY_RE.match(key):
        out.append("key ungültig")
    if _leer(m.get("title")) or _leer(m.get("title_en")):
        out.append("title/title_en fehlt")
    if not _zweisprachig(m.get("scenario")):
        out.append("scenario de/en fehlt")
    if not m.get("goals"):
        out.append("goals leer")
    if "goals_en" in m:
        en = m["goals_en"]
        if not isinstance(en, list) or len(en) != len(m.get("goals") or []) or any(_leer(g) for g in en):
            out.append("goals_en braucht je Lernziel genau eine nichtleere Übersetzung")

    workshop = workshop_for_order(m["order"])
    if not any(s["from"] <= m["order"] <= s["to"] for s in WORKSHOPS[workshop]["sections"]):
        out.append(f"order {m['order']} liegt in keiner Sektion von '{workshop}'")
    for p in m.get("prerequisites", []):
        other = MODULES.get(p)
        if other is None:
            out.append(f"Voraussetzung '{p}' existiert nicht")
        elif workshop_for_order(other["order"]) != workshop:
            out.append(f"Voraussetzung '{p}' gehört zu einem anderen Lehrgang")
        elif other["order"] >= m["order"]:
            out.append(f"Voraussetzung '{p}' liegt nicht vor dem Modul")

    blocks = m.get("blocks") or []
    if not any(b.get("type") in INTERAKTIV for b in blocks):
        out.append("kein interaktives Element")
    for i, b in enumerate(blocks):
        if b.get("type") in ("text", "reveal") and not _zweisprachig(b.get("value")):
            out.append(f"Block {i} ({b.get('type')}): value de/en fehlt")
    out += _kennung_fehler("Block", blocks)

    questions = (m.get("quiz") or {}).get("questions") or []
    if not questions:
        out.append("Quiz ohne Fragen")
    out += _kennung_fehler("Frage", questions)
    for q in questions:
        wo = f"Frage '{q.get('id')}'"
        if not _zweisprachig(q.get("prompt")):
            out.append(f"{wo}: prompt de/en fehlt")
        if q.get("type") in ("single", "multi"):
            opts = q.get("options") or {}
            for lang in ("de", "en"):
                werte = opts.get(lang) or []
                if len(werte) < 2 or any(_leer(o) for o in werte):
                    out.append(f"{wo}: options.{lang} braucht >= 2 nichtleere Einträge")
                elif len(set(werte)) != len(werte):
                    out.append(f"{wo}: doppelte Option in options.{lang}")
    return out


def test_all_modules_are_structurally_consistent():
    errors = []
    with TestClient(app):
        db = SessionLocal()
        try:
            for key, m in MODULES.items():
                errors += [f"{key}: {e}" for e in _modul_fehler(key, m)]
                try:
                    _validate(db, key, _seed_to_module_in(m))
                except HTTPException as err:
                    errors.append(f"{key}: Editor-Validierung: {err.detail}")
                except Exception as err:  # noqa: BLE001 - kaputte Seed-Form benennen statt abbrechen
                    errors.append(f"{key}: Seed-Form unlesbar: {err!r}")
        finally:
            db.close()
    for order, n in Counter(m["order"] for m in MODULES.values()).items():
        if n > 1:
            errors.append(f"order {order} {n}-fach vergeben")
    assert not errors, f"{len(errors)} Content-Fehler:\n" + "\n".join(errors)


def test_structure_check_demands_unique_ids_on_blocks_and_questions():
    m = copy.deepcopy(MODULES["arp"])
    del m["blocks"][0]["id"]
    m["blocks"][2]["id"] = m["blocks"][1]["id"]
    m["quiz"]["questions"][1]["id"] = m["quiz"]["questions"][0]["id"]
    m["quiz"]["questions"][2]["id"] = "Nicht Gültig"
    errors = "\n".join(_modul_fehler("arp", m))
    assert "Block 0 (text): id fehlt" in errors and f"Block-id '{m['blocks'][1]['id']}' 2-fach" in errors
    assert f"Frage-id '{m['quiz']['questions'][0]['id']}' 2-fach" in errors and "Frage 2" in errors


def test_structure_check_demands_complete_goals_en():
    m = copy.deepcopy(MODULES["arp"])
    m["goals_en"] = ["only one"] + [""] * (len(m["goals"]) - 1)
    assert any("goals_en" in e for e in _modul_fehler("arp", m))
    m["goals_en"] = [f"goal {i}" for i in range(len(m["goals"]))]
    assert not any("goals_en" in e for e in _modul_fehler("arp", m))
    m["goals_en"] = m["goals_en"][:-1]
    assert any("goals_en" in e for e in _modul_fehler("arp", m))


def test_readme_module_counts_match_code():
    readme = (Path(__file__).resolve().parents[2] / "README.md").read_text(encoding="utf-8")
    assert f"zusammen {len(MODULES)} Modulen" in readme, f"README nennt nicht {len(MODULES)} Module"
    per_workshop = Counter(workshop_for_order(m["order"]) for m in MODULES.values())
    assert set(per_workshop) == set(WORKSHOPS)
    for key, n in per_workshop.items():
        title = WORKSHOPS[key]["title_de"]
        assert re.search(rf"\*\*{re.escape(title)} \({n} Module\):\*\*", readme), \
            f"README: '{title} ({n} Module)' fehlt oder nennt eine andere Zahl"
