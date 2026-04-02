from sqlalchemy.orm import Session
from app.models.user import User
from app.models.alert import Alert
from app.services.alert_logic import check_user_budgets, check_user_balance

def run_daily_financial_checks(db: Session):
    """
    Automated job to scan all users for budget overflows or low balances.
    This is Task 4 of Milestone 4.
    """
    users = db.query(User).all()
    for user in users:
        # These functions will live in your services/alert_logic.py
        check_user_budgets(db, user.id)
        check_user_balance(db, user.id)
    
    db.commit()
    print("Successfully ran daily background financial checks.")