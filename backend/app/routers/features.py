from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.deps import get_trainer
from app.services.features import comments_enabled, set_comments_enabled

router = APIRouter(tags=["features"])


@router.get("/features")
def get_features(db: Session = Depends(get_db)):
    return {"comments": comments_enabled(db)}


class FeatureReq(BaseModel):
    comments: bool


@router.put("/trainer/features")
def put_features(data: FeatureReq, db: Session = Depends(get_db), _t: dict = Depends(get_trainer)):
    set_comments_enabled(db, data.comments)
    return {"comments": comments_enabled(db)}
