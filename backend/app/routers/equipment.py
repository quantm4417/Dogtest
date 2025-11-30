from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.equipment import EquipmentItem
from app.schemas.equipment import EquipmentCreate, EquipmentUpdate, EquipmentResponse

router = APIRouter()

@router.get("/", response_model=List[EquipmentResponse])
async def read_equipment(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: int = None
):
    query = select(EquipmentItem).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(EquipmentItem.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=EquipmentResponse)
async def create_equipment(
    item_in: EquipmentCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # Verify dog
    dog_result = await db.execute(select(Dog).where(Dog.id == item_in.dog_id, Dog.owner_user_id == current_user.id))
    if not dog_result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found")
        
    item = EquipmentItem(**item_in.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.put("/{item_id}", response_model=EquipmentResponse)
async def update_equipment(
    item_id: int,
    item_in: EquipmentUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(EquipmentItem).join(Dog).where(EquipmentItem.id == item_id, Dog.owner_user_id == current_user.id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Equipment not found")
        
    update_data = item_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
        
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}")
async def delete_equipment(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(EquipmentItem).join(Dog).where(EquipmentItem.id == item_id, Dog.owner_user_id == current_user.id))
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Equipment not found")
        
    await db.delete(item)
    await db.commit()
    return {"ok": True}

