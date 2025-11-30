from sqlalchemy import Column, Integer, String, Date, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class SexEnum(str, enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNKNOWN = "UNKNOWN"

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    owner_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    sex = Column(Enum(SexEnum), default=SexEnum.UNKNOWN)
    weight_kg = Column(Float, nullable=True)
    avatar_image_url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    details = relationship("DogProfileDetails", uselist=False, back_populates="dog", cascade="all, delete-orphan")
    vet_visits = relationship("VetVisit", back_populates="dog", cascade="all, delete-orphan")
    vaccinations = relationship("Vaccination", back_populates="dog", cascade="all, delete-orphan")
    care_tasks = relationship("CareTask", back_populates="dog", cascade="all, delete-orphan")
    training_goals = relationship("TrainingGoal", back_populates="dog", cascade="all, delete-orphan")
    behavior_issues = relationship("BehaviorIssue", back_populates="dog", cascade="all, delete-orphan")
    training_logs = relationship("TrainingLog", back_populates="dog", cascade="all, delete-orphan")
    walk_associations = relationship("WalkDog", back_populates="dog", cascade="all, delete-orphan")
    equipment = relationship("EquipmentItem", back_populates="dog", cascade="all, delete-orphan")

class DogProfileDetails(Base):
    __tablename__ = "dog_profile_details"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), unique=True, nullable=False)
    allergies = Column(Text, nullable=True)
    forbidden_foods = Column(Text, nullable=True)
    preferred_foods = Column(Text, nullable=True)
    diagnosed_conditions = Column(Text, nullable=True)
    care_notes = Column(Text, nullable=True)

    dog = relationship("Dog", back_populates="details")

