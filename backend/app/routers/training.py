from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.models.dogs import Dog
from app.models.training import TrainingGoal, BehaviorIssue, TrainingLog
from app.models.tags import Tag, TagAssignment
from app.schemas.training import (
    TrainingGoalCreate, TrainingGoalUpdate, TrainingGoalResponse,
    BehaviorIssueCreate, BehaviorIssueUpdate, BehaviorIssueResponse,
    TrainingLogCreate, TrainingLogResponse
)

router = APIRouter()

# Helpers
async def check_dog_permission(db: AsyncSession, dog_id: int, user_id: int):
    result = await db.execute(select(Dog).where(Dog.id == dog_id, Dog.owner_user_id == user_id))
    if not result.scalars().first():
        raise HTTPException(status_code=404, detail="Dog not found")

async def assign_tags(db: AsyncSession, entity_type: str, entity_id: int, tag_ids: List[int], user_id: int):
    if not tag_ids:
        return
    
    # Verify tags exist and belong to user
    result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids), Tag.user_id == user_id))
    valid_tags = result.scalars().all()
    if len(valid_tags) != len(tag_ids):
        raise HTTPException(status_code=400, detail="Invalid tag IDs")
        
    for tag in valid_tags:
        assignment = TagAssignment(tag_id=tag.id, entity_type=entity_type, entity_id=entity_id)
        db.add(assignment)

# GOALS
@router.get("/goals", response_model=List[TrainingGoalResponse])
async def read_goals(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(TrainingGoal).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(TrainingGoal.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/goals", response_model=TrainingGoalResponse)
async def create_goal(
    goal_in: TrainingGoalCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_dog_permission(db, goal_in.dog_id, current_user.id)
    goal = TrainingGoal(**goal_in.model_dump())
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal

@router.put("/goals/{goal_id}", response_model=TrainingGoalResponse)
async def update_goal(
    goal_id: int,
    goal_in: TrainingGoalUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(TrainingGoal).join(Dog).where(TrainingGoal.id == goal_id, Dog.owner_user_id == current_user.id))
    goal = result.scalars().first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
        
    update_data = goal_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(goal, key, value)
        
    await db.commit()
    await db.refresh(goal)
    return goal

@router.delete("/goals/{goal_id}")
async def delete_goal(
    goal_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(TrainingGoal).join(Dog).where(TrainingGoal.id == goal_id, Dog.owner_user_id == current_user.id))
    goal = result.scalars().first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    await db.delete(goal)
    await db.commit()
    return {"ok": True}

# ISSUES
@router.get("/issues", response_model=List[BehaviorIssueResponse])
async def read_issues(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(BehaviorIssue).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(BehaviorIssue.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/issues", response_model=BehaviorIssueResponse)
async def create_issue(
    issue_in: BehaviorIssueCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_dog_permission(db, issue_in.dog_id, current_user.id)
    issue = BehaviorIssue(**issue_in.model_dump())
    db.add(issue)
    await db.commit()
    await db.refresh(issue)
    return issue

@router.put("/issues/{issue_id}", response_model=BehaviorIssueResponse)
async def update_issue(
    issue_id: int,
    issue_in: BehaviorIssueUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(BehaviorIssue).join(Dog).where(BehaviorIssue.id == issue_id, Dog.owner_user_id == current_user.id))
    issue = result.scalars().first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
        
    update_data = issue_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(issue, key, value)
    await db.commit()
    await db.refresh(issue)
    return issue

@router.delete("/issues/{issue_id}")
async def delete_issue(
    issue_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(BehaviorIssue).join(Dog).where(BehaviorIssue.id == issue_id, Dog.owner_user_id == current_user.id))
    issue = result.scalars().first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    await db.delete(issue)
    await db.commit()
    return {"ok": True}

# LOGS
@router.get("/logs", response_model=List[TrainingLogResponse])
async def read_logs(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
    dog_id: Optional[int] = None
):
    query = select(TrainingLog).join(Dog).where(Dog.owner_user_id == current_user.id)
    if dog_id:
        query = query.where(TrainingLog.dog_id == dog_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/logs", response_model=TrainingLogResponse)
async def create_log(
    log_in: TrainingLogCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    await check_dog_permission(db, log_in.dog_id, current_user.id)
    
    # Verify goal/issue if provided
    if log_in.training_goal_id:
         g = await db.execute(select(TrainingGoal).where(TrainingGoal.id == log_in.training_goal_id))
         if not g.scalars().first(): raise HTTPException(404, "Goal not found")
         
    if log_in.behavior_issue_id:
         i = await db.execute(select(BehaviorIssue).where(BehaviorIssue.id == log_in.behavior_issue_id))
         if not i.scalars().first(): raise HTTPException(404, "Issue not found")

    log_data = log_in.model_dump(exclude={"tag_ids"})
    log = TrainingLog(**log_data)
    db.add(log)
    await db.commit()
    await db.refresh(log)
    
    if log_in.tag_ids:
        await assign_tags(db, "TRAINING_LOG", log.id, log_in.tag_ids, current_user.id)
        await db.commit()
        
    return log

@router.delete("/logs/{log_id}")
async def delete_log(
    log_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(TrainingLog).join(Dog).where(TrainingLog.id == log_id, Dog.owner_user_id == current_user.id))
    log = result.scalars().first()
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    await db.delete(log)
    await db.commit()
    return {"ok": True}

