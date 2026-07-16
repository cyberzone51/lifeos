"""AI models — разговоры, сообщения, память."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.session import Base


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="ai_conversations")
    messages: Mapped[list["AIMessage"]] = relationship(
        back_populates="conversation", order_by="AIMessage.created_at"
    )


class AIMessage(Base):
    __tablename__ = "ai_messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("ai_conversations.id")
    )
    role: Mapped[str] = mapped_column(String(20))  # user, assistant
    content: Mapped[str] = mapped_column(Text)
    agent_type: Mapped[str | None] = mapped_column(String(50))
    tokens_used: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    conversation: Mapped["AIConversation"] = relationship(
        back_populates="messages"
    )


class AIMemory(Base):
    __tablename__ = "ai_memory"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String(50))  # preferences, goals, dates, habits, style
    key: Mapped[str] = mapped_column(String(200))
    value: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Numeric(3, 2), default=1.0)
    source: Mapped[str | None] = mapped_column(String(50))  # user, inferred
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="ai_memories")
