from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAIService(ABC):

    @abstractmethod
    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response given prompt and context"""
        pass

    @abstractmethod
    async def extract_topics(self, text: str) -> str:
        """Extract structured topics from syllabus text"""
        pass

