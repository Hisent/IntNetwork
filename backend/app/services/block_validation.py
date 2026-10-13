"""Validierung und Sprachauflösung der deklarativen Blocktypen
(diagram, terminal, match, cloze, scenario) -- Autorenreferenz: docs/content-authoring.md.

Jedes Textfeld X darf sprachneutral als `X` ODER zweisprachig als `X_de` + `X_en`
im Payload stehen. `localize` löst das für die Auslieferung zu `X` auf;
`validate_block` wirft ValueError mit Feldpfad (der Aufrufer ergänzt Blocktyp und id).
Längenfehler werden je Block gesammelt und gemeinsam gemeldet (mit `; ` getrennt) --
wer DE kürzt, soll nicht erst im nächsten Lauf erfahren, dass EN auch zu lang ist.
"""
import re
from contextvars import ContextVar

# Sammelstelle der Längenfehler des gerade geprüften Blocks (je Aufruf von validate_block neu)
_too_long: ContextVar[list[str]] = ContextVar("too_long")

DECLARATIVE_TYPES = {"diagram", "terminal", "match", "cloze", "scenario"}

SEQ_STYLES = {"request", "reply", "broadcast", "multicast", "encrypted"}
FLOW_SHAPES = {"host", "switch", "router", "firewall", "server", "cloud", "database", "user",
               "process", "decision"}
UNEXPECTED_TYPE = "ungültiger Datentyp im Payload (Feld nicht eingrenzbar)"
ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
# [[id]] statt {{id}}: Jinja-/Ansible-Beispiele enthalten selbst {{ var }}
GAP_RE = re.compile(r"\[\[([a-z0-9][a-z0-9_-]*)\]\]")


def localize(value, lang: str):
    """`X_de`/`X_en` -> `X` in der gewünschten Sprache, rekursiv."""
    if isinstance(value, list):
        return [localize(v, lang) for v in value]
    if not isinstance(value, dict):
        return value
    out = {}
    for k, v in value.items():
        if k.endswith(("_de", "_en")):
            base = k[:-3]
            if base not in out:
                out[base] = localize(value.get(f"{base}_{lang}", v), lang)
        else:
            out[k] = localize(v, lang)
    return out


def _fail(where: str, msg: str):
    raise ValueError(f"{where}: {msg}")


def _obj(value, where: str, allowed: set[str]) -> dict:
    """Objekt mit bekannten Feldern -- ein vertipptes Feld (details_de) fiele sonst lautlos weg."""
    if not isinstance(value, dict):
        _fail(where, "muss ein Objekt sein")
    for k in value:
        base = k[:-3] if k.endswith(("_de", "_en")) else k
        if base not in allowed:
            _fail(f"{where}.{k}" if where else k, "unbekanntes Feld")
    return value


def _join(where: str, name: str) -> str:
    return f"{where}.{name}" if where else name


def _text(d: dict, name: str, where: str, required: bool = True, max_len: int | None = None) -> bool:
    """Prüft `name` bzw. `name_de`+`name_en`; gibt zurück, ob das Feld gesetzt ist."""
    path = _join(where, name)
    neutral, de, en = d.get(name), d.get(f"{name}_de"), d.get(f"{name}_en")
    if neutral is not None and (de is not None or en is not None):
        _fail(path, f"entweder {name} oder {name}_de/{name}_en, nicht beides")
    values = [neutral] if neutral is not None else [de, en]
    if neutral is None and de is None and en is None:
        if required:
            _fail(path, f"fehlt ({name} oder {name}_de + {name}_en)")
        return False
    for v in values:
        if not isinstance(v, str) or not v.strip():
            _fail(path, "DE und EN müssen beide nichtleerer Text sein")
    for suffix, v in zip([""] if neutral is not None else ["_de", "_en"], values, strict=True):
        if max_len and len(v) > max_len:
            _too_long.get().append(f"{path}{suffix}: zu lang ({len(v)} > {max_len} Zeichen)")
    return True


