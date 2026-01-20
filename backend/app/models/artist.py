"""
Artist Model
"""
from sqlalchemy import Column, String, Date, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Artist(Base):
    """작가/예술가 모델"""
    __tablename__ = "artists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # painter, writer, musician
    birth_date = Column(Date, nullable=True)
    death_date = Column(Date, nullable=True)
    nationality = Column(String(100), nullable=True)
    biography = Column(Text, nullable=True)

    # MediaWiki 연동
    mediawiki_page_id = Column(Integer, unique=True, nullable=True, index=True)
    mediawiki_page_title = Column(String(500), nullable=True)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    works = relationship("Work", back_populates="artist", cascade="all, delete-orphan")
    source_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.source_artist_id",
        back_populates="source_artist",
        cascade="all, delete-orphan"
    )
    target_relationships = relationship(
        "Relationship",
        foreign_keys="Relationship.target_artist_id",
        back_populates="target_artist",
        cascade="all, delete-orphan"
    )
