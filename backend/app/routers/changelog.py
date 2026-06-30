from fastapi import APIRouter, Depends

from app.content.changelog import CHANGELOG
from app.services.deps import get_trainer

router = APIRouter(tags=["changelog"])


@router.get("/changelog")
def changelog(_=Depends(get_trainer)):
    return CHANGELOG