def _text_list(d: dict, name: str, where: str, min_len: int, max_len: int) -> int:
    """Liste nichtleerer Texte, neutral oder DE/EN gleich lang; gibt die Länge zurück."""
    path = _join(where, name)
    neutral, de, en = d.get(name), d.get(f"{name}_de"), d.get(f"{name}_en")
    lists = [neutral] if neutral is not None else [de, en]
    if neutral is not None and (de is not None or en is not None):
        _fail(path, f"entweder {name} oder {name}_de/{name}_en, nicht beides")
    for lst in lists:
        if not isinstance(lst, list) or any(not isinstance(v, str) or not v.strip() for v in lst):
            _fail(path, "braucht eine Liste nichtleerer Texte (DE und EN)")
    if len({len(lst) for lst in lists}) > 1:
        _fail(path, f"{name}_de und {name}_en müssen gleich lang sein")
    n = len(lists[0])
    if not (min_len <= n <= max_len):
        _fail(path, f"braucht {min_len} bis {max_len} Einträge (hat {n})")
    return n


def _items(d: dict, name: str, where: str, min_len: int, max_len: int) -> list:
    items = d.get(name)
    path = _join(where, name)
    if not isinstance(items, list):
        _fail(path, "fehlt oder ist keine Liste")
    if not (min_len <= len(items) <= max_len):
        _fail(path, f"braucht {min_len} bis {max_len} Einträge (hat {len(items)})")
    return items


def _id(d: dict, where: str, seen: set[str], name: str = "id") -> str:
    value = d.get(name)
    if not isinstance(value, str) or not ID_RE.match(value):
        _fail(f"{where}.{name}", "fehlt oder ist kein kebab-case-Bezeichner (a-z, 0-9, -, _)")
    if value in seen:
        _fail(f"{where}.{name}", f"'{value}' doppelt vergeben")
    seen.add(value)
    return value


def _choice(d: dict, name: str, where: str, allowed: set[str]) -> None:
    if name in d and (not isinstance(d[name], str) or d[name] not in allowed):
        _fail(_join(where, name), f"'{d[name]}' ist nicht erlaubt (erlaubt: {', '.join(sorted(allowed))})")


def _known(ref, ids: set[str]) -> bool:
    """Verweis auf eine bekannte id -- eine Liste/ein Objekt an der Stelle ist nicht hashbar."""
    return isinstance(ref, str) and ref in ids


def _optional_list(d: dict, name: str, where: str) -> list:
    value = d.get(name, [])
    if not isinstance(value, list):
        _fail(_join(where, name), "muss eine Liste sein")
    return value


def _flag(d: dict, name: str, where: str) -> None:
    if name in d and not isinstance(d[name], bool):
        _fail(_join(where, name), "muss true/false sein")


# --- diagram -----------------------------------------------------------------

