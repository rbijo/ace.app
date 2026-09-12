import httpx
from typing import Optional
from app.services.ai.base import BaseAIService
from app.core.config import settings


class OpenRouterService(BaseAIService):

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        if not self.api_key:
            return f"[AI Tutor Mock Response]: You asked about '{prompt}'. Focus on breaking down the core concepts."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        full_prompt = f"Context: {context}\n\nUser Question: {prompt}" if context else prompt
        payload = {
            "model": "auto",
            "messages": [
                {"role": "system", "content": "You are ACE AI Academic Tutor, an encouraging and clear study companion."},
                {"role": "user", "content": full_prompt},
            ],
        }
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"[AI Response]: Unable to fetch remote AI completion (HTTP {response.status_code}). Summary: Focus on understanding '{prompt}'."
        except Exception as e:
            return f"[AI Response]: ACE AI Tutor guidance for '{prompt}': Study the core principles step-by-step."

    async def extract_topics(self, text: str) -> str:
        prompt = f"Extract a structured list of study topics from the following syllabus text:\n\n{text}"
        return await self.generate_response(prompt)

