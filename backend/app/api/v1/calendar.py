"""Calendar API — эндпоинты для календаря."""

import uuid
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.calendar_service import CalendarService

router = APIRouter(prefix="/calendar", tags=["Calendar"])


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    all_day: bool = False
    color: Optional[str] = None


class EventResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    location: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    all_day: bool
    color: Optional[str]


@router.post("/events", response_model=EventResponse)
async def create_event(request: EventCreate, db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = CalendarService(db)
    
    event = await service.create_event(
        user_id=user_id,
        title=request.title,
        start_time=request.start_time,
        end_time=request.end_time,
        description=request.description,
        location=request.location,
        all_day=request.all_day,
        color=request.color,
    )
    
    return EventResponse(
        id=str(event.id),
        title=event.title,
        description=event.description,
        location=event.location,
        start_time=event.start_time,
        end_time=event.end_time,
        all_day=event.all_day,
        color=event.color,
    )


@router.get("/events", response_model=List[EventResponse])
async def list_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    user_id = uuid.uuid4()
    service = CalendarService(db)
    events = await service.get_events(user_id, start_date, end_date)
    
    return [
        EventResponse(
            id=str(e.id),
            title=e.title,
            description=e.description,
            location=e.location,
            start_time=e.start_time,
            end_time=e.end_time,
            all_day=e.all_day,
            color=e.color,
        )
        for e in events
    ]


@router.get("/today")
async def get_today(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = CalendarService(db)
    events = await service.get_today_events(user_id)
    return {"events": [{"id": str(e.id), "title": e.title, "start_time": e.start_time} for e in events]}


@router.get("/week")
async def get_week(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = CalendarService(db)
    events = await service.get_week_events(user_id)
    return {"events": [{"id": str(e.id), "title": e.title, "start_time": e.start_time} for e in events]}