def _diagram(pl: dict) -> None:
    kind = pl.get("kind")
    if kind == "sequence":
        _obj(pl, "", {"kind", "title", "caption", "actors", "messages"})
        actors: set[str] = set()
        for i, a in enumerate(_items(pl, "actors", "", 2, 5)):
            w = f"actors[{i}]"
            _obj(a, w, {"id", "label"})
            _id(a, w, actors)
            _text(a, "label", w, max_len=28)
        for i, m in enumerate(_items(pl, "messages", "", 1, 14)):
            w = f"messages[{i}]"
            _obj(m, w, {"from", "to", "label", "detail", "style", "at", "divider"})
            # `to` als Liste = dieselbe Nachricht parallel an mehrere Empfänger
            to = m.get("to")
            if isinstance(to, list) and (not (2 <= len(to) <= 4) or len(set(map(str, to))) != len(to) or m.get("from") in to):
                _fail(f"{w}.to", "als Liste: 2 bis 4 verschiedene Empfänger, ohne den Absender")
            for end, refs in (("from", [m.get("from")]), ("to", to if isinstance(to, list) else [to])):
                for ref in refs:
                    if not isinstance(ref, str) or ref not in actors:
                        _fail(f"{w}.{end}", f"unbekannter Akteur '{ref}'")
            _text(m, "label", w, max_len=70)
            _text(m, "detail", w, required=False)
            _choice(m, "style", w, SEQ_STYLES)
            _text(m, "at", w, required=False, max_len=8)
            _text(m, "divider", w, required=False, max_len=40)
    elif kind == "layers":
        _obj(pl, "", {"kind", "title", "caption", "layers"})
        for i, layer in enumerate(_items(pl, "layers", "", 2, 8)):
            w = f"layers[{i}]"
            _obj(layer, w, {"name", "content", "pdu", "detail"})
            _text(layer, "name", w, max_len=40)
            _text(layer, "content", w, required=False, max_len=120)
            _text(layer, "pdu", w, required=False, max_len=24)
            _text(layer, "detail", w, required=False)
    elif kind == "flow":
        _obj(pl, "", {"kind", "title", "caption", "nodes", "edges", "steps"})
        ids: set[str] = set()
        cells: set[tuple[int, int]] = set()
        for i, n in enumerate(_items(pl, "nodes", "", 2, 14)):
            w = f"nodes[{i}]"
            _obj(n, w, {"id", "label", "shape", "row", "col", "detail"})
            _id(n, w, ids)
            _text(n, "label", w, max_len=40)
            _text(n, "detail", w, required=False)
            _choice(n, "shape", w, FLOW_SHAPES)
            for axis in ("row", "col"):
                v = n.get(axis)
                if isinstance(v, bool) or not isinstance(v, int) or not (0 <= v <= 4):
                    _fail(f"{w}.{axis}", "muss eine ganze Zahl 0 bis 4 sein")
            cell = (n["row"], n["col"])
            if cell in cells:
                _fail(w, f"Rasterzelle row={cell[0]}/col={cell[1]} ist doppelt belegt")
            cells.add(cell)
        nodes = set(ids)
        for i, e in enumerate(_optional_list(pl, "edges", "")):
            w = f"edges[{i}]"
            _obj(e, w, {"id", "from", "to", "label", "detail", "style", "arrow"})
            if "id" in e:
                _id(e, w, ids)
            for end in ("from", "to"):
                if not _known(e.get(end), nodes):
                    _fail(f"{w}.{end}", f"unbekannter Knoten '{e.get(end)}'")
            if e["from"] == e["to"]:
                _fail(w, "Kante von einem Knoten zu sich selbst wird nicht gezeichnet")
            _text(e, "label", w, required=False, max_len=28)
            _text(e, "detail", w, required=False)
            _choice(e, "style", w, {"solid", "dashed"})
            _choice(e, "arrow", w, {"end", "both", "none"})
        if "steps" in pl:
            for i, s in enumerate(_items(pl, "steps", "", 2, 12)):
                w = f"steps[{i}]"
                _obj(s, w, {"highlight", "text"})
                _text(s, "text", w)
                hl = s.get("highlight")
                if not isinstance(hl, list) or not hl:
                    _fail(f"{w}.highlight", "braucht mindestens eine Knoten-/Kanten-id")
                for ref in hl:
                    if not _known(ref, ids):
                        _fail(f"{w}.highlight", f"unbekannte Knoten-/Kanten-id '{ref}'")
    elif kind == "compare":
        _obj(pl, "", {"kind", "title", "caption", "columns", "rows"})
        columns = _items(pl, "columns", "", 2, 4)
        for i, c in enumerate(columns):
            w = f"columns[{i}]"
            _obj(c, w, {"title"})
            _text(c, "title", w, max_len=40)
        for i, r in enumerate(_items(pl, "rows", "", 1, 10)):
            w = f"rows[{i}]"
            _obj(r, w, {"label", "values", "mono", "detail"})
            _text(r, "label", w, max_len=40)
            _flag(r, "mono", w)
            _text(r, "detail", w, required=False)
            _text_list(r, "values", w, len(columns), len(columns))
    else:
        _fail("kind", f"'{kind}' unbekannt (erlaubt: sequence, layers, flow, compare)")
    _text(pl, "title", "", max_len=90)
    _text(pl, "caption", "", required=False)


