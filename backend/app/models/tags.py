from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)

    assignments = relationship("TagAssignment", back_populates="tag", cascade="all, delete-orphan")

class TagAssignment(Base):
    __tablename__ = "tag_assignments"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    entity_type = Column(String, nullable=False) # "TRAINING_LOG", "WALK"
    entity_id = Column(Integer, nullable=False)

    tag = relationship("Tag", back_populates="assignments")

