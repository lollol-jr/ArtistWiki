"""
Artist Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class ArtistBase(BaseModel):
    """Artist 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=255)
    type: str = Field(..., pattern="^(painter|writer|musician)$")
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=100)
    biography: Optional[str] = None


class ArtistCreate(ArtistBase):
    """Artist 생성 스키마"""
    pass


class ArtistUpdate(BaseModel):
    """Artist 업데이트 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    type: Optional[str] = Field(None, pattern="^(painter|writer|musician)$")
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    nationality: Optional[str] = Field(None, max_length=100)
    biography: Optional[str] = None


class ArtistResponse(ArtistBase):
    """Artist 응답 스키마"""
    id: UUID
    mediawiki_page_id: Optional[int] = None
    mediawiki_page_title: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
