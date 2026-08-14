"""AI 答疑路由"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ChatSession, ChatMessage
from app.schemas import ChatSessionCreate, ChatSessionOut, ChatMessageCreate, ChatMessageOut
from app.services.ai_service import chat_completion

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/sessions", response_model=list[ChatSessionOut])
def list_sessions(db: Session = Depends(get_db)):
    return db.query(ChatSession).order_by(ChatSession.updated_at.desc()).all()


@router.post("/sessions", response_model=ChatSessionOut)
def create_session(data: ChatSessionCreate, db: Session = Depends(get_db)):
    s = ChatSession(title=data.title or "新对话")
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    s = db.query(ChatSession).get(session_id)
    if not s:
        raise HTTPException(404, "对话不存在")
    db.query(ChatMessage).filter(ChatMessage.session_id == session_id).delete()
    db.delete(s)
    db.commit()
    return {"ok": True}


@router.get("/sessions/{session_id}/messages", response_model=list[ChatMessageOut])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .all()
    )


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageOut)
async def send_message(session_id: int, data: ChatMessageCreate, db: Session = Depends(get_db)):
    session = db.query(ChatSession).get(session_id)
    if not session:
        raise HTTPException(404, "对话不存在")

    # 保存用户消息
    user_msg = ChatMessage(session_id=session_id, role="user", content=data.content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 获取历史消息构建上下文
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .limit(20)
        .all()
    )
    messages = [
        {"role": "system", "content": "你是 Recall AI 助手，专门帮助学生解答错题、分析知识点。回答要清晰、有逻辑，适合学生理解。"},
    ]
    for msg in history:
        messages.append({"role": msg.role, "content": msg.content})

    # 调用 AI
    ai_reply = await chat_completion(messages)

    # 保存 AI 回复
    ai_msg = ChatMessage(session_id=session_id, role="assistant", content=ai_reply)
    db.add(ai_msg)
    session.title = data.content[:30] if len(history) <= 1 else session.title
    db.commit()
    db.refresh(ai_msg)

    return ai_msg


class ChatProxyRequest(BaseModel):
    """无状态对话代理请求：前端直接传 messages"""
    messages: list[dict]
    temperature: float = 0.7


@router.post("/message")
async def chat_message(data: ChatProxyRequest):
    """AI 答疑代理：前端传 messages，后端转发硅基流动，返回 reply"""
    reply = await chat_completion(data.messages, data.temperature)
    return {"reply": reply}
