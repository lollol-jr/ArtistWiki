"""
Relationship Model
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Relationship(Base):
    """작가 간 관계 모델"""
    __tablename__ = "relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, index=True)
    target_artist_id = Column(UUID(as_uuid=True), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    source_artist = relationship("Artist", foreign_keys=[source_artist_id], back_populates="source_relationships")
    target_artist = relationship("Artist", foreign_keys=[target_artist_id], back_populates="target_relationships")

    __table_args__ = (
        UniqueConstraint('source_artist_id', 'target_artist_id', 'relationship_type', name='uq_relationship'),
    )
