from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class IntervalType(str, enum.Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    CUSTOM_DAYS = "CUSTOM_DAYS"

class CareTask(Base):
    __tablename__ = "care_tasks"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    interval_type = Column(Enum(IntervalType), nullable=False)
    interval_days = Column(Integer, nullable=True)
    next_due_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    dog = relationship("Dog", back_populates="care_tasks")
    logs = relationship("CareTaskLog", back_populates="task", cascade="all, delete-orphan")

class CareTaskLog(Base):
    __tablename__ = "care_task_logs"

    id = Column(Integer, primary_key=True, index=True)
    care_task_id = Column(Integer, ForeignKey("care_tasks.id"), nullable=False)
    done_at = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text, nullable=True)

    task = relationship("CareTask", back_populates="logs")

