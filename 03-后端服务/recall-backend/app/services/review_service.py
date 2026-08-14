"""复习计划服务"""
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Mistake, ReviewRecord
from app.utils.sm2 import sm2, get_mastery_level


def get_today_reviews(db: Session, limit: int = 20) -> list[Mistake]:
    """获取今日待复习错题"""
    now = datetime.utcnow()
    return (
        db.query(Mistake)
        .filter(Mistake.next_review <= now, Mistake.is_archived == False)
        .order_by(Mistake.next_review)
        .limit(limit)
        .all()
    )


def submit_review(db: Session, mistake_id: int, quality: int) -> ReviewRecord:
    """提交复习结果并更新 SM-2 参数"""
    mistake = db.query(Mistake).get(mistake_id)
    if not mistake:
        raise ValueError("错题不存在")

    # 获取最近一次复习记录
    last_review = (
        db.query(ReviewRecord)
        .filter(ReviewRecord.mistake_id == mistake_id)
        .order_by(ReviewRecord.review_at.desc())
        .first()
    )

    easiness = last_review.easiness if last_review else 2.5
    interval = last_review.interval if last_review else 1
    repetition = last_review.repetition if last_review else 0

    result = sm2(quality, easiness, interval, repetition)

    # 创建复习记录
    record = ReviewRecord(
        mistake_id=mistake_id,
        quality=quality,
        easiness=result["easiness"],
        interval=result["interval"],
        repetition=result["repetition"],
    )
    db.add(record)

    # 更新错题
    mistake.review_count += 1
    mistake.next_review = result["next_review"]

    # 计算掌握度
    reviews = db.query(ReviewRecord).filter(ReviewRecord.mistake_id == mistake_id).all()
    avg_q = sum(r.quality for r in reviews) / len(reviews)
    mistake.mastery_level = get_mastery_level(mistake.review_count, avg_q)

    db.commit()
    db.refresh(record)
    return record
