"""Family Service — семейный режим."""

import uuid
import random
import string
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.family import Family, FamilyMember, SharedTask, SharedBudget


class FamilyService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _generate_invite_code(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    async def create_family(
        self,
        user_id: uuid.UUID,
        name: str,
    ) -> Family:
        family = Family(
            name=name,
            invite_code=self._generate_invite_code(),
            created_by=user_id,
        )
        self.db.add(family)
        await self.db.flush()

        # Add creator as admin
        member = FamilyMember(
            family_id=family.id,
            user_id=user_id,
            role="admin",
        )
        self.db.add(member)
        await self.db.flush()

        return family

    async def join_family(
        self,
        user_id: uuid.UUID,
        invite_code: str,
    ) -> Family | None:
        query = select(Family).where(Family.invite_code == invite_code)
        result = await self.db.execute(query)
        family = result.scalar_one_or_none()
        
        if not family:
            return None

        # Check if already member
        existing = await self.db.execute(
            select(FamilyMember).where(
                and_(
                    FamilyMember.family_id == family.id,
                    FamilyMember.user_id == user_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            return family

        member = FamilyMember(
            family_id=family.id,
            user_id=user_id,
            role="member",
        )
        self.db.add(member)
        await self.db.flush()

        return family

    async def get_user_families(self, user_id: uuid.UUID) -> list[dict]:
        query = (
            select(Family, FamilyMember)
            .join(FamilyMember, Family.id == FamilyMember.family_id)
            .where(FamilyMember.user_id == user_id)
        )
        result = await self.db.execute(query)
        return [
            {
                "id": str(f.id),
                "name": f.name,
                "role": m.role,
                "invite_code": f.invite_code,
            }
            for f, m in result.all()
        ]

    async def create_shared_task(
        self,
        family_id: uuid.UUID,
        title: str,
        created_by: uuid.UUID,
        assigned_to: uuid.UUID | None = None,
        due_date: datetime | None = None,
    ) -> SharedTask:
        task = SharedTask(
            family_id=family_id,
            title=title,
            created_by=created_by,
            assigned_to=assigned_to,
            due_date=due_date,
        )
        self.db.add(task)
        await self.db.flush()
        return task

    async def get_family_tasks(self, family_id: uuid.UUID) -> list[SharedTask]:
        query = (
            select(SharedTask)
            .where(SharedTask.family_id == family_id)
            .order_by(SharedTask.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
