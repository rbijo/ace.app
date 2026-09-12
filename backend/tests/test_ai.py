import pytest
from app.services.ai.openrouter import OpenRouterService


@pytest.mark.asyncio
async def test_ai_openrouter_service_fallback():
    service = OpenRouterService(api_key="")
    res = await service.generate_response("What is dynamic programming?")
    assert "dynamic programming" in res.lower() or "ai tutor" in res.lower()

