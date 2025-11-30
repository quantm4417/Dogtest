from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class SexEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"

# Dog Profile Details
class DogProfileDetailsBase(BaseModel):
    allergies: Optional[str] = None
    forbidden_foods: Optional[str] = None
    preferred_foods: Optional[str] = None
    diagnosed_conditions: Optional[str] = None
    care_notes: Optional[str] = None

class DogProfileDetailsCreate(DogProfileDetailsBase):
    pass

class DogProfileDetailsResponse(DogProfileDetailsBase):
    id: int
    dog_id: int

    class Config:
        from_attributes = True

# Dog
class DogBase(BaseModel):
    name: str
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: SexEnum = SexEnum.UNKNOWN
    weight_kg: Optional[float] = None
    notes: Optional[str] = None

class DogCreate(DogBase):
    pass

class DogUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Optional[SexEnum] = None
    weight_kg: Optional[float] = None
    notes: Optional[str] = None

class DogResponse(DogBase):
    id: int
    owner_user_id: int
    avatar_image_url: Optional[str] = None
    details: Optional[DogProfileDetailsResponse] = None

    class Config:
        from_attributes = True