# --- terminal ----------------------------------------------------------------

def _norm(cmd: str) -> str:
    return " ".join(cmd.split()).lower()


WIDE_LINE = 120  # längste Ausgabezeile bei wrap: false (waagerecht scrollend)


def _flags(d: dict, name: str, where: str) -> list[str]:
    """Liste von Zustands-Flags (sets/clears)."""
    value = d.get(name, [])
    if not isinstance(value, list) or (name in d and not value) or len(value) > 4 \
            or any(not isinstance(f, str) or not ID_RE.match(f) for f in value) or len(set(value)) != len(value):
        _fail(_join(where, name), "braucht 1 bis 4 verschiedene Flag-Namen (a-z, 0-9, -, _)")
    return value


def _output(d: dict, where: str) -> list[str]:
    # leere Ausgabe ist erlaubt (Konfigurationsbefehle antworten nicht), das Feld muss aber da sein
    outs = [d[k] for k in ("output", "output_de", "output_en") if k in d]
    if ("output" in d) == ("output_de" in d or "output_en" in d) or \
            ("output" not in d and len(outs) != 2) or any(not isinstance(o, str) for o in outs):
        _fail(f"{where}.output", "fehlt (output oder output_de + output_en, jeweils Text)")
    return outs


def _terminal(pl: dict) -> None:
    _obj(pl, "", {"title", "prompt", "intro", "unknown", "abbreviations", "case_sensitive", "wrap",
                  "commands", "tasks"})
    _text(pl, "title", "", required=False, max_len=90)
    if not isinstance(pl.get("prompt"), str) or not pl["prompt"].strip():
        _fail("prompt", "fehlt (sprachneutraler Text, z. B. 'Infoblox >')")
    _text(pl, "intro", "", required=False)
    _text(pl, "unknown", "", required=False)
    _flag(pl, "abbreviations", "")
    _flag(pl, "case_sensitive", "")
    _flag(pl, "wrap", "")
    known: set[str] = set()
    settable = {f for c in (pl["commands"] if isinstance(pl.get("commands"), list) else []) if isinstance(c, dict)
                for f in (c.get("sets") if isinstance(c.get("sets"), list) else []) if isinstance(f, str)}
    for i, c in enumerate(_items(pl, "commands", "", 1, 30)):
        w = f"commands[{i}]"
        _obj(c, w, {"cmd", "aliases", "output", "desc", "prompt", "chip", "label", "sets", "clears", "variants"})
        names = [c.get("cmd"), *_optional_list(c, "aliases", w)]
        for name in names:
            if not isinstance(name, str) or not name.strip():
                _fail(f"{w}.cmd", "cmd und aliases müssen nichtleerer Text sein")
            if _norm(name) in known:
                _fail(f"{w}.cmd", f"'{name}' ist doppelt vergeben")
            known.add(_norm(name))
        outputs = [(f"{w}.output", _output(c, w))]
        _flags(c, "sets", w)
        for f in _flags(c, "clears", w):
            if f not in settable:
                _fail(f"{w}.clears", f"Flag '{f}' wird von keinem Befehl gesetzt (sets)")
        if "variants" in c:
            for j, v in enumerate(_items(c, "variants", w, 1, 4)):
                vw = f"{w}.variants[{j}]"
                _obj(v, vw, {"when", "output"})
                if not isinstance(v.get("when"), str) or v["when"] not in settable:
                    _fail(f"{vw}.when", f"Flag '{v.get('when')}' wird von keinem Befehl gesetzt (sets)")
                outputs.append((f"{vw}.output", _output(v, vw)))
        if pl.get("wrap") is False:
            for path, outs in outputs:
                widest = max((len(line) for o in outs for line in o.split("\n")), default=0)
                if widest > WIDE_LINE:
                    _too_long.get().append(f"{path}: Zeile zu lang ({widest} > {WIDE_LINE} Zeichen)")
        _text(c, "desc", w, required=False, max_len=80)
        if "prompt" in c and (not isinstance(c["prompt"], str) or not c["prompt"].strip()):
            _fail(f"{w}.prompt", "muss nichtleerer Text sein")
        _flag(c, "chip", w)
        _text(c, "label", w, required=False, max_len=32)
    tasks = _optional_list(pl, "tasks", "") if pl.get("tasks") is not None else []
    for i, t in enumerate(tasks):
        w = f"tasks[{i}]"
        _obj(t, w, {"text", "command", "answers", "explanation"})
        _text(t, "text", w)
        _text(t, "explanation", w, required=False)
        if ("command" in t) == ("answers" in t):
            _fail(w, "braucht genau eines von command oder answers")
        if "command" in t and (not isinstance(t["command"], str) or _norm(t["command"]) not in known):
            _fail(f"{w}.command", f"'{t['command']}' ist kein cmd/alias aus commands")
        if "answers" in t:
            _text_list(t, "answers", w, 1, 10)
    if len(tasks) > 6:
        _fail("tasks", "höchstens 6 Aufgaben")


