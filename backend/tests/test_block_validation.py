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
from tests.conftest import put_module

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
# Erweiterungen (alle Felder optional): je Blocktyp ein Beispiel, das sie zusammen nutzt
SEQUENCE_X = {**SEQUENCE, "messages": [
    {"from": "c", "to": "s", "label": "Hello", "style": "multicast", "at": "0 s",
     "divider_de": "Wartezeit", "divider_en": "Timeout"},
    {"from": "s", "to": "c", "label": "Hello", "at_de": "30 s", "at_en": "30 s"}],
    "actors": [*SEQUENCE["actors"], {"id": "r", "label": "Router"}]}
SEQUENCE_X["messages"].append({"from": "c", "to": ["s", "r"], "label": "an alle Router"})
FLOW_X = {**FLOW, "edges": [{"id": "link", "from": "pc", "to": "sw", "label": "hin"},
                            {"from": "pc", "to": "sw", "label": "doppelt"},
                            {"from": "sw", "to": "pc", "label": "zurück"}]}
COMPARE_X = {**COMPARE, "rows": [{"label": "Befehl", "mono": True, "values": ["show aaa", "show tacacs"],
                                  "detail_de": "Anzeige", "detail_en": "Display"}]}
TERMINAL_X = {
    "prompt": "PC>", "wrap": False,
    "commands": [{"cmd": "ping 10.0.0.1", "output": "Reply", "sets": ["pinged"], "label_de": "Ping", "label_en": "ping"},
                 {"cmd": "arp -a", "output": "(leer)", "variants": [{"when": "pinged", "output_de": "10.0.0.1 da", "output_en": "10.0.0.1 present"}]},
                 {"cmd": "arp -d \\*", "output": "", "clears": ["pinged"]},
                 {"cmd": "show wide", "output": "x" * 120}],
    "tasks": [{"text": "Leeren", "command": "arp -d \\*", "explanation_de": "Cache leer", "explanation_en": "Cache empty"}],
}
CLOZE_X = {"prompt": "Ergänze", "text": "[[a]] und [[b]] und [[c]]",
           "options_de": ["eins", "zwei", "drei"], "options_en": ["one", "two", "three"],
           "gaps": [{"id": "a", "answer": 0}, {"id": "b", "answer": [1, 2]},
                    {"id": "c", "options": ["x", "y", "z"], "answer": [0, 2]}]}
SCENARIO_X = {**SCENARIO, "nodes": [
    {**SCENARIO["nodes"][0], "options": [{"label": "x" * 180, "to": "b"}, {"label": "Neustart", "to": "schlecht"}]},
    *SCENARIO["nodes"][1:]]}
EXTENDED = [("diagram", SEQUENCE_X), ("diagram", FLOW_X), ("diagram", COMPARE_X), ("terminal", TERMINAL_X),
            ("cloze", CLOZE_X), ("scenario", SCENARIO_X)]
