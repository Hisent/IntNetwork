"""Prüft die Dinge, die über die Backend-/Frontend-Grenze hinweg zusammenpassen
müssen, ohne dass es eine technische Verbindung gibt: die Widget-Liste und die
Versionsnummer.

Hält VALID_WIDGET_IDS und die Frontend-Registry deckungsgleich.

Die beiden Listen werden von Hand gepflegt, es gibt keine Ableitung. Wird die
Backend-Liste beim Anlegen eines Widgets vergessen, lehnt der Modul-Editor das
Speichern mit 422 ab — das ist in diesem Projekt schon dreimal passiert (Modul
16, Modul 17, PKI-Lehrgang) und fällt jedes Mal erst im Trainerbetrieb auf,
nicht beim Ausliefern. Deshalb hier ein Abgleich statt einer weiteren Notiz.
"""
import json
import re
from pathlib import Path

from app.config import APP_VERSION
from app.routers.trainer_content import VALID_WIDGET_IDS

FRONTEND = Path(__file__).resolve().parents[2] / "frontend"
REGISTRY = FRONTEND / "src" / "widgets" / "registry.tsx"
PACKAGE_JSON = FRONTEND / "package.json"


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


def test_backend_and_frontend_version_match():
    """Die Version steht in app/config.py und in frontend/package.json. Beim
    Release v1.32.0 wurde eine dritte, hartkodierte Kopie in src/lib/version.ts
    vergessen — im Trainerbereich stand danach zwei Versionen lang die falsche
    Nummer. Die dritte Kopie ist weg (Vite setzt den Wert jetzt aus
    package.json ein), diese beiden hier bleiben und muessen zusammenpassen."""
    frontend_version = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))["version"]
    assert frontend_version == APP_VERSION, (
        f"frontend/package.json steht auf {frontend_version}, "
        f"backend/app/config.py auf {APP_VERSION}")
