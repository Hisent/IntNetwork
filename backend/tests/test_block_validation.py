"""Deklarativer Block-Baukasten (diagram, terminal, match, cloze, scenario):
Validierung mit Feldpfad, Sprachauflösung und der Weg durch Editor-API und
Teilnehmer-Auslieferung. Autorenreferenz: docs/content-authoring.md."""
import copy

import pytest
from fastapi.testclient import TestClient

from app.content.registry import MODULES
from app.database import SessionLocal
from app.main import app
from app.models.content import ContentBlock, ContentModule, ContentModuleSnapshot, ContentQuizQuestion
from app.services.block_validation import DECLARATIVE_TYPES, localize, validate_block

SEQUENCE = {
    "kind": "sequence", "title_de": "DORA", "title_en": "DORA",
    "actors": [{"id": "c", "label": "Client"}, {"id": "s", "label_de": "Server", "label_en": "Server"}],
    "messages": [{"from": "c", "to": "s", "label": "DISCOVER", "style": "broadcast",
                  "detail_de": "Rundruf", "detail_en": "Broadcast"},
                 {"from": "s", "to": "s", "label_de": "prüft Pool", "label_en": "checks pool"}],
}
LAYERS = {"kind": "layers", "title": "TCP/IP",
          "layers": [{"name": "Transport", "content": "TCP", "pdu": "Segment", "detail": "Ports"},
                     {"name": "Internet"}]}
FLOW = {
    "kind": "flow", "title": "Topologie",
    "nodes": [{"id": "pc", "label": "PC", "shape": "host", "row": 0, "col": 0},
              {"id": "sw", "label": "Switch", "shape": "switch", "row": 0, "col": 1, "detail": "Layer 2"}],
    "edges": [{"id": "link", "from": "pc", "to": "sw", "label": "Gi1/0/1", "arrow": "none"}],
    "steps": [{"highlight": ["pc"], "text": "Start"}, {"highlight": ["link", "sw"], "text": "Weiter"}],
}
COMPARE = {"kind": "compare", "title": "AAA", "columns": [{"title": "RADIUS"}, {"title": "TACACS+"}],
           "rows": [{"label": "Transport", "values_de": ["UDP", "TCP"], "values_en": ["UDP", "TCP"]}]}
TERMINAL = {
    "prompt": "Infoblox >", "unknown": "Unknown command: {cmd}",
    "commands": [{"cmd": "show status", "aliases": ["status"], "output": "Grid Master", "desc": "Status"},
                 {"cmd": "set maintenancemode", "output_de": "", "output_en": "", "prompt": "Maintenance Mode >"}],
    "tasks": [{"text_de": "Status prüfen", "text_en": "Check status", "command": "status"},
              {"text": "Rolle?", "answers": ["Grid Master"]}],
}
MATCH = {"prompt_de": "Ordne zu", "prompt_en": "Match",
         "pairs": [{"left": "DNS", "right_de": "Namen", "right_en": "Names"},
                   {"left": "DHCP", "right_de": "Adressen", "right_en": "Addresses"},
                   {"left": "NTP", "right_de": "Zeit", "right_en": "Time"}]}
CLOZE = {"prompt": "Ergänze", "mono": True,
         "text_de": "hosts: [[ziel]]\nname: \"{{ paket }}\"\nstate: [[state]]",
         "text_en": "hosts: [[ziel]]\nname: \"{{ package }}\"\nstate: [[state]]",
         "gaps": [{"id": "ziel", "accept": ["webservers"]},
                  {"id": "state", "options": ["present", "started"], "answer": 0}]}
SCENARIO = {
    "title": "Störung", "start": "a",
    "nodes": [{"id": "a", "text": "Was tun?", "options": [{"label": "Prüfen", "to": "b"}, {"label": "Neustart", "to": "schlecht"}]},
              {"id": "b", "text": "Und dann?", "options": [{"label": "Zurück", "to": "a"}, {"label": "Beheben", "to": "gut"}]},
              {"id": "gut", "text": "Sauber gelöst.", "outcome": "good"},
              {"id": "schlecht", "text": "Ausfall.", "outcome": "bad"}],
}
VALID = [("diagram", SEQUENCE), ("diagram", LAYERS), ("diagram", FLOW), ("diagram", COMPARE),
         ("terminal", TERMINAL), ("match", MATCH), ("cloze", CLOZE), ("scenario", SCENARIO)]


