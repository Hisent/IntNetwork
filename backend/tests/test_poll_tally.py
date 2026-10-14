"""Abstimmungsarten: Prüfung und Auswertung als reine Funktionen (services/poll_tally.py)."""
import pytest

from app.services.poll_tally import TEXT_MAX, normalize_word, parse_answer, tally, text_answers, word_moderation


def bad(*args, **kw):
    with pytest.raises(ValueError):
        parse_answer(*args, **kw)


def test_single():
    assert parse_answer("single", 2, 3) == 2
    for raw in (3, -1, True, "1", [1], None):
        bad("single", raw, 3)


def test_multi_sortiert_entdoppelt_und_begrenzt():
    assert parse_answer("multi", [2, 0, 2], 4) == [0, 2]
    assert parse_answer("multi", [0, 1, 2, 3], 4) == [0, 1, 2, 3]  # ohne Höchstzahl: alle
    assert parse_answer("multi", [1, 3], 4, max_selections=2) == [1, 3]
    bad("multi", [0, 1, 2], 4, max_selections=2)
    for raw in ([], [4], [-1], [True], 1, "0"):
        bad("multi", raw, 4)


def test_scale():
    assert parse_answer("scale", 0, lo=0, hi=10) == 0
    assert parse_answer("scale", 5) == 5
    for raw in (0, 6, True, 2.5, "3"):
        bad("scale", raw)


def test_text_normalisiert_leerraum_und_kappt():
    assert parse_answer("text", "  zu   viel\n Broadcast ") == "zu viel Broadcast"
    assert parse_answer("text", "x" * TEXT_MAX) == "x" * TEXT_MAX
    for raw in ("", "   ", "x" * (TEXT_MAX + 1), 3, ["a"]):
        bad("text", raw)


def test_words_normalisiert_und_begrenzt():
    assert normalize_word("  Load \t Balancer ") == "load balancer"
    assert normalize_word("Straße") == "straße"
    assert parse_answer("words", ["VLAN", " vlan ", "", "Trunk"]) == ["vlan", "trunk"]
    for raw in ([], ["", " "], ["a", "b", "c", "d"], ["x" * 31], "vlan", [1]):
        bad("words", raw)


def test_unbekannte_art():
    bad("umfrage", 1)
    with pytest.raises(ValueError):
        tally("single", [])


def test_tally_multi_ignoriert_kaputte_werte():
    assert tally("multi", [[0, 1], [1], [7], "x"], options=3) == {"counts": [1, 2, 0], "votes": 4}


def test_tally_scale_verteilung_und_mittelwert():
    assert tally("scale", [1, 2, 2, 5, 9], lo=1, hi=5) == {"counts": [1, 2, 0, 0, 1], "votes": 4, "mean": 2.5}
    assert tally("scale", [], lo=0, hi=2) == {"counts": [0, 0, 0], "votes": 0, "mean": None}
    assert tally("scale", [1, 2, 2], lo=1, hi=3)["mean"] == 1.67


def test_tally_words_zaehlt_und_sortiert():
    out = tally("words", [["vlan", "trunk"], ["vlan"], ["acl", "trunk"], ["vlan"]])
    assert out == {"votes": 4, "words": [{"word": "vlan", "count": 3}, {"word": "trunk", "count": 2},
                                         {"word": "acl", "count": 1}]}
    assert len(tally("words", [[f"w{i}"] for i in range(100)])["words"]) == 60


def test_text_answers_alphabetisch_und_nur_sichtbare_fuer_teilnehmer():
    rows = [(5, "zebra", False), (2, "Apfel", True), (9, "birne", False)]
    assert text_answers(rows, moderator=True) == {"votes": 3, "answers": [
        {"id": 9, "text": "birne"}, {"id": 5, "text": "zebra"}], "moderation": [
        {"id": 2, "text": "Apfel", "hidden": True}, {"id": 9, "text": "birne", "hidden": False},
        {"id": 5, "text": "zebra", "hidden": False}]}
    assert text_answers(rows, moderator=False) == {"votes": 3, "answers": [{"text": "birne"}, {"text": "zebra"}]}


def test_ausgeblendetes_wort_zaehlt_nirgends():
    values = [["vlan", "mist"], ["mist"], ["trunk"]]
    out = tally("words", values, hidden_words=frozenset({"mist"}))
    assert out == {"votes": 3, "words": [{"word": "trunk", "count": 1}, {"word": "vlan", "count": 1}]}
    assert word_moderation(values, frozenset({"mist"})) == [
        {"word": "mist", "count": 2, "hidden": True}, {"word": "trunk", "count": 1, "hidden": False},
        {"word": "vlan", "count": 1, "hidden": False}]
