from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.tags import Tag
from app.schemas.tags import TagCreate, TagResponse

router = APIRouter()

@router.get("/", response_model=List[TagResponse])
async def read_tags(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Tag).where(Tag.user_id == current_user.id))
    return result.scalars().all()

@router.post("/", response_model=TagResponse)
async def create_tag(
    tag_in: TagCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if exists
    result = await db.execute(select(Tag).where(Tag.user_id == current_user.id, Tag.name == tag_in.name))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Tag already exists")
        
    tag = Tag(user_id=current_user.id, name=tag_in.name)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag

@router.delete("/{tag_id}")
async def delete_tag(
    tag_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Tag).where(Tag.id == tag_id, Tag.user_id == current_user.id))
    tag = result.scalars().first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    await db.delete(tag)
    await db.commit()
    return {"ok": True}

