"""Family API — эндпоинты для семейного режима."""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.family_service import FamilyService

router = APIRouter(prefix="/family", tags=["Family"])


class FamilyCreate(BaseModel):
    name: str


class FamilyJoin(BaseModel):
    invite_code: str


class SharedTaskCreate(BaseModel):
    title: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


class FamilyResponse(BaseModel):
    id: str
    name: str
    role: str
    invite_code: str


class SharedTaskResponse(BaseModel):
    id: str
    title: str
    assigned_to: Optional[str]
    is_completed: bool
    due_date: Optional[datetime]


@router.post("/", response_model=FamilyResponse)
async def create_family(request: FamilyCreate, db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = FamilyService(db)
    
    family = await service.create_family(user_id, request.name)
    
    return FamilyResponse(
        id=str(family.id),
        name=family.name,
        role="admin",
        invite_code=family.invite_code,
    )


@router.post("/join")
async def join_family(request: FamilyJoin, db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = FamilyService(db)
    
    family = await service.join_family(user_id, request.invite_code)
    
    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    
    return {"status": "joined", "family_id": str(family.id)}


@router.get("/", response_model=List[FamilyResponse])
async def list_families(db: AsyncSession = Depends(get_db)):
    user_id = uuid.uuid4()
    service = FamilyService(db)
    families = await service.get_user_families(user_id)
    return families


@router.post("/{family_id}/tasks", response_model=SharedTaskResponse)
async def create_shared_task(
    family_id: str,
    request: SharedTaskCreate,
    db: AsyncSession = Depends(get_db),
):
    user_id = uuid.uuid4()
    service = FamilyService(db)
    
    task = await service.create_shared_task(
        family_id=uuid.UUID(family_id),
        title=request.title,
        created_by=user_id,
        assigned_to=uuid.UUID(request.assigned_to) if request.assigned_to else None,
        due_date=request.due_date,
    )
    
    return SharedTaskResponse(
        id=str(task.id),
        title=task.title,
        assigned_to=str(task.assigned_to) if task.assigned_to else None,
        is_completed=task.is_completed,
        due_date=task.due_date,
    )


@router.get("/{family_id}/tasks")
async def list_shared_tasks(family_id: str, db: AsyncSession = Depends(get_db)):
    service = FamilyService(db)
    tasks = await service.get_family_tasks(uuid.UUID(family_id))
    return [
        {
            "id": str(t.id),
            "title": t.title,
            "assigned_to": str(t.assigned_to) if t.assigned_to else None,
            "is_completed": t.is_completed,
        }
        for t in tasks
    ]
