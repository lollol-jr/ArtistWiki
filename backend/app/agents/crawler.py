"""
Crawler Agent - 외부 소스에서 작가 정보 수집
"""
from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup

from app.agents.base import BaseAgent


class CrawlerAgent(BaseAgent):
    """크롤링 에이전트"""

    def __init__(self):
        super().__init__("crawler")

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        크롤링 작업 실행

        Args:
            task_data: {
                "url": "크롤링할 URL",
                "artist_name": "작가 이름"
            }

        Returns:
            크롤링 결과
        """
        url = task_data.get("url")
        artist_name = task_data.get("artist_name")

        if not url:
            raise ValueError("URL is required")

        self.logger.info(f"Crawling data for {artist_name} from {url}")

        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 기본 정보 추출 (예시 - 실제 구현은 소스에 따라 다름)
        extracted_data = {
            "name": artist_name,
            "source_url": url,
            "raw_html": response.text[:1000],  # 처음 1000자만
            "title": soup.title.string if soup.title else None,
        }

        self.logger.info(f"Successfully crawled data for {artist_name}")

        return extracted_data
