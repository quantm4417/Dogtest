from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog, DogProfileDetails
from app.schemas.dogs import DogCreate, DogUpdate, DogResponse, DogProfileDetailsCreate, DogProfileDetailsResponse
import shutil
import os
from pathlib import Path

router = APIRouter()

@router.get("/", response_model=List[DogResponse])
async def read_dogs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100
):
    result = await db.execute(
        select(Dog).where(Dog.owner_user_id == current_user.id).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=DogResponse)
async def create_dog(
    dog_in: DogCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    dog = Dog(**dog_in.model_dump(), owner_user_id=current_user.id)
    db.add(dog)
    await db.commit()
    await db.refresh(dog)
    
    # Create empty profile details automatically
    details = DogProfileDetails(dog_id=dog.id)
    db.add(details)
    await db.commit()
    
    return dog

@router.get("/{dog_id}", response_model=DogResponse)
async def read_dog(
    dog_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    dog = result.scalars().first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    return dog

@router.patch("/{dog_id}", response_model=DogResponse)
async def update_dog(
    dog_id: int,
    dog_in: DogUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    dog = result.scalars().first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    update_data = dog_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dog, key, value)
    
    await db.commit()
    await db.refresh(dog)
    return dog

@router.delete("/{dog_id}")
async def delete_dog(
    dog_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    dog = result.scalars().first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")
    
    await db.delete(dog)
    await db.commit()
    return {"ok": True}

# Profile Details
@router.get("/{dog_id}/details", response_model=DogProfileDetailsResponse)
async def read_dog_details(
    dog_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Verify dog ownership
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found")
        
    result = await db.execute(select(DogProfileDetails).where(DogProfileDetails.dog_id == dog_id))
    details = result.scalars().first()
    if not details:
         # Should have been created on dog creation, but handle edge case
         details = DogProfileDetails(dog_id=dog_id)
         db.add(details)
         await db.commit()
         await db.refresh(details)
    return details

@router.put("/{dog_id}/details", response_model=DogProfileDetailsResponse)
async def update_dog_details(
    dog_id: int,
    details_in: DogProfileDetailsCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Verify dog ownership
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found")
        
    result = await db.execute(select(DogProfileDetails).where(DogProfileDetails.dog_id == dog_id))
    details = result.scalars().first()
    if not details:
        details = DogProfileDetails(dog_id=dog_id)
        db.add(details)
    
    update_data = details_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(details, key, value)
        
    await db.commit()
    await db.refresh(details)
    return details

# Avatar Upload
@router.post("/{dog_id}/avatar", response_model=DogResponse)
async def upload_avatar(
    dog_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...)
):
    # Verify dog ownership
    result = await db.execute(
        select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == current_user.id)
    )
    dog = result.scalars().first()
    if not dog:
        raise HTTPException(status_code=404, detail="Dog not found")

    # Validate file
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save file
    upload_dir = Path("/app/media/dogs/avatars")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_ext = ".jpg" if file.content_type == "image/jpeg" else ".png"
    filename = f"{dog.id}_{int(os.path.getmtime(upload_dir) if upload_dir.exists() else 0)}{file_ext}" # Simple unique name
    # Better unique name
    import time
    filename = f"{dog.id}_{int(time.time())}{file_ext}"
    file_path = upload_dir / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Update URL
    # Assuming we serve media at /media
    dog.avatar_image_url = f"/media/dogs/avatars/{filename}"
    await db.commit()
    await db.refresh(dog)
    return dog

