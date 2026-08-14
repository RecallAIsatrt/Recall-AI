"""复习计划路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Mistake
from app.schemas import ReviewSubmit, ReviewOut, MistakeOut
from app.services.review_service import get_today_reviews, submit_review

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/today", response_model=list[MistakeOut])
def today_reviews(db: Session = Depends(get_db)):
    return get_today_reviews(db)


@router.post("/{mistake_id}", response_model=ReviewOut)
def submit(mistake_id: int, data: ReviewSubmit, db: Session = Depends(get_db)):
    try:
        return submit_review(db, mistake_id, data.quality)
    except ValueError as e:
        raise HTTPException(404, str(e))
