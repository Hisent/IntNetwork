from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.quiz_result import QuizResult
from app.services import grading
from app.services.deps import get_trainer
from app.content.registry import module_meta, trainer_module

router = APIRouter(prefix="/trainer/modules", tags=["trainer-modules"])


@router.get("")
def list_trainer_modules(db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    return module_meta(db)


@router.get("/{key}")
def get_trainer_module(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    m = trainer_module(db, key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    return m


@router.get("/{key}/quiz-stats")
def quiz_stats(key: str, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    """Pro Quizfrage: wie viele Abgaben waren richtig? Zeigt dem Trainer, welche
    Konzepte hängen. Abgaben zu inzwischen gelöschten/ersetzten Fragen fallen
    stillschweigend raus (IDs matchen nicht mehr)."""
    m = trainer_module(db, key)
    if not m:
        raise HTTPException(status_code=404, detail="Modul nicht gefunden")
    submissions = [r.answers for r in db.query(QuizResult).filter(QuizResult.module_key == key)]
    prompts = {q["id"]: q["prompt"] for q in m["quiz"]["questions"]}
    return {"submissions": len(submissions),
            "questions": [{**s, "prompt": prompts[s["id"]]}
                          for s in grading.question_stats(m["quiz"], submissions)]}
