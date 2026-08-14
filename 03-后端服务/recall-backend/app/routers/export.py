"""导出路由"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Mistake
from app.services.export_service import export_to_pdf, export_to_markdown

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/pdf")
def export_pdf(subject: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Mistake).filter(Mistake.is_archived == False)
    if subject:
        q = q.filter(Mistake.subject == subject)
    mistakes = q.all()
    data = [
        {
            "title": m.title,
            "content": m.content,
            "subject": m.subject,
            "knowledge_point": m.knowledge_point,
            "ai_analysis": m.ai_analysis,
            "review_count": m.review_count,
        }
        for m in mistakes
    ]
    pdf_bytes = export_to_pdf(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=recall-mistakes.pdf"},
    )


@router.get("/markdown")
def export_markdown(subject: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Mistake).filter(Mistake.is_archived == False)
    if subject:
        q = q.filter(Mistake.subject == subject)
    mistakes = q.all()
    data = [
        {
            "title": m.title,
            "content": m.content,
            "subject": m.subject,
            "knowledge_point": m.knowledge_point,
            "ai_analysis": m.ai_analysis,
            "review_count": m.review_count,
        }
        for m in mistakes
    ]
    md_text = export_to_markdown(data)
    return Response(
        content=md_text,
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=recall-mistakes.md"},
    )
