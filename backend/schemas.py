"""
Pydantic схемы для валидации данных
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# Схемы для пользователей
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    telegram_id: Optional[str] = None


class User(UserBase):
    id: int
    telegram_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Схемы для аутентификации
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Схемы для анализа
class AnalysisRequest(BaseModel):
    text: str
    analysis_type: str  # sentiment, summary, keywords


class AnalysisResponse(BaseModel):
    id: int
    original_text: str
    analysis_type: str
    result: str
    confidence_score: Optional[str] = None
    processing_time: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnalysisList(BaseModel):
    analyses: List[AnalysisResponse]
    total: int


# Схемы для Telegram
class TelegramUser(BaseModel):
    telegram_id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


# Общие схемы ответов
class MessageResponse(BaseModel):
    message: str
    status: str = "success"


class ErrorResponse(BaseModel):
    detail: str
    status: str = "error"