@pytest.mark.parametrize("block_type,payload", VALID, ids=lambda v: v if isinstance(v, str) else v.get("kind", ""))
def test_valid_examples_pass(block_type, payload):
    validate_block(block_type, payload)


def _broken(payload: dict, change) -> dict:
    out = copy.deepcopy(payload)
    change(out)
    return out


def _set(path: list, value):
    def change(d):
        for key in path[:-1]:
            d = d[key]
        d[path[-1]] = value
    return change


def _drop(path: list):
    def change(d):
        for key in path[:-1]:
            d = d[key]
        del d[path[-1]]
    return change


INVALID = [
    # (Typ, Vorlage, Änderung, erwarteter Feldpfad/Meldungsteil)
    ("diagram", SEQUENCE, _set(["kind"], "gantt"), "kind: 'gantt' unbekannt"),
    ("diagram", SEQUENCE, _drop(["title_en"]), "title: DE und EN"),
    ("diagram", SEQUENCE, _set(["title"], "DORA"), "title: entweder title oder title_de/title_en"),
    ("diagram", SEQUENCE, _set(["actors"], [{"id": "c", "label": "Client"}]), "actors: braucht 2 bis 5"),
    ("diagram", SEQUENCE, _set(["messages", 0, "to"], "srv"), "messages[0].to: unbekannter Akteur 'srv'"),
    ("diagram", SEQUENCE, _set(["messages", 0, "style"], "fett"), "messages[0].style: 'fett' ist nicht erlaubt"),
    ("diagram", SEQUENCE, _set(["messages", 1, "label_en"], ""), "messages[1].label: DE und EN"),
    ("diagram", SEQUENCE, _set(["messages", 0, "details_de"], "x"), "messages[0].details_de: unbekanntes Feld"),
    ("diagram", SEQUENCE, _set(["actors", 1, "id"], "c"), "actors[1].id: 'c' doppelt"),
    ("diagram", SEQUENCE, _set(["messages", 0, "label"], "x" * 71), "messages[0].label: zu lang"),
    ("diagram", LAYERS, _set(["layers"], [{"name": "nur eine"}]), "layers: braucht 2 bis 8"),
    ("diagram", LAYERS, _drop(["layers", 1, "name"]), "layers[1].name: fehlt"),
    ("diagram", FLOW, _set(["edges", 0, "to"], "router"), "edges[0].to: unbekannter Knoten 'router'"),
    ("diagram", FLOW, _set(["nodes", 1, "col"], 0), "nodes[1]: Rasterzelle row=0/col=0 ist doppelt belegt"),
    ("diagram", FLOW, _set(["nodes", 0, "col"], 9), "nodes[0].col: muss eine ganze Zahl 0 bis 4"),
    ("diagram", FLOW, _set(["nodes", 0, "shape"], "printer"), "nodes[0].shape: 'printer' ist nicht erlaubt"),
    ("diagram", FLOW, _set(["steps", 1, "highlight"], ["link", "wan"]), "steps[1].highlight: unbekannte Knoten-/Kanten-id 'wan'"),
    ("diagram", FLOW, _set(["edges", 0, "to"], "pc"), "edges[0]: Kante von einem Knoten zu sich selbst"),
    ("diagram", COMPARE, _set(["rows", 0, "values_en"], ["UDP"]), "rows[0].values: values_de und values_en müssen gleich lang"),
    ("diagram", COMPARE, _set(["rows", 0, "values_de"], ["UDP", "TCP", "?"]), "rows[0].values"),
    ("diagram", COMPARE, _set(["columns"], [{"title": "allein"}]), "columns: braucht 2 bis 4"),
    ("terminal", TERMINAL, _drop(["prompt"]), "prompt: fehlt"),
    ("terminal", TERMINAL, _set(["commands"], []), "commands: braucht 1 bis 30"),
    ("terminal", TERMINAL, _drop(["commands", 0, "output"]), "commands[0].output: fehlt"),
    ("terminal", TERMINAL, _drop(["commands", 1, "output_en"]), "commands[1].output: fehlt"),
    ("terminal", TERMINAL, _set(["commands", 1, "cmd"], "Show  Status"), "commands[1].cmd: 'Show  Status' ist doppelt"),
    ("terminal", TERMINAL, _set(["tasks", 0, "command"], "show grid"), "tasks[0].command: 'show grid' ist kein cmd/alias"),
    ("terminal", TERMINAL, _set(["tasks", 1, "command"], "status"), "tasks[1]: braucht genau eines von command oder answers"),
    ("match", MATCH, _set(["pairs"], MATCH["pairs"][:2]), "pairs: braucht 3 bis 8"),
    ("match", MATCH, _set(["pairs", 1, "right_en"], "Names"), "pairs: right (en) enthält doppelte Einträge"),
    ("match", MATCH, _drop(["pairs", 2, "right_de"]), "pairs[2].right: DE und EN"),
    ("match", MATCH, _drop(["prompt_de"]), "prompt: DE und EN"),
    ("cloze", CLOZE, _set(["gaps", 0], {"id": "ziel"}), "gaps[0]: braucht genau eines von options (+ answer) oder accept"),
    ("cloze", CLOZE, _set(["gaps", 1, "answer"], 2), "gaps[1].answer: muss gültiger Options-Index"),
    ("cloze", CLOZE, _set(["gaps", 0, "accept"], []), "gaps[0].accept: braucht 1 bis 12"),
    ("cloze", CLOZE, _set(["text_en"], "hosts: [[ziel]]"), "text_en: Lücke 'state' kommt im Text nicht als [[state]] vor"),
    ("cloze", CLOZE, _set(["text_de"], "hosts: [[ziel]] [[state]] [[port]]"), "text_de: Platzhalter [[port]] hat keine Lücke"),
    ("cloze", CLOZE, _set(["gaps", 1, "id"], "ziel"), "gaps[1].id: 'ziel' doppelt"),
    ("scenario", SCENARIO, _set(["start"], "anfang"), "start: unbekannter Knoten 'anfang'"),
    ("scenario", SCENARIO, _set(["nodes", 0, "options", 1, "to"], "nirgendwo"), "nodes[0].options[1].to: unbekannter Zielknoten 'nirgendwo'"),
    ("scenario", SCENARIO, _set(["nodes", 0, "options", 1, "to"], "b"), "nodes[3]: 'schlecht' ist vom Start aus nicht erreichbar"),
    ("scenario", SCENARIO, _set(["nodes", 1, "options"], [{"label": "Zurück", "to": "a"}, {"label": "Im Kreis", "to": "b"}]),
     "nodes[2]: 'gut' ist vom Start aus nicht erreichbar"),
    ("scenario", SCENARIO, _set(["nodes", 2, "outcome"], "super"), "nodes[2].outcome: 'super' ist nicht erlaubt"),
    ("scenario", SCENARIO, _set(["nodes", 2, "options"], []), "nodes[2]: braucht genau eines von options"),
    ("scenario", SCENARIO, _set(["nodes", 0, "options"], [{"label": "nur eine", "to": "b"}]), "nodes[0].options: braucht 2 bis 4"),
]