VALID = [("diagram", SEQUENCE), ("diagram", LAYERS), ("diagram", FLOW), ("diagram", COMPARE),
         ("terminal", TERMINAL), ("match", MATCH), ("cloze", CLOZE), ("scenario", SCENARIO)] + EXTENDED


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
    # Erweiterungen
    ("diagram", SEQUENCE_X, _set(["messages", 2, "to"], ["s", "x"]), "messages[2].to: unbekannter Akteur 'x'"),
    ("diagram", SEQUENCE_X, _set(["messages", 2, "to"], ["s", "c"]), "messages[2].to: als Liste: 2 bis 4 verschiedene Empfänger"),
    ("diagram", SEQUENCE_X, _set(["messages", 2, "to"], ["s"]), "messages[2].to: als Liste: 2 bis 4 verschiedene Empfänger"),
    ("terminal", TERMINAL_X, _set(["commands", 0, "label_de"], "x" * 33), "commands[0].label_de: zu lang (33 > 32"),
    ("diagram", SEQUENCE_X, _set(["messages", 0, "at"], "nach 30 s"), "messages[0].at: zu lang (9 > 8"),
    ("diagram", SEQUENCE_X, _drop(["messages", 0, "divider_en"]), "messages[0].divider: DE und EN"),
    ("diagram", SEQUENCE_X, _set(["messages", 0, "divider"], "x"), "messages[0].divider: entweder divider oder"),
    ("diagram", SEQUENCE_X, _set(["messages", 1, "note"], "x"), "messages[1].note: unbekanntes Feld"),
    ("diagram", COMPARE_X, _set(["rows", 0, "mono"], "ja"), "rows[0].mono: muss true/false sein"),
    ("diagram", COMPARE_X, _drop(["rows", 0, "detail_en"]), "rows[0].detail: DE und EN"),
    ("diagram", COMPARE_X, _set(["columns", 0, "mono"], True), "columns[0].mono: unbekanntes Feld"),
    ("terminal", TERMINAL_X, _set(["wrap"], "nein"), "wrap: muss true/false sein"),
    ("terminal", TERMINAL_X, _set(["commands", 3, "output"], "ok\n" + "x" * 121), "commands[3].output: Zeile zu lang (121 > 120"),
    ("terminal", TERMINAL_X, _set(["commands", 0, "sets"], "pinged"), "commands[0].sets: braucht 1 bis 4 verschiedene Flag-Namen"),
    ("terminal", TERMINAL_X, _set(["commands", 0, "sets"], ["Pinged!"]), "commands[0].sets: braucht 1 bis 4 verschiedene Flag-Namen"),
    ("terminal", TERMINAL_X, _set(["commands", 1, "variants", 0, "when"], "pingt"), "commands[1].variants[0].when: Flag 'pingt' wird von keinem Befehl gesetzt"),
    ("terminal", TERMINAL_X, _drop(["commands", 1, "variants", 0, "output_en"]), "commands[1].variants[0].output: fehlt"),
    ("terminal", TERMINAL_X, _set(["commands", 1, "variants", 0, "prompt"], "x"), "commands[1].variants[0].prompt: unbekanntes Feld"),
    ("terminal", TERMINAL_X, _set(["commands", 1, "variants"], []), "commands[1].variants: braucht 1 bis 4"),
    ("terminal", TERMINAL_X, _set(["commands", 2, "clears"], ["weg"]), "commands[2].clears: Flag 'weg' wird von keinem Befehl gesetzt"),
    ("terminal", TERMINAL_X, _drop(["tasks", 0, "explanation_en"]), "tasks[0].explanation: DE und EN"),
    ("terminal", TERMINAL_X, _set(["tasks", 0, "command"], "arp -d *"), "tasks[0].command: 'arp -d *' ist kein cmd/alias"),
    ("terminal", TERMINAL_X, _set(["tasks", 0, "hint"], "x"), "tasks[0].hint: unbekanntes Feld"),
    ("cloze", CLOZE_X, _set(["options_en"], ["one", "two"]), "options: options_de und options_en müssen gleich lang"),
    ("cloze", CLOZE_X, _set(["gaps", 0, "answer"], 3), "gaps[0].answer: muss gültiger Options-Index"),
    ("cloze", CLOZE_X, _drop(["gaps", 0, "answer"]), "gaps[0].answer: muss gültiger Options-Index"),
    ("cloze", CLOZE_X, _set(["gaps", 1, "answer"], []), "gaps[1].answer: muss gültiger Options-Index"),
    ("cloze", CLOZE_X, _set(["gaps", 1, "answer"], [1, 1]), "gaps[1].answer: Liste gültiger Optionen"),
    ("cloze", CLOZE_X, _set(["gaps", 2, "answer"], [0, 1, 2]), "gaps[2].answer: Liste gültiger Optionen"),
    ("cloze", CLOZE_X, _set(["gaps", 1, "answer"], [1, True]), "gaps[1].answer: muss gültiger Options-Index"),
    ("cloze", CLOZE, _set(["gaps", 0], {"id": "ziel", "answer": 0}), "gaps[0]: braucht genau eines von options (+ answer) oder accept"),
    ("scenario", SCENARIO_X, _set(["nodes", 0, "options", 0, "label"], "x" * 181), "nodes[0].options[0].label: zu lang (181 > 180"),
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


