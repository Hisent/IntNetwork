from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.audit import log_action
from app.services.deps import get_trainer
from app.services.features import comments_enabled, set_comments_enabled

router = APIRouter(tags=["features"])


@router.get("/features")
def get_features(db: Session = Depends(get_db)):
    return {"comments": comments_enabled(db)}


class FeatureReq(BaseModel):
    comments: bool


@router.put("/trainer/features")
def put_features(data: FeatureReq, db: Session = Depends(get_db), trainer: dict = Depends(get_trainer)):
    set_comments_enabled(db, data.comments)
    log_action(db, trainer, "feature.toggle", target="comments", detail=f"comments={data.comments}")
    return {"comments": comments_enabled(db)}
