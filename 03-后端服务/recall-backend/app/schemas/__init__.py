"""Recall AI 智能错题本 - Pydantic Schema"""
from datetime import datetime
from pydantic import BaseModel, Field


# ===== Category =====
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)
    color: str = Field(default="#007AFF", max_length=20)
    icon: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    mistake_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


# ===== Mistake =====
class MistakeBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str
    source: str | None = None
    subject: str = Field(..., max_length=50)
    knowledge_point: str | None = None
    error_type: str | None = None
    category_id: int | None = None

class MistakeCreate(MistakeBase):
    image_url: str | None = None

class MistakeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    source: str | None = None
    subject: str | None = None
    knowledge_point: str | None = None
    error_type: str | None = None
    category_id: int | None = None
    ai_analysis: str | None = None

class MistakeOut(MistakeBase):
    id: int
    ai_analysis: str | None = None
    image_url: str | None = None
    review_count: int = 0
    mastery_level: float = 0.0
    next_review: datetime | None = None
    is_archived: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ===== Review =====
class ReviewSubmit(BaseModel):
    quality: int = Field(..., ge=0, le=5)

class ReviewOut(BaseModel):
    id: int
    mistake_id: int
    quality: int
    easiness: float
    interval: int
    repetition: int
    review_at: datetime

    model_config = {"from_attributes": True}


# ===== Chat =====
class ChatSessionCreate(BaseModel):
    title: str | None = "新对话"

class ChatSessionOut(BaseModel):
    id: int
    title: str
    is_pinned: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ChatMessageCreate(BaseModel):
    content: str

class ChatMessageOut(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ===== Dashboard =====
class DashboardStats(BaseModel):
    total: int = 0
    mastered: int = 0
    pending: int = 0
    avg_reviews: float = 0.0
    subject_distribution: dict[str, int] = {}
    weekly_trend: list[dict] = []
    weak_points: list[dict] = []
