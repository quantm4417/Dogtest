from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.health import VetVisit, Vaccination, Invoice
from app.schemas.health import (
    VetVisitCreate, VetVisitUpdate, VetVisitResponse,
    VaccinationCreate, VaccinationUpdate, VaccinationResponse,
    InvoiceCreate, InvoiceResponse
)
import shutil
import os
from pathlib import Path
import time

router = APIRouter()

# Helpers
async def check_dog_permission(db: AsyncSession, dog_id: int, user_id: int):
    result = await db.execute(select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == user_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found or access denied")

# VET VISITS
@router.get("/vet-visits", response_model=List[VetVisitResponse])
async def read_vet_visits(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(VetVisit).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(VetVisit.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/vet-visits", response_model=VetVisitResponse)
async def create_vet_visit(
    visit_in: VetVisitCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_dog_permission(db, visit_in.dog_id, current_user.id)
    visit = VetVisit(**visit_in.model_dump())
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit

@router.put("/vet-visits/{visit_id}", response_model=VetVisitResponse)
async def update_vet_visit(
    visit_id: int,
    visit_in: VetVisitUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(VetVisit).join(Dog).where(VetVisit.id == visit_id, Dog.owner_user_id == current_user.id))
    visit = result.scalars().first()
    if not visit:
        raise HTTPException(status_code=404, detail="Vet visit not found")
    
    update_data = visit_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(visit, key, value)
    await db.commit()
    await db.refresh(visit)
    return visit

@router.delete("/vet-visits/{visit_id}")
async def delete_vet_visit(
    visit_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(VetVisit).join(Dog).where(VetVisit.id == visit_id, Dog.owner_user_id == current_user.id))
    visit = result.scalars().first()
    if not visit:
        raise HTTPException(status_code=404, detail="Vet visit not found")
    await db.delete(visit)
    await db.commit()
    return {"ok": True}

# VACCINATIONS
@router.get("/vaccinations", response_model=List[VaccinationResponse])
async def read_vaccinations(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(Vaccination).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(Vaccination.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/vaccinations", response_model=VaccinationResponse)
async def create_vaccination(
    vax_in: VaccinationCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_dog_permission(db, vax_in.dog_id, current_user.id)
    vax = Vaccination(**vax_in.model_dump())
    db.add(vax)
    await db.commit()
    await db.refresh(vax)
    return vax

@router.put("/vaccinations/{vax_id}", response_model=VaccinationResponse)
async def update_vaccination(
    vax_id: int,
    vax_in: VaccinationUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Vaccination).join(Dog).where(Vaccination.id == vax_id, Dog.owner_user_id == current_user.id))
    vax = result.scalars().first()
    if not vax:
        raise HTTPException(status_code=404, detail="Vaccination not found")
        
    update_data = vax_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vax, key, value)
    await db.commit()
    await db.refresh(vax)
    return vax

@router.delete("/vaccinations/{vax_id}")
async def delete_vaccination(
    vax_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Vaccination).join(Dog).where(Vaccination.id == vax_id, Dog.owner_user_id == current_user.id))
    vax = result.scalars().first()
    if not vax:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    await db.delete(vax)
    await db.commit()
    return {"ok": True}

# INVOICES
@router.get("/invoices", response_model=List[InvoiceResponse])
async def read_invoices(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    # Since invoices can be linked to Dog directly OR via VetVisit, filtering is tricky if done purely on Dog ID.
    # But typically they are linked to Dog. If only linked to VetVisit, we need to join VetVisit -> Dog.
    # For simplicity, we assume if dog_id is provided on Invoice, we use it.
    # But better: Join both ways.
    
    query = select(Invoice)
    # We must filter by user ownership. This requires joins since Invoice doesn't have user_id.
    # Join Invoice -> Dog (optional)
    # Join Invoice -> VetVisit (optional) -> Dog
    
    # This is complex in SQL. Let's handle "Direct Dog" and "Via VetVisit" separately or assume strict linking.
    # Schema says: dog_id (FK -> dogs.id, optional), vet_visit_id (FK -> vet_visits.id, optional)
    # One of them should be set.
    
    # Safe way: Fetch all user dogs, then fetch invoices where dog_id IN user_dogs OR vet_visit.dog_id IN user_dogs.
    
    user_dogs_result = await db.execute(select(Dog.id).where(Dog.owner_user_id == current_user.id))
    user_dog_ids = user_dogs_result.scalars().all()
    
    if not user_dog_ids:
        return []
        
    # If filtering by specific dog
    if dog_id:
        if dog_id not in user_dog_ids:
             raise HTTPException(status_code=404, detail="Dog not found")
        target_dog_ids = [dog_id]
    else:
        target_dog_ids = user_dog_ids

    # Construct query
    # Invoices where dog_id IN target OR (vet_visit.dog_id IN target)
    
    # We can do this with a JOIN to VetVisit (outer)
    query = select(Invoice).outerjoin(VetVisit, Invoice.vet_visit_id == VetVisit.id).where(
        ((Invoice.dog_id.in_(target_dog_ids)) | (VetVisit.dog_id.in_(target_dog_ids)))
    )
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/invoices", response_model=InvoiceResponse)
async def create_invoice(
    inv_in: InvoiceCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Validate permissions
    if inv_in.dog_id:
        await check_dog_permission(db, inv_in.dog_id, current_user.id)
    
    if inv_in.vet_visit_id:
        # Check vet visit ownership
        vv_result = await db.execute(select(VetVisit).join(Dog).where(VetVisit.id == inv_in.vet_visit_id, Dog.owner_user_id == current_user.id))
        if not vv_result.scalars().first():
             raise HTTPException(status_code=404, detail="Vet visit not found or access denied")
             
    if not inv_in.dog_id and not inv_in.vet_visit_id:
        raise HTTPException(status_code=400, detail="Invoice must be linked to a dog or a vet visit")

    inv = Invoice(**inv_in.model_dump())
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv

@router.post("/invoices/{invoice_id}/file", response_model=InvoiceResponse)
async def upload_invoice_file(
    invoice_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...)
):
    # Check invoice ownership
    # This is tricky because we need to verify the invoice belongs to one of the user's dogs.
    # Fetch invoice first
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
        
    # Verify ownership
    user_dogs_result = await db.execute(select(Dog.id).where(Dog.owner_user_id == current_user.id))
    user_dog_ids = user_dogs_result.scalars().all()
    
    has_access = False
    if invoice.dog_id and invoice.dog_id in user_dog_ids:
        has_access = True
    elif invoice.vet_visit_id:
        # Check via vet visit
        vv_result = await db.execute(select(VetVisit).where(VetVisit.id == invoice.vet_visit_id))
        vv = vv_result.scalars().first()
        if vv and vv.dog_id in user_dog_ids:
            has_access = True
            
    if not has_access:
        raise HTTPException(status_code=403, detail="Access denied")

    # Validate file
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    upload_dir = Path("/app/media/invoices")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    ext = ".pdf"
    if file.content_type == "image/jpeg": ext = ".jpg"
    elif file.content_type == "image/png": ext = ".png"
    
    filename = f"{invoice_id}_{int(time.time())}{ext}"
    file_path = upload_dir / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    invoice.file_url = f"/media/invoices/{filename}"
    await db.commit()
    await db.refresh(invoice)
    return invoice

