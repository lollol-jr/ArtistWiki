"""
Base Agent Class
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """모든 에이전트의 베이스 클래스"""

    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        에이전트 실행 메서드

        Args:
            task_data: 작업 데이터

        Returns:
            실행 결과 딕셔너리
        """
        pass

    async def on_success(self, result: Dict[str, Any]) -> None:
        """성공 시 호출되는 훅"""
        self.logger.info(f"Agent {self.name} completed successfully")

    async def on_failure(self, error: Exception) -> None:
        """실패 시 호출되는 훅"""
        self.logger.error(f"Agent {self.name} failed: {str(error)}")

    async def validate_input(self, task_data: Dict[str, Any]) -> bool:
        """입력 데이터 검증"""
        return True
