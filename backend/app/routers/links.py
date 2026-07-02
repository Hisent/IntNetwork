from fastapi import APIRouter

from app.content.links import LINKS

router = APIRouter(tags=["links"])


@router.get("/links")
def links():
    """Kuratierte Vertiefungslinks — bilingual, Client wählt die Sprache."""
    return LINKS
