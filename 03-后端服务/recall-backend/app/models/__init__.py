"""Recall AI 智能错题本 - 数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    color = Column(String(20), nullable=False, default="#007AFF")
    icon = Column(String(50), nullable=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    mistakes = relationship("Mistake", back_populates="category", lazy="selectin")


class Mistake(Base):
    __tablename__ = "mistakes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100), nullable=True)
    subject = Column(String(50), nullable=False)
    knowledge_point = Column(String(100), nullable=True)
    error_type = Column(String(50), nullable=True)
    ai_analysis = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    review_count = Column(Integer, default=0)
    mastery_level = Column(Float, default=0.0)
    next_review = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="mistakes")
    reviews = relationship("ReviewRecord", back_populates="mistake", lazy="selectin")


class ReviewRecord(Base):
    __tablename__ = "review_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mistake_id = Column(Integer, ForeignKey("mistakes.id"), nullable=False)
    quality = Column(Integer, nullable=False)  # SM-2 quality: 0-5
    easiness = Column(Float, default=2.5)
    interval = Column(Integer, default=1)
    repetition = Column(Integer, default=0)
    review_at = Column(DateTime, default=datetime.utcnow)

    mistake = relationship("Mistake", back_populates="reviews")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, default="新对话")
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session", lazy="selectin")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(20), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