# --- match -------------------------------------------------------------------

def _match(pl: dict) -> None:
    _obj(pl, "", {"prompt", "pairs", "explanation"})
    _text(pl, "prompt", "")
    _text(pl, "explanation", "", required=False)
    pairs = _items(pl, "pairs", "", 3, 8)
    for i, p in enumerate(pairs):
        w = f"pairs[{i}]"
        _obj(p, w, {"left", "right"})
        _text(p, "left", w, max_len=60)
        _text(p, "right", w, max_len=160)
    for side in ("left", "right"):
        for lang in ("de", "en"):
            values = [p.get(side, p.get(f"{side}_{lang}")) for p in pairs]
            if len(set(values)) != len(values):
                _fail("pairs", f"{side} ({lang}) enthält doppelte Einträge -- Zuordnung wäre mehrdeutig")


# --- cloze -------------------------------------------------------------------

def _cloze(pl: dict) -> None:
    _obj(pl, "", {"prompt", "text", "mono", "options", "gaps", "explanation"})
    _text(pl, "prompt", "")
    _text(pl, "text", "")
    _text(pl, "explanation", "", required=False)
    _flag(pl, "mono", "")
    shared = any(k in pl for k in ("options", "options_de", "options_en"))
    shared_n = _text_list(pl, "options", "", 2, 8) if shared else 0
    ids: set[str] = set()
    for i, g in enumerate(_items(pl, "gaps", "", 1, 10)):
        w = f"gaps[{i}]"
        _obj(g, w, {"id", "options", "answer", "accept", "case_sensitive", "strict_whitespace"})
        _id(g, w, ids)
        own = any(k in g for k in ("options", "options_de", "options_en"))
        # ohne eigene options/accept gilt die gemeinsame Liste des Blocks (options auf Blockebene)
        has_options = own or (shared and "accept" not in g)
        if has_options == ("accept" in g):
            _fail(w, "braucht genau eines von options (+ answer) oder accept -- eine Lücke ohne Lösung ist nicht prüfbar")
        if has_options:
            n = _text_list(g, "options", w, 2, 6) if own else shared_n
            ans = g.get("answer")
            valid = ans if isinstance(ans, list) else [ans]
            if not valid or any(isinstance(a, bool) or not isinstance(a, int) or not (0 <= a < n) for a in valid):
                _fail(f"{w}.answer", "muss gültiger Options-Index sein (oder eine Liste davon, wenn mehrere Optionen richtig sind)")
            if len(set(valid)) != len(valid) or len(valid) >= n:
                _fail(f"{w}.answer", "Liste gültiger Optionen: keine doppelten, und nicht alle Optionen")
        else:
            _text_list(g, "accept", w, 1, 12)
            _flag(g, "case_sensitive", w)
            _flag(g, "strict_whitespace", w)
    for key in ("text", "text_de", "text_en"):
        if key not in pl:
            continue
        used = GAP_RE.findall(pl[key])
        for ref in used:
            if ref not in ids:
                _fail(key, f"Platzhalter [[{ref}]] hat keine Lücke in gaps")
        for gid in ids:
            if gid not in used:
                _fail(key, f"Lücke '{gid}' kommt im Text nicht als [[{gid}]] vor")


