"""Knowledge model — база знаний."""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, DateTime, ForeignKey, ARRAY, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class KnowledgeItem(Base):
    __tablename__ = "knowledge_items"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    item_type: Mapped[str] = mapped_column(String(20))  # pdf, image, link, video, text, voice
    title: Mapped[str | None] = mapped_column(String(500))
    content: Mapped[str | None] = mapped_column(Text)
    file_url: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    summary: Mapped[str | None] = mapped_column(Text)
    extra_data: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
