from app.services import grading

QUIZ = {"questions": [
    {"id": "q1", "type": "single", "prompt": "?", "options": ["a", "b"], "answer": "b"},
    {"id": "q2", "type": "multi", "prompt": "?", "options": ["a", "b", "c"], "answer": ["a", "c"]},
    {"id": "q3", "type": "number", "prompt": "?", "answer": 10},
]}


def test_grade_all_correct():
    score, total = grading.grade(QUIZ, {"q1": "b", "q2": ["c", "a"], "q3": 10})
    assert (score, total) == (3, 3)


def test_grade_partial_and_wrong_types():
    score, total = grading.grade(QUIZ, {"q1": "a", "q2": ["a"], "q3": 10})
    assert (score, total) == (1, 3)


def test_passed_threshold():
    assert grading.passed(2, 3, 0.7) is False
    assert grading.passed(3, 3, 0.7) is True
    assert grading.passed(0, 0, 0.7) is False
