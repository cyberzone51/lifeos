"""User Repository — работа с пользователями."""

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.db.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_or_create_by_telegram(
        self, telegram_id: int, **kwargs
    ) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if not user:
            user = await self.create(telegram_id=telegram_id, **kwargs)
        return user

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        await self.db.flush()
        return user
