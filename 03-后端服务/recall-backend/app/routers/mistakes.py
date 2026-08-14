"""错题 CRUD 路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Mistake, Category
from app.schemas import MistakeCreate, MistakeUpdate, MistakeOut
from app.services.ai_service import analyze_mistake

router = APIRouter(prefix="/mistakes", tags=["mistakes"])


@router.get("", response_model=list[MistakeOut])
def list_mistakes(
    subject: str | None = None,
    category_id: int | None = None,
    keyword: str | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    q = db.query(Mistake).filter(Mistake.is_archived == False)
    if subject:
        q = q.filter(Mistake.subject == subject)
    if category_id:
        q = q.filter(Mistake.category_id == category_id)
    if keyword:
        q = q.filter(Mistake.content.contains(keyword) | Mistake.title.contains(keyword))
    return q.order_by(Mistake.updated_at.desc()).offset(skip).limit(limit).all()


@router.get("/{mistake_id}", response_model=MistakeOut)
def get_mistake(mistake_id: int, db: Session = Depends(get_db)):
    m = db.query(Mistake).get(mistake_id)
    if not m:
        raise HTTPException(404, "错题不存在")
    return m


@router.post("", response_model=MistakeOut)
async def create_mistake(data: MistakeCreate, db: Session = Depends(get_db)):
    m = Mistake(**data.model_dump())
    if not m.ai_analysis:
        try:
            result = await analyze_mistake(m.content, m.subject)
            m.ai_analysis = result.get("raw", "")
        except Exception:
            m.ai_analysis = "AI 分析暂不可用"
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.patch("/{mistake_id}", response_model=MistakeOut)
def update_mistake(mistake_id: int, data: MistakeUpdate, db: Session = Depends(get_db)):
    m = db.query(Mistake).get(mistake_id)
    if not m:
        raise HTTPException(404, "错题不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(m, k, v)
    db.commit()
    db.refresh(m)
    return m


@router.delete("/{mistake_id}")
def delete_mistake(mistake_id: int, db: Session = Depends(get_db)):
    m = db.query(Mistake).get(mistake_id)
    if not m:
        raise HTTPException(404, "错题不存在")
    m.is_archived = True
    db.commit()
    return {"ok": True}


@router.get("/search", response_model=list[MistakeOut])
def search_mistakes(q: str = Query(...), db: Session = Depends(get_db)):
    return (
        db.query(Mistake)
        .filter(
            Mistake.is_archived == False,
            (Mistake.title.contains(q) | Mistake.content.contains(q) | Mistake.knowledge_point.contains(q)),
        )
        .limit(20)
        .all()
    )