def test_all_length_errors_of_a_block_are_reported_together():
    """DE und EN zu lang, dazu ein weiteres Feld und ein Strukturfehler: alles in einer Meldung."""
    bad = _broken(SCENARIO, lambda d: (
        d["nodes"][0]["options"][0].pop("label"),
        d["nodes"][0]["options"][0].update(label_de="d" * 181, label_en="e" * 190),
        d.update(title="t" * 91),
        d["nodes"][2].update(outcome="super")))
    with pytest.raises(ValueError) as err:
        validate_block("scenario", bad)
    for part in ("nodes[0].options[0].label_de: zu lang (181 > 180 Zeichen)",
                 "nodes[0].options[0].label_en: zu lang (190 > 180 Zeichen)", "title: zu lang (91 > 90 Zeichen)",
                 "nodes[2].outcome: 'super' ist nicht erlaubt"):
        assert part in str(err.value)
    validate_block("scenario", SCENARIO)  # die Sammlung ist je Aufruf frisch


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
        assert put_module(c, "/api/trainer/content/modules/baukasten", json=_module(blocks), headers=h).status_code == 200

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
        # neue optionale Felder: sprachaufgelöst und vollständig ausgeliefert
        assert seen[8]["messages"][0] == {"from": "c", "to": "s", "label": "Hello", "style": "multicast",
                                          "at": "0 s", "divider": "Wartezeit"}
        assert seen[10]["rows"][0]["mono"] is True and seen[10]["rows"][0]["detail"] == "Anzeige"
        assert seen[11]["wrap"] is False and seen[11]["commands"][0]["sets"] == ["pinged"]
        assert seen[11]["commands"][1]["variants"] == [{"when": "pinged", "output": "10.0.0.1 da"}]
        assert seen[11]["tasks"][0]["explanation"] == "Cache leer"
        assert seen[12]["options"] == ["eins", "zwei", "drei"] and seen[12]["gaps"][1] == {"id": "b", "answer": [1, 2]}


def test_editor_rejects_broken_block_with_type_id_and_field(scratch_module):
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "baukasten-kaputt", "title_de": "X"}, headers=h)
        bad = _broken(SEQUENCE, _set(["messages", 0, "to"], "srv"))
        r = put_module(c, "/api/trainer/content/modules/baukasten-kaputt", headers=h,
                  json=_module([{"type": "text", "value_de": "a", "value_en": "b"},
                                {"type": "diagram", "payload": bad}]))
        assert r.status_code == 422
        assert r.json()["detail"] == "diagram-Block '#2': messages[0].to: unbekannter Akteur 'srv'"
        r = put_module(c, "/api/trainer/content/modules/baukasten-kaputt", headers=h,
                  json=_module([{"type": "scenario", "widget_id": "scenario-x", "payload": None}]))
        assert r.status_code == 422 and r.json()["detail"] == "scenario-Block 'scenario-x': payload fehlt"


def _paths(node, path=()):
    if path:
        yield path
    for k, v in (node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else ()):
        yield from _paths(v, (*path, k))


def test_wrong_json_types_are_validation_errors_never_crashes():
    """Jedes Feld jedes Blocktyps mit falschem JSON-Typ: ValueError (-> 422) mit
    Feldpfad, nie TypeError/KeyError (-> 500) und nie nur das Auffangnetz."""
    from app.services.block_validation import UNEXPECTED_TYPE
    shipped = [(b["type"], b["payload"]) for m in MODULES.values() for b in m["blocks"] if b["type"] in DECLARATIVE_TYPES]
    seen = set()
    for block_type, payload in [*VALID, *shipped]:
        for path in _paths(payload):
            shape = (block_type, payload.get("kind"), tuple("[]" if isinstance(k, int) else k for k in path))
            if shape in seen:  # dieselbe Feldposition einmal je Typ genügt
                continue
            seen.add(shape)
            for wrong in (None, 5, 1.5, True, "x", "", [], {}, [[1]], {"a": 1}, ["x", "x"], [None]):
                broken = copy.deepcopy(payload)
                node = broken
                for k in path[:-1]:
                    node = node[k]
                node[path[-1]] = wrong
                try:
                    validate_block(block_type, broken)
                except ValueError as err:
                    assert UNEXPECTED_TYPE not in str(err), (shape, wrong)
    assert {s[0] for s in seen} == DECLARATIVE_TYPES and len(seen) > 100


def test_editor_answers_422_for_wrong_json_type(scratch_module):
    with TestClient(app, raise_server_exceptions=False) as c:
        h = _trainer(c)
        c.post("/api/trainer/content/modules", json={"key": "baukasten-kaputt", "title_de": "X"}, headers=h)
        for payload, detail in ((_broken(FLOW, _set(["nodes", 0, "shape"], ["host"])), "nodes[0].shape"),
                                (_broken(TERMINAL, _set(["tasks"], 5)), "tasks: muss eine Liste sein"),
                                (_broken(FLOW, _set(["edges"], 5)), "edges: muss eine Liste sein")):
            block_type = "terminal" if payload.get("prompt") else "diagram"
            r = put_module(c, "/api/trainer/content/modules/baukasten-kaputt", headers=h,
                           json=_module([{"type": block_type, "payload": payload}]))
            assert r.status_code == 422 and detail in r.json()["detail"], r.text


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
