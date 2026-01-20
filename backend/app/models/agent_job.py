"""
Agent Job Model
"""
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from app.core.database import Base


class AgentJob(Base):
    """에이전트 작업 모델"""
    __tablename__ = "agent_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False, index=True)  # pending, running, success, failed
    target_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    target_type = Column(String(50), nullable=True)
    input_data = Column(JSONB, nullable=True)
    output_data = Column(JSONB, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
