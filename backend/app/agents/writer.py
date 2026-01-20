"""
Writer Agent - AI로 위키 페이지 생성
"""
from typing import Dict, Any
from openai import AsyncOpenAI

from app.agents.base import BaseAgent
from app.core.config import settings


class WriterAgent(BaseAgent):
    """작성 에이전트"""

    def __init__(self):
        super().__init__("writer")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def execute(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        위키 페이지 생성

        Args:
            task_data: {
                "artist_name": "작가 이름",
                "artist_type": "painter|writer|musician",
                "source_data": "수집된 데이터"
            }

        Returns:
            생성된 위키 페이지
        """
        artist_name = task_data.get("artist_name")
        artist_type = task_data.get("artist_type", "artist")
        source_data = task_data.get("source_data", {})

        if not artist_name:
            raise ValueError("artist_name is required")

        self.logger.info(f"Generating wiki page for {artist_name}")

        # AI 프롬프트 생성
        prompt = self._create_prompt(artist_name, artist_type, source_data)

        # OpenAI API 호출
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates well-structured Wikipedia-style articles about artists."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )

        wiki_content = response.choices[0].message.content

        result = {
            "artist_name": artist_name,
            "wiki_content": wiki_content,
            "format": "wikitext",
            "model": "gpt-4"
        }

        self.logger.info(f"Successfully generated wiki page for {artist_name}")

        return result

    def _create_prompt(self, artist_name: str, artist_type: str, source_data: Dict[str, Any]) -> str:
        """AI 프롬프트 생성"""
        return f"""
Create a Wikipedia-style article about {artist_name}, a {artist_type}.

Source data:
{source_data}

Please create a well-structured article with the following sections:
1. Introduction (brief overview)
2. Early Life
3. Career
4. Notable Works
5. Legacy and Influence

Use proper Wikipedia formatting (wikitext syntax).
"""
