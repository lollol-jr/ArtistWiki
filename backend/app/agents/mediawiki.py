"""
MediaWiki Agent - MediaWiki API 연동
"""
from typing import Dict, Any, Optional
import httpx

from app.agents.base import BaseAgent
from app.core.config import settings


class MediaWikiAgent(BaseAgent):
    """미디어위키 연동 에이전트"""

    def __init__(self):
        super().__init__("mediawiki")
        self.api_url = settings.MEDIAWIKI_API_URL
        self.username = settings.MEDIAWIKI_BOT_USERNAME
        self.password = settings.MEDIAWIKI_BOT_PASSWORD
        self.token: Optional[str] = None

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        MediaWiki 작업 실행

        Args:
            task_data: {
                "action": "create|edit|delete",
                "page_title": "페이지 제목",
                "content": "페이지 내용"
            }

        Returns:
            작업 결과
        """
        action = task_data.get("action")
        page_title = task_data.get("page_title")
        content = task_data.get("content")

        if not page_title:
            raise ValueError("page_title is required")

        self.logger.info(f"Executing MediaWiki action: {action} for page: {page_title}")

        # 토큰 획득 (필요 시)
        if not self.token:
            await self._login()

        if action == "create" or action == "edit":
            result = await self._edit_page(page_title, content)
        elif action == "delete":
            result = await self._delete_page(page_title)
        else:
            raise ValueError(f"Unknown action: {action}")

        self.logger.info(f"MediaWiki action completed: {action} for page: {page_title}")

        return result

    async def _login(self) -> None:
        """MediaWiki 로그인 및 토큰 획득"""
        async with httpx.AsyncClient() as client:
            # 로그인 토큰 획득
            response = await client.get(
                self.api_url,
                params={
                    "action": "query",
                    "meta": "tokens",
                    "type": "login",
                    "format": "json"
                }
            )
            data = response.json()
            login_token = data["query"]["tokens"]["logintoken"]

            # 로그인
            response = await client.post(
                self.api_url,
                data={
                    "action": "login",
                    "lgname": self.username,
                    "lgpassword": self.password,
                    "lgtoken": login_token,
                    "format": "json"
                }
            )

            # CSRF 토큰 획득
            response = await client.get(
                self.api_url,
                params={
                    "action": "query",
                    "meta": "tokens",
                    "format": "json"
                }
            )
            data = response.json()
            self.token = data["query"]["tokens"]["csrftoken"]

        self.logger.info("Successfully logged in to MediaWiki")

    async def _edit_page(self, page_title: str, content: str) -> Dict[str, Any]:
        """페이지 생성/편집"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                data={
                    "action": "edit",
                    "title": page_title,
                    "text": content,
                    "token": self.token,
                    "format": "json",
                    "bot": "1"
                }
            )
            result = response.json()

            if "error" in result:
                raise Exception(f"MediaWiki API error: {result['error']}")

            return {
                "page_title": page_title,
                "page_id": result.get("edit", {}).get("pageid"),
                "status": "success"
            }

    async def _delete_page(self, page_title: str) -> Dict[str, Any]:
        """페이지 삭제"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                data={
                    "action": "delete",
                    "title": page_title,
                    "token": self.token,
                    "format": "json"
                }
            )
            result = response.json()

            if "error" in result:
                raise Exception(f"MediaWiki API error: {result['error']}")

            return {
                "page_title": page_title,
                "status": "deleted"
            }

    async def get_page(self, page_title: str) -> Dict[str, Any]:
        """페이지 조회"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.api_url,
                params={
                    "action": "parse",
                    "page": page_title,
                    "format": "json"
                }
            )
            result = response.json()

            if "error" in result:
                return {"error": result["error"], "exists": False}

            return {
                "page_title": page_title,
                "page_id": result.get("parse", {}).get("pageid"),
                "content": result.get("parse", {}).get("wikitext", {}).get("*"),
                "exists": True
            }
