from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.bill import Bill
from app.schemas.bill import BillCreate, BillUpdate, BillResponse

# FIXED: Import from the new central dependency file to break the circular loop
from app.api.deps import get_current_user
from app.models.user import User

# MILESTONE 4: Logic Services
from app.services.bill_manager import BillManager
from app.services.reminder_service import ReminderService

router = APIRouter()

@router.get("/", response_model=List[BillResponse])
def get_bills(
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # FIXED: Use Dependency Injection
):
    """
    MILESTONE 4: Bill Analytics & Reminders.
    Fetches all bills, updates their status dynamically, and triggers background reminders.
    """
    bills = db.query(Bill).filter(Bill.user_id == current_user.id).all()
    
    # Intelligence Layer: Re-calculate status for all bills dynamically
    for bill in bills:
        bill.status = BillManager.get_updated_status(bill)
    
    db.commit() 
    
    # Milestone 4: Trigger email/push notifications as a background process
    background_tasks.add_task(ReminderService.process_bill_reminders, db, current_user.id)
    
    return bills

@router.post("/", response_model=BillResponse, status_code=status.HTTP_201_CREATED)
def create_bill(
    bill_in: BillCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    MILESTONE 4: Automation.
    Registers a new bill and automatically determines its initial status.
    """
    new_bill = Bill(**bill_in.model_dump(), user_id=current_user.id)
    
    # Set initial status (Pending or Overdue) using the Logic Service
    new_bill.status = BillManager.get_updated_status(new_bill)
    
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    return new_bill

@router.put("/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: int, 
    bill_update: BillUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    MILESTONE 4: Bill Management.
    Updates bill details and re-calculates status based on payment logic.
    """
    db_bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == current_user.id).first()
    
    if not db_bill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill not found.")
    
    # Modern Pydantic v2 update logic
    update_data = bill_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bill, key, value)
    
    # Re-calculate status in case the due_date or amount_paid was changed
    db_bill.status = BillManager.get_updated_status(db_bill)
    
    db.commit()
    db.refresh(db_bill)
    return db_bill

@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill(
    bill_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Removes a bill from the tracking system.
    """
    bill = db.query(Bill).filter(Bill.id == bill_id, Bill.user_id == current_user.id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    db.delete(bill)
    db.commit()
    return None