"""AI API — эндпоинты для AI ассистента с интеграцией БД."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.ai_service import AIService
from app.repositories.ai_repo import AIRepository

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    intent: dict
    action_taken: Optional[dict] = None


class MemoryResponse(BaseModel):
    id: str
    category: str
    key: str
    value: str
    confidence: float
    source: Optional[str]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    """Отправить сообщение AI ассистенту."""
    # TODO: Получение user_id из JWT
    # Пока используем заглушку
    user_id = uuid.uuid4()  # Заглушка для тестирования

    ai_service = AIService(db)
    
    conv_id = None
    if request.conversation_id:
        try:
            conv_id = uuid.UUID(request.conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation_id")

    result = await ai_service.process_message(
        user_id=user_id,
        message=request.message,
        conversation_id=conv_id,
    )

    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        intent=result["intent"],
        action_taken=result.get("action_taken"),
    )


@router.get("/conversations")
async def list_conversations(db: AsyncSession = Depends(get_db)):
    """Получить список разговоров."""
    user_id = uuid.uuid4()  # Заглушка
    ai_repo = AIRepository(db)
    conversations = await ai_repo.get_user_conversations(user_id)
    
    return [
        {
            "id": str(c.id),
            "title": c.title,
            "created_at": c.created_at.isoformat(),
        }
        for c in conversations
    ]


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Получить сообщения разговора."""
    user_id = uuid.uuid4()  # Заглушка
    ai_repo = AIRepository(db)
    
    try:
        conv_id = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid conversation_id")

    conversation = await ai_repo.get_conversation(conv_id, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = await ai_repo.get_conversation_history(conv_id)
    
    return [
        {
            "id": str(m.id),
            "role": m.role,
            "content": m.content,
            "agent_type": m.agent_type,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]


@router.get("/memory", response_model=list[MemoryResponse])
async def get_memory(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Получить AI память пользователя."""
    user_id = uuid.uuid4()  # Заглушка
    ai_repo = AIRepository(db)
    memories = await ai_repo.get_user_memories(user_id, category)
    
    return [
        MemoryResponse(
            id=str(m.id),
            category=m.category,
            key=m.key,
            value=m.value,
            confidence=float(m.confidence),
            source=m.source,
        )
        for m in memories
    ]


@router.delete("/memory/{memory_id}")
async def delete_memory(memory_id: str, db: AsyncSession = Depends(get_db)):
    """Удалить запись из AI памяти."""
    user_id = uuid.uuid4()  # Заглушка
    ai_repo = AIRepository(db)
    
    try:
        mem_id = uuid.UUID(memory_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid memory_id")

    deleted = await ai_repo.delete_memory(mem_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found")

    return {"status": "deleted"}


@router.post("/voice")
async def voice_chat():
    """Голосовой ввод (заглушка)."""
    # TODO: Whisper интеграция
    return {"status": "not_implemented"}
