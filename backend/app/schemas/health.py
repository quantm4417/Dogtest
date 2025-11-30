from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

# Vet Visits
class VetVisitBase(BaseModel):
    date: date
    vet_name: Optional[str] = None
    reason: str
    diagnosis: Optional[str] = None
    treatment_and_medication: Optional[str] = None
    notes_markdown: Optional[str] = None

class VetVisitCreate(VetVisitBase):
    dog_id: int

class VetVisitUpdate(BaseModel):
    date: Optional[date] = None
    vet_name: Optional[str] = None
    reason: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment_and_medication: Optional[str] = None
    notes_markdown: Optional[str] = None

class VetVisitResponse(VetVisitBase):
    id: int
    dog_id: int
    
    class Config:
        from_attributes = True

# Vaccinations
class VaccinationBase(BaseModel):
    date: date
    vaccine_type: str
    valid_until: Optional[date] = None
    notes: Optional[str] = None

class VaccinationCreate(VaccinationBase):
    dog_id: int

class VaccinationUpdate(BaseModel):
    date: Optional[date] = None
    vaccine_type: Optional[str] = None
    valid_until: Optional[date] = None
    notes: Optional[str] = None

class VaccinationResponse(VaccinationBase):
    id: int
    dog_id: int

    class Config:
        from_attributes = True

# Invoices
class InvoiceBase(BaseModel):
    date: date
    amount: float
    currency: str = "CHF"
    description: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    dog_id: Optional[int] = None
    vet_visit_id: Optional[int] = None

class InvoiceResponse(InvoiceBase):
    id: int
    dog_id: Optional[int]
    vet_visit_id: Optional[int]
    file_url: Optional[str]

    class Config:
        from_attributes = True

