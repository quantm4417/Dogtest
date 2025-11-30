from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class GoalStatus(str, Enum):
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    PAUSED = "PAUSED"

class TrainingGoalBase(BaseModel):
    title: str
    category: Optional[str] = None
    status: GoalStatus = GoalStatus.PLANNED
    priority: int = 1
    description: Optional[str] = None

class TrainingGoalCreate(TrainingGoalBase):
    dog_id: int

class TrainingGoalUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    status: Optional[GoalStatus] = None
    priority: Optional[int] = None
    description: Optional[str] = None

class TrainingGoalResponse(TrainingGoalBase):
    id: int
    dog_id: int
    
    class Config:
        from_attributes = True

class BehaviorIssueBase(BaseModel):
    title: str
    description: str
    typical_triggers: Optional[str] = None
    severity: int

class BehaviorIssueCreate(BehaviorIssueBase):
    dog_id: int

class BehaviorIssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    typical_triggers: Optional[str] = None
    severity: Optional[int] = None

class BehaviorIssueResponse(BehaviorIssueBase):
    id: int
    dog_id: int

    class Config:
        from_attributes = True

class TrainingLogBase(BaseModel):
    datetime: datetime
    rating: Optional[int] = None
    notes_markdown: Optional[str] = None
    video_urls_json: List[str] = []

class TrainingLogCreate(TrainingLogBase):
    dog_id: int
    training_goal_id: Optional[int] = None
    behavior_issue_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class TrainingLogResponse(TrainingLogBase):
    id: int
    dog_id: int
    training_goal_id: Optional[int]
    behavior_issue_id: Optional[int]
    
    # We will add tags later when we define TagResponse
    
    class Config:
        from_attributes = True

