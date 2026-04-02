from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.alert_service import AlertService
from app.models.user import User

# Global variable to track scheduler state
scheduler = BackgroundScheduler()

def run_financial_checks():
    """
    The 'Backend Brain' job: Iterates through all users to check for 
    low balances, exceeded budgets, and upcoming bills.
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        if not users:
            print(" Scheduler: No users found to check.")
            return

        for user in users:
            # 1. Check for balances below threshold
            AlertService.check_low_balance(db, user.id)
            
            # 2. Compare spending vs budget limits
            AlertService.check_budget_exceeded(db, user.id)
            
            # 3. Look for bills due in the next 3 days
            AlertService.check_upcoming_bills(db, user.id)
            
        print(f"Scheduled Financial Checks Completed for {len(users)} users.")
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

def start_scheduler():
    """
    Initializes and starts the background job interval.
    """
    # Check if the scheduler is already active to prevent duplicate jobs
    if not scheduler.running:
        # Runs every 6 hours as per your requirements
        # For testing during your demo, you can change 'hours=6' to 'minutes=1'
        scheduler.add_job(
            run_financial_checks, 
            'interval', 
            hours=6, 
            id='financial_monitoring_job',
            replace_existing=True
        )
        scheduler.start()
        print(" Milestone 4: Background Automation Scheduler Started (Interval: 6h).")
    else:
        print("Scheduler is already running.")