from typing import Optional
from app.services.ai.base import BaseAIService
from app.core.config import settings


class OpenAIService(BaseAIService):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        if not self.api_key:
            return f"[OpenAI Fallback]: Guidance for topic '{prompt}'."
        return f"[OpenAI Response]: Explanation for '{prompt}'."

    async def extract_topics(self, text: str) -> str:
        return await self.generate_response(f"Extract topics from syllabus:\n{text}")