@pytest.mark.parametrize("block_type,template,change,expected", INVALID, ids=[c[3][:48] for c in INVALID])
def test_author_errors_name_the_field(block_type, template, change, expected):
    with pytest.raises(ValueError) as err:
        validate_block(block_type, _broken(template, change))
    assert expected in str(err.value)


def test_scenario_rejects_endless_loop():
    """Alle Knoten sind erreichbar, aber aus der Schleife a<->b führt kein Weg zu einem Ende."""
    loop = {"title": "Schleife", "start": "a", "nodes": [
        {"id": "a", "text": "A", "options": [{"label": "zu b", "to": "b"}, {"label": "Ende", "to": "c"}]},
        {"id": "b", "text": "B", "options": [{"label": "zu d", "to": "d"}, {"label": "auch d", "to": "d"}]},
        {"id": "d", "text": "D", "options": [{"label": "zu b", "to": "b"}, {"label": "wieder b", "to": "b"}]},
        {"id": "c", "text": "Ende", "outcome": "ok"}]}
    with pytest.raises(ValueError, match=r"nodes\[1\]: von 'b' aus ist kein Endknoten erreichbar"):
        validate_block("scenario", loop)


@pytest.mark.parametrize("payload", [None, {}, []])
def test_missing_payload_is_rejected(payload):
    for block_type in DECLARATIVE_TYPES:
        with pytest.raises(ValueError, match="payload fehlt"):
            validate_block(block_type, payload)


