from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class GoalStatus(str, enum.Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"

class TrainingGoal(Base):
    __tablename__ = "training_goals"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    status = Column(Enum(GoalStatus), default=GoalStatus.PLANNED)
    priority = Column(Integer, default=1) # 1-3
    description = Column(Text, nullable=True)

    dog = relationship("Dog", back_populates="training_goals")
    logs = relationship("TrainingLog", back_populates="goal")

class BehaviorIssue(Base):
    __tablename__ = "behavior_issues"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    typical_triggers = Column(Text, nullable=True)
    severity = Column(Integer, nullable=False) # 1-3

    dog = relationship("Dog", back_populates="behavior_issues")
    logs = relationship("TrainingLog", back_populates="behavior_issue")

class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    training_goal_id = Column(Integer, ForeignKey("training_goals.id"), nullable=True)
    behavior_issue_id = Column(Integer, ForeignKey("behavior_issues.id"), nullable=True)
    datetime = Column(DateTime(timezone=True), nullable=False)
    rating = Column(Integer, nullable=True) # 1-5
    notes_markdown = Column(Text, nullable=True)
    video_urls_json = Column(JSON, default=list)

    dog = relationship("Dog", back_populates="training_logs")
    goal = relationship("TrainingGoal", back_populates="logs")
    behavior_issue = relationship("BehaviorIssue", back_populates="logs")

