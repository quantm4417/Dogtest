from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.care import CareTask, CareTaskLog, IntervalType
from app.schemas.care import (
    CareTaskCreate, CareTaskUpdate, CareTaskResponse,
    CareTaskLogResponse
)
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/tasks", response_model=List[CareTaskResponse])
async def read_care_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: int = None
):
    query = select(CareTask).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(CareTask.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/tasks", response_model=CareTaskResponse)
async def create_care_task(
    task_in: CareTaskCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Verify dog
    dog_result = await db.execute(select(Dog).where(Dog.id == task_in.dog_id, Dog.owner_user_id == current_user.id))
    if not dog_result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found")
        
    task = CareTask(**task_in.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

@router.put("/tasks/{task_id}", response_model=CareTaskResponse)
async def update_care_task(
    task_id: int,
    task_in: CareTaskUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(CareTask).join(Dog).where(CareTask.id == task_id, Dog.owner_user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Care task not found")
        
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    await db.commit()
    await db.refresh(task)
    return task

@router.delete("/tasks/{task_id}")
async def delete_care_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(CareTask).join(Dog).where(CareTask.id == task_id, Dog.owner_user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Care task not found")
        
    await db.delete(task)
    await db.commit()
    return {"ok": True}

@router.post("/tasks/{task_id}/complete", response_model=CareTaskResponse)
async def complete_care_task(
    task_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    notes: str = None
):
    result = await db.execute(select(CareTask).join(Dog).where(CareTask.id == task_id, Dog.owner_user_id == current_user.id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Care task not found")
    
    # Create log
    log = CareTaskLog(
        care_task_id=task.id,
        done_at=datetime.utcnow(),
        notes=notes
    )
    db.add(log)
    
    # Calculate next due date
    today = datetime.utcnow().date()
    if task.interval_type == IntervalType.DAILY:
        task.next_due_date = today + timedelta(days=1)
    elif task.interval_type == IntervalType.WEEKLY:
        task.next_due_date = today + timedelta(weeks=1)
    elif task.interval_type == IntervalType.MONTHLY:
        # Simple monthly addition (30 days approx or same day next month)
        # Let's do 30 days for simplicity or simple month logic
        import calendar
        month = today.month
        year = today.year
        next_month = month + 1
        if next_month > 12:
            next_month = 1
            year += 1
        
        # Try to keep same day, clamp to max days in month
        day = min(today.day, calendar.monthrange(year, next_month)[1])
        task.next_due_date = today.replace(year=year, month=next_month, day=day)
        
    elif task.interval_type == IntervalType.CUSTOM_DAYS:
        days = task.interval_days or 1
        task.next_due_date = today + timedelta(days=days)
    
    await db.commit()
    await db.refresh(task)
    return task

@router.get("/logs", response_model=List[CareTaskLogResponse])
async def read_care_logs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: int = None,
    task_id: int = None
):
    query = select(CareTaskLog).join(CareTask).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(CareTask.dog_id == dog_id)
    if task_id:
        query = query.where(CareTaskLog.care_task_id == task_id)
        
    result = await db.execute(query)
    return result.scalars().all()

