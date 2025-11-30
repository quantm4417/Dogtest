from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Enum, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class WalkMood(str, enum.Enum):
    CALM = "CALM"
    NORMAL = "NORMAL"
    STRESSED = "STRESSED"

class Walk(Base):
    __tablename__ = "walks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    start_datetime = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    mood = Column(Enum(WalkMood), default=WalkMood.NORMAL)
    distance_km = Column(Float, nullable=True)
    notes_markdown = Column(Text, nullable=True)
    video_urls_json = Column(JSON, default=list)
    gpx_file_url = Column(String, nullable=True)
    has_route_data = Column(Boolean, default=False)

    # Relationships
    dog_associations = relationship("WalkDog", back_populates="walk", cascade="all, delete-orphan")

class WalkDog(Base):
    __tablename__ = "walk_dogs"

    walk_id = Column(Integer, ForeignKey("walks.id"), primary_key=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), primary_key=True)

    walk = relationship("Walk", back_populates="dog_associations")
    dog = relationship("Dog", back_populates="walk_associations")

