from app.services import grading

QUIZ = {"questions": [
    {"id": "q1", "type": "single", "answer": 1},
    {"id": "q2", "type": "multi", "answer": [0, 2]},
    {"id": "q3", "type": "number", "answer": 24},
]}


def test_single_correct_and_wrong():
    assert grading._correct(QUIZ["questions"][0], 1) is True
    assert grading._correct(QUIZ["questions"][0], 0) is False


def test_multi_ignores_order():
    assert grading._correct(QUIZ["questions"][1], [2, 0]) is True
    assert grading._correct(QUIZ["questions"][1], [0]) is False
    assert grading._correct(QUIZ["questions"][1], "not-a-list") is False


def test_number_tolerates_string_input():
    assert grading._correct(QUIZ["questions"][2], "24") is True
    assert grading._correct(QUIZ["questions"][2], 25) is False
    assert grading._correct(QUIZ["questions"][2], "abc") is False


def test_grade_counts_correct_answers():
    score, total = grading.grade(QUIZ, {"q1": 1, "q2": [0, 2], "q3": 24})
    assert (score, total) == (3, 3)
    score, total = grading.grade(QUIZ, {"q1": 0})
    assert (score, total) == (0, 3)


def test_passed_threshold():
    assert grading.passed(2, 3, 0.6) is True
    assert grading.passed(1, 3, 0.6) is False
    assert grading.passed(0, 0, 0.6) is False


def test_question_results_per_question():
    res = grading.question_results(QUIZ, {"q1": 1, "q2": [2, 0], "q3": 99})
    assert res == {"q1": True, "q2": True, "q3": False}
    # fehlende Antwort -> False, nie KeyError
    assert grading.question_results(QUIZ, {}) == {"q1": False, "q2": False, "q3": False}


def test_question_stats_aggregates_submissions():
    subs = [{"q1": 1, "q2": [0, 2], "q3": 24},   # alles richtig
            {"q1": 0, "q2": [0, 2], "q3": 99},   # nur q2 richtig
            {"q1": 1}]                            # q2/q3 nicht beantwortet -> falsch
    stats = grading.question_stats(QUIZ, subs)
    assert stats == [{"id": "q1", "correct": 2, "attempts": 3},
                     {"id": "q2", "correct": 2, "attempts": 3},
                     {"id": "q3", "correct": 1, "attempts": 3}]
    assert grading.question_stats(QUIZ, []) == [
        {"id": "q1", "correct": 0, "attempts": 0},
        {"id": "q2", "correct": 0, "attempts": 0},
        {"id": "q3", "correct": 0, "attempts": 0}]
