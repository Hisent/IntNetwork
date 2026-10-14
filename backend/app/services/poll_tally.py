"""Live-Abstimmung: Antworten prüfen und auswerten — reine Funktionen ohne DB.

Arten: single (Bestand, Quiz/Check), multi, scale, text, words. Die Auswertung
liefert nur Summen bzw. Texte, nie eine Zuordnung zu Teilnehmern.
"""
from collections import Counter

TEXT_MAX = 280     # Zeichen je Freitext-Antwort
WORD_MAX = 30      # Zeichen je Wort der Wortwolke
WORDS_MAX = 3      # Wörter je Teilnehmer
CLOUD_MAX = 60     # meistgenannte Wörter, die die Wolke zeigt


def _int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def normalize_word(raw: str) -> str:
    """Groß/klein und Leerraum vereinheitlichen: „ Load  Balancer“ = „load balancer“.
    lower() statt casefold(): sonst würde aus „Straße“ „strasse“."""
    return " ".join(raw.split()).lower()


def parse_answer(kind: str, raw, options: int = 0, max_selections: int | None = None,
                 lo: int = 1, hi: int = 5):
    """Prüft eine Teilnehmer-Antwort und liefert den zu speichernden Wert.
    ValueError mit Meldung, wenn sie nicht zur Art passt."""
    if kind == "single":
        if not _int(raw) or not 0 <= raw < options:
            raise ValueError("Ungültige Auswahl")
        return raw
    if kind == "multi":
        if not isinstance(raw, list) or not all(_int(i) and 0 <= i < options for i in raw):
            raise ValueError("Ungültige Auswahl")
        picked = sorted(set(raw))
        if not 1 <= len(picked) <= (max_selections or options):
            raise ValueError("Ungültige Anzahl an Antworten")
        return picked
    if kind == "scale":
        if not _int(raw) or not lo <= raw <= hi:
            raise ValueError("Wert außerhalb der Skala")
        return raw
    if kind == "text":
        text = " ".join(raw.split()) if isinstance(raw, str) else ""
        if not 1 <= len(text) <= TEXT_MAX:
            raise ValueError(f"Antwort leer oder länger als {TEXT_MAX} Zeichen")
        return text
    if kind == "words":
        if not isinstance(raw, list) or not all(isinstance(w, str) for w in raw):
            raise ValueError("Ungültige Wörter")
        words = list(dict.fromkeys(w for w in map(normalize_word, raw) if w))  # doppelt zählt einmal
        if not 1 <= len(words) <= WORDS_MAX or any(len(w) > WORD_MAX for w in words):
            raise ValueError(f"1 bis {WORDS_MAX} Wörter mit je höchstens {WORD_MAX} Zeichen")
        return words
    raise ValueError("Unbekannte Art")


def tally(kind: str, values: list, options: int = 0, lo: int = 1, hi: int = 5) -> dict:
    """Ergebnis für multi/scale/words aus den gespeicherten Werten.
    Werte, die (etwa nach einer Inhaltsänderung) nicht mehr passen, zählen nicht."""
    if kind == "multi":
        counts = [0] * options
        for picked in values:
            for i in picked if isinstance(picked, list) else []:
                if _int(i) and 0 <= i < options:
                    counts[i] += 1
        return {"counts": counts, "votes": len(values)}
    if kind == "scale":
        valid = [v for v in values if _int(v) and lo <= v <= hi]
        counts = [0] * (hi - lo + 1)
        for v in valid:
            counts[v - lo] += 1
        return {"counts": counts, "votes": len(valid),
                "mean": round(sum(valid) / len(valid), 2) if valid else None}
    if kind == "words":
        counter = Counter(w for words in values if isinstance(words, list) for w in words if isinstance(w, str))
        top = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:CLOUD_MAX]
        return {"words": [{"word": w, "count": n} for w, n in top], "votes": len(values)}
    raise ValueError("Unbekannte Art")


def text_answers(rows: list[tuple[int, str, bool]], moderator: bool) -> dict:
    """Freitexte (id, text, hidden). Alphabetisch statt in Abgabe-Reihenfolge —
    die Reihenfolge verriete sonst, wer wann geschrieben hat. Der Trainer bekommt
    alle samt id (zum Ausblenden), Teilnehmer nur die sichtbaren, ohne id."""
    rows = sorted((r for r in rows if isinstance(r[1], str)), key=lambda r: (r[1].lower(), r[0]))
    answers = ([{"id": i, "text": text, "hidden": hidden} for i, text, hidden in rows] if moderator
               else [{"text": text} for _i, text, hidden in rows if not hidden])
    return {"answers": answers, "votes": len(rows)}
