"""AI Repository — работа с разговорами, сообщениями и памятью."""

import uuid
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.ai import AIConversation, AIMessage, AIMemory


class AIRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Conversations
    async def create_conversation(
        self, user_id: uuid.UUID, title: str | None = None
    ) -> AIConversation:
        conversation = AIConversation(user_id=user_id, title=title)
        self.db.add(conversation)
        await self.db.flush()
        return conversation

    async def get_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> AIConversation | None:
        query = (
            select(AIConversation)
            .options(selectinload(AIConversation.messages))
            .where(
                and_(
                    AIConversation.id == conversation_id,
                    AIConversation.user_id == user_id,
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_conversations(
        self, user_id: uuid.UUID, limit: int = 20
    ) -> list[AIConversation]:
        query = (
            select(AIConversation)
            .where(AIConversation.user_id == user_id)
            .order_by(AIConversation.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    # Messages
    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        agent_type: str | None = None,
        tokens_used: int | None = None,
    ) -> AIMessage:
        message = AIMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            agent_type=agent_type,
            tokens_used=tokens_used,
        )
        self.db.add(message)
        await self.db.flush()
        return message

    async def get_conversation_history(
        self, conversation_id: uuid.UUID, limit: int = 50
    ) -> list[AIMessage]:
        query = (
            select(AIMessage)
            .where(AIMessage.conversation_id == conversation_id)
            .order_by(AIMessage.created_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        messages = list(result.scalars().all())
        messages.reverse()  # oldest first
        return messages

    # Memory
    async def add_memory(
        self,
        user_id: uuid.UUID,
        category: str,
        key: str,
        value: str,
        source: str = "inferred",
        confidence: float = 0.9,
    ) -> AIMemory:
        # Check if memory exists
        existing = await self.get_memory_by_key(user_id, category, key)
        
        if existing:
            existing.value = value
            existing.confidence = confidence
            existing.source = source
            await self.db.flush()
            return existing
        
        memory = AIMemory(
            user_id=user_id,
            category=category,
            key=key,
            value=value,
            source=source,
            confidence=confidence,
        )
        self.db.add(memory)
        await self.db.flush()
        return memory

    async def get_memory_by_key(
        self, user_id: uuid.UUID, category: str, key: str
    ) -> AIMemory | None:
        query = select(AIMemory).where(
            and_(
                AIMemory.user_id == user_id,
                AIMemory.category == category,
                AIMemory.key == key,
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_user_memories(
        self, user_id: uuid.UUID, category: str | None = None
    ) -> list[AIMemory]:
        query = select(AIMemory).where(AIMemory.user_id == user_id)
        
        if category:
            query = query.where(AIMemory.category == category)
            
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def delete_memory(self, memory_id: uuid.UUID, user_id: uuid.UUID) -> bool:
        query = delete(AIMemory).where(
            and_(AIMemory.id == memory_id, AIMemory.user_id == user_id)
        )
        result = await self.db.execute(query)
        return result.rowcount > 0