# --- scenario ----------------------------------------------------------------

def _scenario(pl: dict) -> None:
    _obj(pl, "", {"title", "start", "nodes"})
    _text(pl, "title", "", max_len=90)
    ids: set[str] = set()
    nodes = _items(pl, "nodes", "", 2, 24)
    for i, n in enumerate(nodes):
        _obj(n, f"nodes[{i}]", {"id", "text", "options", "outcome"})
        _id(n, f"nodes[{i}]", ids)
    if not _known(pl.get("start"), ids):
        _fail("start", f"unbekannter Knoten '{pl.get('start')}'")
    targets: dict[str, list[str]] = {}
    for i, n in enumerate(nodes):
        w = f"nodes[{i}]"
        _text(n, "text", w)
        if ("options" in n) == ("outcome" in n):
            _fail(w, "braucht genau eines von options (Entscheidung) oder outcome (Endknoten)")
        targets[n["id"]] = []
        if "outcome" in n:
            _choice(n, "outcome", w, {"good", "ok", "bad"})
            continue
        for j, o in enumerate(_items(n, "options", w, 2, 4)):
            ow = f"{w}.options[{j}]"
            _obj(o, ow, {"label", "to"})
            _text(o, "label", ow, max_len=180)
            if not _known(o.get("to"), ids):
                _fail(f"{ow}.to", f"unbekannter Zielknoten '{o.get('to')}'")
            targets[n["id"]].append(o["to"])
    reachable = {pl["start"]}
    todo = [pl["start"]]
    while todo:
        for nxt in targets[todo.pop()]:
            if nxt not in reachable:
                reachable.add(nxt)
                todo.append(nxt)
    for i, n in enumerate(nodes):
        if n["id"] not in reachable:
            _fail(f"nodes[{i}]", f"'{n['id']}' ist vom Start aus nicht erreichbar")
    # Rückwärts von den Endknoten: wer keinen erreicht, hängt in einer Endlosschleife.
    finishes = {n["id"] for n in nodes if "outcome" in n}
    changed = True
    while changed:
        changed = False
        for nid, outs in targets.items():
            if nid not in finishes and any(o in finishes for o in outs):
                finishes.add(nid)
                changed = True
    for i, n in enumerate(nodes):
        if n["id"] not in finishes:
            _fail(f"nodes[{i}]", f"von '{n['id']}' aus ist kein Endknoten erreichbar (Endlosschleife)")


_VALIDATORS = {"diagram": _diagram, "terminal": _terminal, "match": _match,
               "cloze": _cloze, "scenario": _scenario}


def validate_block(block_type: str, payload) -> None:
    if not isinstance(payload, dict) or not payload:
        raise ValueError("payload fehlt")
    errors: list[str] = []
    token = _too_long.set(errors)
    try:
        _VALIDATORS[block_type](payload)
    except ValueError as e:
        errors.append(str(e))
    except (TypeError, KeyError, AttributeError, IndexError):
        # Netz unter den Einzelprüfungen: ein falscher JSON-Typ an unerwarteter
        # Stelle ist ein Eingabefehler (422), kein Serverfehler.
        errors.append(UNEXPECTED_TYPE)
    finally:
        _too_long.reset(token)
    if errors:
        raise ValueError("; ".join(errors))
