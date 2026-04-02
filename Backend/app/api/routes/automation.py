from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alert_service import check_upcoming_bills, check_budget_exceeded
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/run-daily-bill-check")
async def trigger_daily_bills(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    MANUAL TRIGGER: Simulates the 'Every Day' scheduled job.
    Scans all users for bills due in the next 3 days and inserts alerts.
    """
    # In a real app, this runs via a Celery Beat or a Cron job.
    # For the demo, we trigger it here to show the logic works.
    users = db.query(User).all()
    for user in users:
        background_tasks.add_task(check_upcoming_bills, db, user_id=user.id)
    
    return {"message": f"Automation started: Scanning bills for {len(users)} users."}

@router.post("/run-budget-audit")
async def trigger_budget_audit(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    MANUAL TRIGGER: Simulates the 'Every Few Hours' audit.
    Checks if any user has exceeded 80% of their category limits.
    """
    users = db.query(User).all()
    for user in users:
        # This logic scans their transactions vs their budget limits
        background_tasks.add_task(check_budget_exceeded, db, user_id=user.id)
        
    return {"message": "Budget audit automation triggered."}