from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class WalkMood(str, Enum):
    CALM = "CALM"
    NORMAL = "NORMAL"
    STRESSED = "STRESSED"

class WalkBase(BaseModel):
    start_datetime: datetime
    duration_minutes: int
    mood: WalkMood = WalkMood.NORMAL
    distance_km: Optional[float] = None
    notes_markdown: Optional[str] = None
    video_urls_json: List[str] = []

class WalkCreate(WalkBase):
    dog_ids: List[int]
    tag_ids: Optional[List[int]] = []

class WalkUpdate(BaseModel):
    start_datetime: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    mood: Optional[WalkMood] = None
    distance_km: Optional[float] = None
    notes_markdown: Optional[str] = None
    video_urls_json: Optional[List[str]] = None
    dog_ids: Optional[List[int]] = None

class WalkResponse(WalkBase):
    id: int
    user_id: int
    gpx_file_url: Optional[str]
    has_route_data: bool
    
    # We will need to include Dog info here probably, or just IDs
    
    class Config:
        from_attributes = True

