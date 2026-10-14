"""Wiederholung (spaced review): welche Quizfragen für einen Teilnehmer dran sind.

Reine Logik ohne DB (tests/test_review.py); die Daten sammelt routers/review.py.

1. Kandidaten: Fragen aus Modulen des Kurses, deren Wissenscheck der Teilnehmer
   bestanden hat (Progress.done), und zwar vor mindestens MIN_AGE. Damit greift
   die Regel auch in eintägigen Kursen (Vormittag -> Nachmittag), am Folgetag
   sowieso.
2. Leitner-Kästen: `streak` = richtige Wiederholungen in Folge. Eine nie
   wiederholte Frage ist fällig; sonst, sobald last_reviewed + INTERVALS[streak]
   vergangen ist. Richtig -> streak + 1 (nächster, längerer Abstand), falsch ->
   streak 0 (nach INTERVALS[0] wieder fällig: so lange, bis sie sitzt). Nur eine
   FÄLLIGE Antwort zählt — "Nochmal" direkt nach einem Fehler bewertet zwar,
   rückt die Frage aber nicht vor.
3. Reihenfolge der fälligen: zuerst Fragen mit Fehler (in irgendeiner
   Quiz-Abgabe oder in der letzten Wiederholung), dann der Rest; innerhalb
   jeweils am längsten nicht gesehen zuerst (gesehen = letzte Wiederholung,
   sonst Modulabschluss), Gleichstand zufällig.
4. Ein Satz = die ersten SET_SIZE davon. Schreibt nie Progress/QuizResult.
"""
import random
from dataclasses import dataclass
from datetime import datetime, timedelta

SET_SIZE = 8
MIN_AGE = timedelta(hours=3)
# ponytail: feste Leitner-Abstände für alle (Kasten 0..4, darüber bleibt es bei
# Kasten 4); 20 h statt 24 h, damit "gestern geübt" am nächsten Morgen dran ist.
# Pro-Frage-Schwierigkeit (SM-2/FSRS) erst, wenn Kurse über Wochen laufen.
INTERVALS = (timedelta(minutes=10), timedelta(hours=20), timedelta(days=3),
             timedelta(days=7), timedelta(days=21))
# Eine vergessene Aufwärmrunde soll nicht tagelang als Banner stehen bleiben.
WARMUP_MAX_AGE = timedelta(hours=4)


@dataclass(frozen=True)
class Candidate:
    qid: int
    completed_at: datetime          # Abschluss des Moduls
    last_reviewed: datetime | None  # None = nie wiederholt
    streak: int
    wrong: bool                     # Fehler in einer Abgabe oder in der letzten Wiederholung


def is_due(last_reviewed: datetime | None, streak: int, now: datetime) -> bool:
    return last_reviewed is None or now - last_reviewed >= INTERVALS[min(streak, len(INTERVALS) - 1)]


def next_streak(streak: int, correct: bool) -> int:
    return streak + 1 if correct else 0


def due_in_order(candidates: list[Candidate], now: datetime, rng: random.Random | None = None) -> list[int]:
    """Alle fälligen Frage-ids, wichtigste zuerst (Regel 3)."""
    due = [c for c in candidates if is_due(c.last_reviewed, c.streak, now)]
    (rng or random).shuffle(due)  # Gleichstand zufällig; sort ist stabil
    due.sort(key=lambda c: (not c.wrong, c.last_reviewed or c.completed_at))
    return [c.qid for c in due]
