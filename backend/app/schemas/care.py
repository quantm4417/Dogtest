from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class IntervalType(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    CUSTOM_DAYS = "CUSTOM_DAYS"

class CareTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    interval_type: IntervalType
    interval_days: Optional[int] = None
    next_due_date: date
    is_active: bool = True

class CareTaskCreate(CareTaskBase):
    dog_id: int

class CareTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    interval_type: Optional[IntervalType] = None
    interval_days: Optional[int] = None
    next_due_date: Optional[date] = None
    is_active: Optional[bool] = None

class CareTaskResponse(CareTaskBase):
    id: int
    dog_id: int

    class Config:
        from_attributes = True

class CareTaskLogBase(BaseModel):
    done_at: datetime
    notes: Optional[str] = None

class CareTaskLogResponse(CareTaskLogBase):
    id: int
    care_task_id: int

    class Config:
        from_attributes = True

