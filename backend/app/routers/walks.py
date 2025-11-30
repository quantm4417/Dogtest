from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.walks import Walk, WalkDog
from app.models.tags import Tag, TagAssignment
from app.schemas.walks import WalkCreate, WalkUpdate, WalkResponse
import shutil
import os
from pathlib import Path
import time

router = APIRouter()

async def assign_tags(db: AsyncSession, entity_type: str, entity_id: int, tag_ids: List[int], user_id: int):
    if not tag_ids:
        return
    result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id))
    valid_tags = result.scalars().all()
    for tag in valid_tags:
        assignment = TagAssignment(tag_id=tag.id, entity_type=entity_type, entity_id=entity_id)
        db.add(assignment)

@router.get("/", response_model=List[WalkResponse])
async def read_walks(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(Walk).where(Walk.user_id == current_user.id)
    
    if dog_id:
        # Join with WalkDog
        query = query.join(WalkDog).where(WalkDog.dog_id == dog_id)
        
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=WalkResponse)
async def create_walk(
    walk_in: WalkCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Verify dogs belong to user
    dogs_result = await db.execute(select(Dog).where(Dog.id.in_(walk_in.dog_ids), Dog.owner_user_id == current_user.id))
    valid_dogs = dogs_result.scalars().all()
    
    if len(valid_dogs) != len(set(walk_in.dog_ids)):
         raise HTTPException(status_code=400, detail="One or more dogs not found or access denied")

    walk_data = walk_in.model_dump(exclude={"dog_ids", "tag_ids"})
    walk = Walk(**walk_data, user_id=current_user.id)
    db.add(walk)
    await db.commit()
    await db.refresh(walk)
    
    # Associations
    for dog_id in walk_in.dog_ids:
        wd = WalkDog(walk_id=walk.id, dog_id=dog_id)
        db.add(wd)
        
    # Tags
    if walk_in.tag_ids:
        await assign_tags(db, "WALK", walk.id, walk_in.tag_ids, current_user.id)
        
    await db.commit()
    await db.refresh(walk)
    return walk

@router.post("/{walk_id}/gpx", response_model=WalkResponse)
async def upload_gpx(
    walk_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    file: UploadFile = File(...)
):
    result = await db.execute(select(Walk).where(Walk.id == walk_id, Walk.user_id == current_user.id))
    walk = result.scalars().first()
    if not walk:
        raise HTTPException(status_code=404, detail="Walk not found")
        
    # Validate file extension/type roughly
    if not file.filename.lower().endswith(('.gpx', '.xml')):
         raise HTTPException(status_code=400, detail="Invalid file type. Must be GPX/XML")

    upload_dir = Path("/app/media/walks/gpx")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{walk.id}_{int(time.time())}.gpx"
    file_path = upload_dir / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    walk.gpx_file_url = f"/media/walks/gpx/{filename}"
    walk.has_route_data = True
    
    await db.commit()
    await db.refresh(walk)
    return walk

@router.delete("/{walk_id}")
async def delete_walk(
    walk_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Walk).where(Walk.id == walk_id, Walk.user_id == current_user.id))
    walk = result.scalars().first()
    if not walk:
        raise HTTPException(status_code=404, detail="Walk not found")
    await db.delete(walk)
    await db.commit()
    return {"ok": True}