def test_localize_resolves_language_fields_recursively():
    de = localize(SEQUENCE, "de")
    en = localize(SEQUENCE, "en")
    assert de["title"] == "DORA" and "title_de" not in de
    assert de["messages"][0]["detail"] == "Rundruf" and en["messages"][0]["detail"] == "Broadcast"
    assert en["messages"][1] == {"from": "s", "to": "s", "label": "checks pool"}
    assert localize(COMPARE, "en")["rows"][0]["values"] == ["UDP", "TCP"]
    assert localize(CLOZE, "en")["text"].count("[[") == 2
    assert localize(TERMINAL, "de")["commands"][1]["output"] == ""


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def _module(blocks):
    return {"title_de": "Baukasten", "title_en": "Kit", "order": 98, "prerequisites": [], "goals": [],
            "scenario_de": "S", "scenario_en": "S", "blocks": blocks,
            "quiz": [{"qtype": "single", "prompt_de": "F?", "prompt_en": "Q?",
                      "options_de": ["A", "B"], "options_en": ["A", "B"], "answer": 0}]}


@pytest.fixture
def scratch_module():
    """Legt nichts an, räumt aber die Testmodule wieder ab -- sonst zählen spätere
    Tests (test_content_seed: genau die Seed-Module) ein Modul zu viel."""
    keys = ("baukasten", "baukasten-kaputt")
    yield
    with SessionLocal() as db:
        for model in (ContentBlock, ContentQuizQuestion, ContentModuleSnapshot):
            db.query(model).filter(model.module_key.in_(keys)).delete(synchronize_session=False)
        db.query(ContentModule).filter(ContentModule.key.in_(keys)).delete(synchronize_session=False)
        db.commit()


def test_editor_round_trip_and_localized_delivery(scratch_module):
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "baukasten", "title_de": "Baukasten"}, headers=h)
        blocks = [{"type": t, "payload": p, "note": "Hinweis"} for t, p in VALID]
        assert c.put("/api/trainer/content/modules/baukasten", json=_module(blocks), headers=h).status_code == 200

        # Editor: Payload kommt verlustfrei zurück
        stored = c.get("/api/trainer/content/modules/baukasten", headers=h).json()["blocks"]
        assert [(b["type"], b["payload"]) for b in stored] == VALID

        # Trainer-Ansicht (DE): flach, sprachaufgelöst, mit Notiz und Lösungen
        seen = c.get("/api/trainer/modules/baukasten", headers=h).json()["blocks"]
        assert [b["type"] for b in seen] == [t for t, _ in VALID]
        assert seen[0]["kind"] == "sequence" and seen[0]["messages"][0]["detail"] == "Rundruf"
        assert seen[0]["note"] == "Hinweis"
        assert seen[5]["pairs"][0] == {"left": "DNS", "right": "Namen"}
        assert seen[6]["gaps"][1]["answer"] == 0 and "[[ziel]]" in seen[6]["text"]
        assert seen[7]["nodes"][2]["outcome"] == "good"


def test_editor_rejects_broken_block_with_type_id_and_field(scratch_module):
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "baukasten-kaputt", "title_de": "X"}, headers=h)
        bad = _broken(SEQUENCE, _set(["messages", 0, "to"], "srv"))
        r = c.put("/api/trainer/content/modules/baukasten-kaputt", headers=h,
                  json=_module([{"type": "text", "value_de": "a", "value_en": "b"},
                                {"type": "diagram", "payload": bad}]))
        assert r.status_code == 422
        assert r.json()["detail"] == "diagram-Block '#2': messages[0].to: unbekannter Akteur 'srv'"
        r = c.put("/api/trainer/content/modules/baukasten-kaputt", headers=h,
                  json=_module([{"type": "scenario", "widget_id": "scenario-x", "payload": None}]))
        assert r.status_code == 422 and r.json()["detail"] == "scenario-Block 'scenario-x': payload fehlt"


def test_every_block_type_has_a_demo_in_the_shipped_content():
    """Phase-1-Zusage: je Typ (und je Diagramm-Variante) ein echtes Beispiel mit eigener id."""
    found = {}
    for key, m in MODULES.items():
        for b in m["blocks"]:
            if b["type"] in DECLARATIVE_TYPES:
                assert b.get("id"), f"{key}: {b['type']}-Block ohne id"
                found.setdefault(b["type"] + ":" + b["payload"].get("kind", ""), key)
    assert set(found) >= {"diagram:sequence", "diagram:layers", "diagram:flow", "diagram:compare",
                          "terminal:", "match:", "cloze:", "scenario:"}
