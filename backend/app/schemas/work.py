"""
Work Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class WorkBase(BaseModel):
    """Work 기본 스키마"""
    title: str = Field(..., min_length=1, max_length=500)
    year: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class WorkCreate(WorkBase):
    """Work 생성 스키마"""
    artist_id: UUID


class WorkUpdate(BaseModel):
    """Work 업데이트 스키마"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    year: Optional[int] = None
    type: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class WorkResponse(WorkBase):
    """Work 응답 스키마"""
    id: UUID
    artist_id: UUID
    mediawiki_page_id: Optional[int] = None
    mediawiki_page_title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
