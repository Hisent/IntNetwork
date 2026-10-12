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

        # Mit aktueller Version klappt es; ohne base_version wie bisher (Altclients).
        assert c.put(f"{URL}?base_version={neu}", json=_minimal_module(), headers=h).status_code == 200
        assert c.put(URL, json=_minimal_module(), headers=h).status_code == 200
