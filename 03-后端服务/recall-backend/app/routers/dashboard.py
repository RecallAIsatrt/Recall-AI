"""数据看板路由"""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Mistake, ReviewRecord, Category
from app.schemas import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Mistake).filter(Mistake.is_archived == False).count()
    mastered = db.query(Mistake).filter(
        Mistake.is_archived == False, Mistake.mastery_level >= 0.8
    ).count()
    pending = db.query(Mistake).filter(
        Mistake.is_archived == False, Mistake.review_count == 0
    ).count()

    avg_reviews_result = db.query(func.avg(Mistake.review_count)).filter(
        Mistake.is_archived == False
    ).scalar()
    avg_reviews = round(avg_reviews_result or 0, 1)

    # 学科分布
    subject_dist = {}
    rows = db.query(Mistake.subject, func.count(Mistake.id)).filter(
        Mistake.is_archived == False
    ).group_by(Mistake.subject).all()
    for subject, count in rows:
        subject_dist[subject] = count

    # 薄弱知识点
    weak = (
        db.query(Mistake.knowledge_point, func.count(Mistake.id).label("cnt"))
        .filter(Mistake.is_archived == False, Mistake.mastery_level < 0.5)
        .group_by(Mistake.knowledge_point)
        .order_by(func.count(Mistake.id).desc())
        .limit(5)
        .all()
    )
    weak_points = [{"point": w[0], "count": w[1]} for w in weak if w[0]]

    return DashboardStats(
        total=total,
        mastered=mastered,
        pending=pending,
        avg_reviews=avg_reviews,
        subject_distribution=subject_dist,
        weak_points=weak_points,
    )
