from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, asc
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.care import CareTask
from app.models.health import Vaccination, VetVisit
from pydantic import BaseModel
from datetime import date, timedelta

router = APIRouter()

class ReminderItem(BaseModel):
    type: str # CARE_TASK, VACCINATION, VET_VISIT
    id: int
    date: date
    title: str
    dog_name: str
    is_overdue: bool = False

@router.get("/upcoming", response_model=List[ReminderItem])
async def read_upcoming_reminders(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    days: int = 30
):
    today = date.today()
    limit_date = today + timedelta(days=days)
    
    reminders = []
    
    # Care Tasks (Due <= limit_date)
    # Also include overdue (due < today)
    tasks_query = select(CareTask).join(Dog).where(
        Dog.owner_user_id == current_user.id,
        CareTask.is_active == True,
        CareTask.next_due_date <= limit_date
    )
    tasks_res = await db.execute(tasks_query)
    tasks = tasks_res.scalars().all()
    
    for t in tasks:
        d_res = await db.execute(select(Dog.name).where(Dog.id == t.dog_id))
        d_name = d_res.scalar_one()
        reminders.append(ReminderItem(
            type="CARE_TASK",
            id=t.id,
            date=t.next_due_date,
            title=f"Care: {t.title}",
            dog_name=d_name,
            is_overdue=(t.next_due_date < today)
        ))

    # Vaccinations (Valid until <= limit_date)
    vax_query = select(Vaccination).join(Dog).where(
        Dog.owner_user_id == current_user.id,
        Vaccination.valid_until != None,
        Vaccination.valid_until <= limit_date,
        Vaccination.valid_until >= today - timedelta(days=365) # Don't show ancient expired ones
    )
    vax_res = await db.execute(vax_query)
    vaxs = vax_res.scalars().all()
    
    for v in vaxs:
        d_res = await db.execute(select(Dog.name).where(Dog.id == v.dog_id))
        d_name = d_res.scalar_one()
        reminders.append(ReminderItem(
            type="VACCINATION",
            id=v.id,
            date=v.valid_until,
            title=f"Vaccine Expiring: {v.vaccine_type}",
            dog_name=d_name,
            is_overdue=(v.valid_until < today)
        ))
        
    # Vet Visits (Date >= today and <= limit_date) - Future visits
    vet_query = select(VetVisit).join(Dog).where(
        Dog.owner_user_id == current_user.id,
        VetVisit.date >= today,
        VetVisit.date <= limit_date
    )
    vet_res = await db.execute(vet_query)
    vets = vet_res.scalars().all()
    
    for v in vets:
        d_res = await db.execute(select(Dog.name).where(Dog.id == v.dog_id))
        d_name = d_res.scalar_one()
        reminders.append(ReminderItem(
            type="VET_VISIT",
            id=v.id,
            date=v.date,
            title=f"Vet Visit: {v.reason}",
            dog_name=d_name,
            is_overdue=False
        ))

    # Sort by date
    reminders.sort(key=lambda x: x.date)
    return reminders

