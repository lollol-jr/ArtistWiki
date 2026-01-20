"""
Agent Orchestrator
"""
from typing import Dict, Any, List, Optional
from uuid import UUID
import asyncio
import logging
from datetime import datetime

from app.agents.base import BaseAgent
from app.models.agent_job import AgentJob
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """에이전트 오케스트레이터 - 모든 에이전트를 조율"""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.logger = logging.getLogger("orchestrator")

    def register_agent(self, agent_type: str, agent: BaseAgent) -> None:
        """에이전트 등록"""
        self.agents[agent_type] = agent
        self.logger.info(f"Registered agent: {agent_type}")

    async def execute_workflow(
        self,
        workflow: List[Dict[str, Any]],
        db: AsyncSession,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        워크플로우 실행

        Args:
            workflow: 워크플로우 정의 (에이전트 순서 및 설정)
            db: 데이터베이스 세션
            context: 공유 컨텍스트

        Returns:
            실행 결과
        """
        if context is None:
            context = {}

        results = []

        for step in workflow:
            agent_type = step.get("agent_type")
            task_data = step.get("task_data", {})

            # 컨텍스트 병합
            task_data.update(context)

            result = await self.execute_task(
                agent_type=agent_type,
                task_data=task_data,
                db=db
            )

            results.append(result)

            # 다음 단계를 위해 컨텍스트 업데이트
            if result.get("status") == "success":
                context.update(result.get("output", {}))
            else:
                # 실패 시 중단
                break

        return {
            "status": "completed",
            "results": results,
            "context": context
        }

    async def execute_task(
        self,
        agent_type: str,
        task_data: Dict[str, Any],
        db: AsyncSession
    ) -> Dict[str, Any]:
        """
        단일 에이전트 작업 실행

        Args:
            agent_type: 에이전트 타입
            task_data: 작업 데이터
            db: 데이터베이스 세션

        Returns:
            실행 결과
        """
        agent = self.agents.get(agent_type)

        if not agent:
            return {
                "status": "error",
                "error": f"Unknown agent type: {agent_type}"
            }

        # AgentJob 생성
        job = AgentJob(
            job_type=agent_type,
            status="running",
            input_data=task_data,
            started_at=datetime.utcnow()
        )
        db.add(job)
        await db.commit()

        try:
            # 에이전트 실행
            result = await agent.execute(task_data)

            # Job 업데이트
            job.status = "success"
            job.output_data = result
            job.completed_at = datetime.utcnow()

            await agent.on_success(result)

            return {
                "status": "success",
                "job_id": str(job.id),
                "output": result
            }

        except Exception as e:
            # Job 업데이트
            job.status = "failed"
            job.error_message = str(e)
            job.completed_at = datetime.utcnow()

            await agent.on_failure(e)

            return {
                "status": "error",
                "job_id": str(job.id),
                "error": str(e)
            }
        finally:
            await db.commit()


# 글로벌 오케스트레이터 인스턴스
orchestrator = AgentOrchestrator()
