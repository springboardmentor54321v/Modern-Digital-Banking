from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.reward import Reward
from app.models.bill import Bill
from app.models.user import User
from app.schemas.reward import RewardResponse, RewardUpdate

router = APIRouter(tags=["Milestone 4: Rewards Tracking"])

# --- Helper Logic ---
def get_demo_user(db: Session):
    """Ensures a user context exists for the demo."""
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No users found. Register via /auth/register first."
        )
    return user

# --- Endpoints ---

@router.post("/", response_model=RewardResponse, status_code=status.HTTP_201_CREATED)
def create_reward(reward_in: RewardUpdate, db: Session = Depends(get_db)):
    """
    MILESTONE 4: Create a new reward program.
    Run this first to avoid '404 Not Found' when updating!
    """
    user = get_demo_user(db)
    new_reward = Reward(**reward_in.model_dump(), user_id=user.id)
    db.add(new_reward)
    db.commit()
    db.refresh(new_reward)
    return new_reward

@router.get("/balance", response_model=dict)
def get_rewards_balance(db: Session = Depends(get_db)):
    """
    MILESTONE 4 INTELLIGENCE: 
    Calculates total reward points ($10 per paid bill).
    """
    user = get_demo_user(db)
    
    # Logic: Count bills where status is 'paid'
    paid_bills_count = db.query(Bill).filter(
        Bill.user_id == user.id, 
        Bill.status == "paid" 
    ).count()
    
    return {
        "user_id": user.id,
        "user_name": user.name,
        "paid_bills_processed": paid_bills_count,
        "points_balance": paid_bills_count * 10
    }

@router.get("/", response_model=List[RewardResponse])
def get_all_rewards(db: Session = Depends(get_db)):
    """Retrieve all reward programs available in the catalog."""
    return db.query(Reward).all()

@router.put("/{reward_id}", response_model=RewardResponse)
def update_reward_program(
    reward_id: int = Path(..., description="The ID of the reward to update", gt=0), 
    reward_update: RewardUpdate = None, 
    db: Session = Depends(get_db)
):
    """
    MILESTONE 4: Update metadata for a reward.
    Uses model_dump(exclude_unset=True) for partial updates.
    """
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    
    if not reward:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Reward ID {reward_id} not found. Create it first using POST."
        )
    
    # Update only the fields provided in the JSON
    update_data = reward_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reward, key, value)
    
    db.commit()
    db.refresh(reward)
    return reward