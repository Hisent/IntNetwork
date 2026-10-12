"""Struktureller Konsistenztest über ALLE ausgelieferten Module (app/content).

Prüft, was sonst erst im Betrieb auffällt: fehlende Übersetzung, Quiz ohne
gültige Lösung, doppelte Frage-/Block-ids, Voraussetzungen über Lehrgangsgrenzen,
Module außerhalb jeder Sektion (unsichtbar in der Navigation) und eine README,
die andere Modulzahlen nennt als der Code.

Die Blockstruktur selbst prüft bewusst derselbe Code wie der Modul-Editor
(`_validate`) -- ein Seed-Modul, das dort durchfällt, ließe sich im Editor weder
speichern noch per "Auslieferungszustand laden" zurückholen.
"""
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

INTERAKTIV = {"widget", "check", "order", "debug", "reveal", "reflect"}


def _leer(value) -> bool:
    return not isinstance(value, str) or not value.strip()


def _zweisprachig(value) -> bool:
    return isinstance(value, dict) and not _leer(value.get("de")) and not _leer(value.get("en"))


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
    for bid, n in Counter(b["id"] for b in blocks if b.get("type") != "widget" and "id" in b).items():
        if n > 1:
            out.append(f"Block-id '{bid}' {n}-fach (Anker für Content-Migrationen)")

    questions = (m.get("quiz") or {}).get("questions") or []
    if not questions:
        out.append("Quiz ohne Fragen")
    for qid, n in Counter(q.get("id") for q in questions).items():
        if n > 1 or _leer(qid):
            out.append(f"Frage-id '{qid}' fehlt oder ist {n}-fach")
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


def test_readme_module_counts_match_code():
    readme = (Path(__file__).resolve().parents[2] / "README.md").read_text(encoding="utf-8")
    assert f"zusammen {len(MODULES)} Modulen" in readme, f"README nennt nicht {len(MODULES)} Module"
    per_workshop = Counter(workshop_for_order(m["order"]) for m in MODULES.values())
    assert set(per_workshop) == set(WORKSHOPS)
    for key, n in per_workshop.items():
        title = WORKSHOPS[key]["title_de"]
        assert re.search(rf"\*\*{re.escape(title)} \({n} Module\):\*\*", readme), \
            f"README: '{title} ({n} Module)' fehlt oder nennt eine andere Zahl"
