from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.walks import Walk, WalkDog
from app.models.training import TrainingLog, TrainingGoal
from app.models.health import VetVisit
from app.models.care import CareTaskLog, CareTask
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class ActivityItem(BaseModel):
    type: str
    id: int
    datetime: datetime
    title: str
    description: Optional[str] = None
    dog_names: List[str] = []

@router.get("/", response_model=List[ActivityItem])
async def read_activity(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    limit: int = 50
):
    # Fetch Walks
    walks_query = select(Walk).where(Walk.user_id == current_user.id).order_by(desc(Walk.start_datetime)).limit(limit)
    walks_res = await db.execute(walks_query)
    walks = walks_res.scalars().all()
    
    # Fetch Training Logs
    # Join Dog to ensure user ownership
    tlogs_query = select(TrainingLog).join(Dog).where(Dog.owner_user_id == current_user.id).order_by(desc(TrainingLog.datetime)).limit(limit)
    tlogs_res = await db.execute(tlogs_query)
    tlogs = tlogs_res.scalars().all()
    
    # Fetch Vet Visits
    visits_query = select(VetVisit).join(Dog).where(Dog.owner_user_id == current_user.id).order_by(desc(VetVisit.date)).limit(limit)
    visits_res = await db.execute(visits_query)
    visits = visits_res.scalars().all()
    
    # Fetch Care Logs
    clogs_query = select(CareTaskLog).join(CareTask).join(Dog).where(Dog.owner_user_id == current_user.id).order_by(desc(CareTaskLog.done_at)).limit(limit)
    clogs_res = await db.execute(clogs_query)
    clogs = clogs_res.scalars().all()
    
    activities = []
    
    # Process Walks
    for w in walks:
        # Need to fetch associated dogs names efficiently. 
        # For now, lazy loading might trigger N+1 but we are async.
        # We should have eager loaded. Let's assume basic info for now.
        # We'll do a separate small query or assume loaded if lazy='subquery' was set (it wasn't).
        
        # Fetch dog names manually for now to avoid session issues
        wd_res = await db.execute(select(Dog.name).join(WalkDog).where(WalkDog.walk_id == w.id))
        dog_names = wd_res.scalars().all()
        
        activities.append(ActivityItem(
            type="WALK",
            id=w.id,
            datetime=w.start_datetime,
            title=f"Walk ({w.duration_minutes} min)",
            description=w.mood.value if w.mood else None,
            dog_names=list(dog_names)
        ))

    # Process Training Logs
    for t in tlogs:
        # Get dog name
        d_res = await db.execute(select(Dog.name).where(Dog.id == t.dog_id))
        d_name = d_res.scalar_one()
        
        title = "Training Session"
        # If linked to goal
        if t.training_goal_id:
             # fetch goal title
             g_res = await db.execute(select(TrainingGoal.title).where(TrainingGoal.id == t.training_goal_id))
             g_title = g_res.scalar_one_or_none()
             if g_title: title = f"Training: {g_title}"
             
        activities.append(ActivityItem(
            type="TRAINING",
            id=t.id,
            datetime=t.datetime,
            title=title,
            description=f"Rating: {t.rating}/5" if t.rating else None,
            dog_names=[d_name]
        ))
        
    # Process Vet Visits
    for v in visits:
        d_res = await db.execute(select(Dog.name).where(Dog.id == v.dog_id))
        d_name = d_res.scalar_one()
        
        # Convert date to datetime for sorting
        dt = datetime.combine(v.date, datetime.min.time())
        
        activities.append(ActivityItem(
            type="VET",
            id=v.id,
            datetime=dt,
            title=f"Vet: {v.reason}",
            description=v.diagnosis,
            dog_names=[d_name]
        ))

    # Process Care Logs
    for c in clogs:
         # Need task info
         task_res = await db.execute(select(CareTask).where(CareTask.id == c.care_task_id))
         task = task_res.scalar_one()
         
         d_res = await db.execute(select(Dog.name).where(Dog.id == task.dog_id))
         d_name = d_res.scalar_one()
         
         activities.append(ActivityItem(
             type="CARE",
             id=c.id,
             datetime=c.done_at,
             title=f"Care: {task.title}",
             description=None,
             dog_names=[d_name]
         ))
    
    # Sort all by datetime desc
    activities.sort(key=lambda x: x.datetime, reverse=True)
    
    return activities[:limit]

