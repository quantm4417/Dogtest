from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class EquipmentType(str, Enum):
    LEASH = "LEASH"
    HARNESS = "HARNESS"
    COLLAR = "COLLAR"
    TOY = "TOY"
    BED = "BED"
    BOWL = "BOWL"
    OTHER = "OTHER"

class EquipmentBase(BaseModel):
    type: EquipmentType
    name: str
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class EquipmentCreate(EquipmentBase):
    dog_id: int

class EquipmentUpdate(BaseModel):
    type: Optional[EquipmentType] = None
    name: Optional[str] = None
    description: Optional[str] = None
    purchase_date: Optional[date] = None
    brand: Optional[str] = None
    size: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class EquipmentResponse(EquipmentBase):
    id: int
    dog_id: int

    class Config:
        from_attributes = True

