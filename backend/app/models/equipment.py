from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class EquipmentType(str, enum.Enum):
    LEASH = "LEASH"
    HARNESS = "HARNESS"
    COLLAR = "COLLAR"
    TOY = "TOY"
    BED = "BED"
    BOWL = "BOWL"
    OTHER = "OTHER"

class EquipmentItem(Base):
    __tablename__ = "equipment_items"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    type = Column(Enum(EquipmentType), default=EquipmentType.OTHER)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    purchase_date = Column(Date, nullable=True)
    brand = Column(String, nullable=True)
    size = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    dog = relationship("Dog", back_populates="equipment")

