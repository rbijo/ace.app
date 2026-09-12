from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.ai_session import AISession
from app.schemas.ai import AIQueryRequest, AIQueryResponse
from app.services.ai.openrouter import OpenRouterService
from app.services.ai.gemini import GeminiService
from app.services.ai.openai import OpenAIService

router = APIRouter(prefix="/ai", tags=["AI Tutor Service"])


@router.post("/query", response_model=AIQueryResponse)
async def query_ai_tutor(
    query_in: AIQueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    provider_name = (query_in.provider or "openrouter").lower()

    if provider_name == "gemini":
        service = GeminiService()
    elif provider_name == "openai":
        service = OpenAIService()
    else:
        service = OpenRouterService()

    response_text = await service.generate_response(prompt=query_in.prompt)

    # Record AI Session
    ai_session = AISession(
        user_id=current_user.id,
        topic_id=query_in.topic_id,
        prompt=query_in.prompt,
        response=response_text,
        provider=provider_name
    )
    db.add(ai_session)
    await db.commit()

    return AIQueryResponse(
        response=response_text,
        provider=provider_name,
        topic_id=query_in.topic_id
    )

