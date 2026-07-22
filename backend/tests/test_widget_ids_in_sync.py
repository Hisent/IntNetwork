"""Hält VALID_WIDGET_IDS und die Frontend-Registry deckungsgleich.

Die beiden Listen werden von Hand gepflegt, es gibt keine Ableitung. Wird die
Backend-Liste beim Anlegen eines Widgets vergessen, lehnt der Modul-Editor das
Speichern mit 422 ab — das ist in diesem Projekt schon dreimal passiert (Modul
16, Modul 17, PKI-Lehrgang) und fällt jedes Mal erst im Trainerbetrieb auf,
nicht beim Ausliefern. Deshalb hier ein Abgleich statt einer weiteren Notiz.
"""
import re
from pathlib import Path

from app.routers.trainer_content import VALID_WIDGET_IDS

REGISTRY = Path(__file__).resolve().parents[2] / "frontend" / "src" / "widgets" / "registry.tsx"


def _frontend_widget_ids() -> set[str]:
    source = REGISTRY.read_text(encoding="utf-8")
    # Zeilenform in registry.tsx: '<id>': lazy(() => import(...))
    return set(re.findall(r"^\s*'([a-z0-9-]+)':\s*lazy\(", source, re.MULTILINE))


def test_backend_and_frontend_widget_ids_match():
    frontend = _frontend_widget_ids()
    assert frontend, f"Keine Widget-IDs in {REGISTRY} gefunden — Regex an das Dateiformat anpassen"
    assert frontend == VALID_WIDGET_IDS, (
        f"Nur im Frontend: {sorted(frontend - VALID_WIDGET_IDS)}; "
        f"nur im Backend: {sorted(VALID_WIDGET_IDS - frontend)}")


def test_every_widget_used_in_content_is_registered():
    """Ein Tippfehler in einer Widget-id einer Seed-Datei bliebe sonst stumm:
    der Block wird gespeichert, das Frontend findet nur keine Komponente."""
    from app.content.registry import MODULES

    used = {block["id"] for module in MODULES.values()
            for block in module["blocks"] if block["type"] == "widget"}
    assert used <= VALID_WIDGET_IDS, f"Unbekannte Widget-IDs im Kursinhalt: {sorted(used - VALID_WIDGET_IDS)}"
