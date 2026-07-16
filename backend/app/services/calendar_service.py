"""Calendar Service — управление календарем и событиями."""

import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.models.calendar import CalendarEvent


class CalendarService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_event(
        self,
        user_id: uuid.UUID,
        title: str,
        start_time: datetime,
        end_time: datetime | None = None,
        description: str | None = None,
        location: str | None = None,
        all_day: bool = False,
        color: str | None = None,
    ) -> CalendarEvent:
        event = CalendarEvent(
            user_id=user_id,
            title=title,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location,
            all_day=all_day,
            color=color,
        )
        self.db.add(event)
        await self.db.flush()
        return event

    async def get_events(
        self,
        user_id: uuid.UUID,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> list[CalendarEvent]:
        query = select(CalendarEvent).where(CalendarEvent.user_id == user_id)
        
        if start_date:
            query = query.where(CalendarEvent.start_time >= start_date)
        if end_date:
            query = query.where(CalendarEvent.start_time <= end_date)
            
        query = query.order_by(CalendarEvent.start_time)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_today_events(self, user_id: uuid.UUID) -> list[CalendarEvent]:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        return await self.get_events(user_id, today, tomorrow)

    async def get_week_events(self, user_id: uuid.UUID) -> list[CalendarEvent]:
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = today + timedelta(days=7)
        return await self.get_events(user_id, today, week_end)

    async def delete_event(self, event_id: uuid.UUID) -> bool:
        query = select(CalendarEvent).where(CalendarEvent.id == event_id)
        result = await self.db.execute(query)
        event = result.scalar_one_or_none()
        
        if event:
            await self.db.delete(event)
            await self.db.flush()
            return True
        return False
