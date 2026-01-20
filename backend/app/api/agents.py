"""
Agents API Router
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.core.database import get_db
from app.models.agent_job import AgentJob
from app.agents.orchestrator import orchestrator
from app.agents.crawler import CrawlerAgent
from app.agents.writer import WriterAgent
from app.agents.mediawiki import MediaWikiAgent
from pydantic import BaseModel

router = APIRouter()

# 에이전트 등록
orchestrator.register_agent("crawler", CrawlerAgent())
orchestrator.register_agent("writer", WriterAgent())
orchestrator.register_agent("mediawiki", MediaWikiAgent())


class WorkflowStep(BaseModel):
    agent_type: str
    task_data: Dict[str, Any]


class WorkflowRequest(BaseModel):
    workflow: List[WorkflowStep]
    context: Optional[Dict[str, Any]] = None


@router.post("/jobs")
async def execute_workflow(
    request: WorkflowRequest,
    db: AsyncSession = Depends(get_db)
):
    """워크플로우 실행"""
    workflow = [step.model_dump() for step in request.workflow]
    result = await orchestrator.execute_workflow(
        workflow=workflow,
        db=db,
        context=request.context or {}
    )
    return result


@router.get("/jobs")
async def get_agent_jobs(
    status: Optional[str] = Query(None, pattern="^(pending|running|success|failed)$"),
    job_type: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """에이전트 작업 목록 조회"""
    query = select(AgentJob)

    # 필터링
    if status:
        query = query.filter(AgentJob.status == status)
    if job_type:
        query = query.filter(AgentJob.job_type == job_type)

    # 총 개수
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    # 최신순 정렬 및 페이지네이션
    query = query.order_by(AgentJob.created_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = result.scalars().all()

    return {
        "items": jobs,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@router.get("/jobs/{job_id}")
async def get_agent_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """에이전트 작업 상세 조회"""
    result = await db.execute(
        select(AgentJob).filter(AgentJob.id == job_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Agent job not found")

    return job
