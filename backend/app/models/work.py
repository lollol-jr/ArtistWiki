"""
Work Model
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Work(Base):
    """작품 모델"""
    __tablename__ = "works"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    year = Column(Integer, nullable=True, index=True)
    type = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # MediaWiki 연동
    mediawiki_page_id = Column(Integer, unique=True, nullable=True, index=True)
    mediawiki_page_title = Column(String(500), nullable=True)

    # 타임스탬프
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    artist = relationship("Artist", back_populates="works")
