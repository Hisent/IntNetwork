def _correct(question: dict, answer) -> bool:
    t = question["type"]
    if t == "single":
        return answer == question["answer"]
    if t == "multi":
        if not isinstance(answer, list):
            return False
        return sorted(answer) == sorted(question["answer"])
    if t == "number":
        try:
            return float(answer) == float(question["answer"])
        except (TypeError, ValueError):
            return False
    return False


def grade(quiz: dict, answers: dict) -> tuple[int, int]:
    questions = quiz["questions"]
    score = sum(1 for q in questions if _correct(q, (answers or {}).get(q["id"])))
    return score, len(questions)


def question_results(quiz: dict, answers: dict) -> dict[str, bool]:
    """Pro Frage: war die Antwort korrekt? Verraet NICHT die Loesung, nur ob die
    abgegebene Antwort stimmte -> Basis fuer Per-Frage-Feedback im Frontend."""
    return {q["id"]: _correct(q, (answers or {}).get(q["id"])) for q in quiz["questions"]}


def passed(score: int, total: int, threshold: float) -> bool:
    return total > 0 and (score / total) >= threshold
