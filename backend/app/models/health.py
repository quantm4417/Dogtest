from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class VetVisit(Base):
    __tablename__ = "vet_visits"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    date = Column(Date, nullable=False)
    vet_name = Column(String, nullable=True)
    reason = Column(String, nullable=False)
    diagnosis = Column(Text, nullable=True)
    treatment_and_medication = Column(Text, nullable=True)
    notes_markdown = Column(Text, nullable=True)
    
    dog = relationship("Dog", back_populates="vet_visits")
    invoices = relationship("Invoice", back_populates="vet_visit")

class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=False)
    date = Column(Date, nullable=False)
    vaccine_type = Column(String, nullable=False)
    valid_until = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    dog = relationship("Dog", back_populates="vaccinations")

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    dog_id = Column(Integer, ForeignKey("dogs.id"), nullable=True)
    vet_visit_id = Column(Integer, ForeignKey("vet_visits.id"), nullable=True)
    date = Column(Date, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="CHF")
    description = Column(String, nullable=True)
    file_url = Column(String, nullable=True)

    vet_visit = relationship("VetVisit", back_populates="invoices")

