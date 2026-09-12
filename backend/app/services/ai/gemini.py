import httpx
from typing import Optional
from app.services.ai.base import BaseAIService
from app.core.config import settings


class GeminiService(BaseAIService):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        if not self.api_key:
            return f"[Gemini AI Fallback]: Answer for '{prompt}' based on academic curriculum."
        return f"[Gemini AI]: Detailed study guidance for '{prompt}'."

    async def extract_topics(self, text: str) -> str:
        return await self.generate_response(f"Extract topics: {text}")

