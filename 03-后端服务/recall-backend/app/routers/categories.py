"""分类 CRUD 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Category, Mistake
from app.schemas import CategoryCreate, CategoryUpdate, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    cats = db.query(Category).order_by(Category.sort_order).all()
    result = []
    for c in cats:
        out = CategoryOut.model_validate(c)
        out.mistake_count = db.query(Mistake).filter(
            Mistake.category_id == c.id, Mistake.is_archived == False
        ).count()
        result.append(out)
    return result


@router.post("", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    c = Category(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.patch("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    c = db.query(Category).get(category_id)
    if not c:
        raise HTTPException(404, "分类不存在")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    c = db.query(Category).get(category_id)
    if not c:
        raise HTTPException(404, "分类不存在")
    mistake_count = db.query(Mistake).filter(Mistake.category_id == category_id).count()
    if mistake_count > 0:
        raise HTTPException(400, f"该分类下还有 {mistake_count} 道错题，请先移动或删除")
    db.delete(c)
    db.commit()
    return {"ok": True}
