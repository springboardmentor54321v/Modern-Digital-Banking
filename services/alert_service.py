from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import logging

from app.models.transaction import Transaction
from app.models.alert import Alert
from app.models.account import Account
from app.models.budget import Budget
from app.models.bill import Bill

# Setup logging for background execution visibility
logger = logging.getLogger(__name__)

def check_low_balance(db: Session, user_id: int, account_id: int, threshold: float = 100.0):
    """
    MILESTONE 4: Real-time Account Monitoring.
    Generates an alert if balance drops below threshold, with anti-spam check.
    """
    try:
        account = db.query(Account).filter(Account.id == account_id, Account.user_id == user_id).first()
        
        if account and account.balance < threshold:
            # Anti-spam: Don't create a new alert if an unread one for this account already exists
            existing_alert = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.message.like(f"%{account.account_name}%"),
                Alert.is_read == False
            ).first()

            if not existing_alert:
                new_alert = Alert(
                    user_id=user_id,
                    message=f"Low Balance Alert: Your account '{account.account_name}' is currently at ${account.balance:,.2f}.",
                    is_read=False,
                    created_at=datetime.now()
                )
                db.add(new_alert)
                db.commit()
                logger.info(f"Low balance alert created for User {user_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error in low balance check: {e}")

def check_budget_exceeded(db: Session, user_id: int, amount: float, category: str):
    """
    MILESTONE 4: Proactive Budget Audit.
    Syncs with the 'Budgets' table to check for category overruns.
    """
    try:
        # 1. Fetch user-defined budget for this category
        budget = db.query(Budget).filter(Budget.user_id == user_id, Budget.category == category).first()
        
        # If no specific budget exists, use a global default of 500 for the demo
        BUDGET_LIMIT = budget.amount if budget else 500.00
        
        # 2. Calculate monthly spending for this specific category
        now = datetime.now()
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == category,
            Transaction.transaction_type.in_(["withdrawal", "transfer"]),
            func.extract('month', Transaction.timestamp) == now.month,
            func.extract('year', Transaction.timestamp) == now.year
        ).scalar() or 0.0

        # 3. Check and generate warning
        if total_spent > BUDGET_LIMIT:
            message = f"Budget Warning: Spent ${total_spent:,.2f} on {category} (Limit: ${BUDGET_LIMIT})."
            
            # Prevent duplicate unread budget alerts for the same category
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.message.like(f"%{category}%"),
                Alert.is_read == False
            ).first()

            if not existing:
                new_alert = Alert(
                    user_id=user_id,
                    message=message,
                    is_read=False,
                    created_at=now
                )
                db.add(new_alert)
                db.commit()
                logger.info(f"Budget alert triggered for {category}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error in budget audit: {e}")

def check_upcoming_bills(db: Session, user_id: int, days_ahead: int = 3):
    """
    MILESTONE 4: Scheduled Automation.
    Identifies unpaid bills due in the near future.
    """
    try:
        upcoming_date = datetime.now() + timedelta(days=days_ahead)
        bills = db.query(Bill).filter(
            Bill.user_id == user_id,
            Bill.due_date <= upcoming_date,
            Bill.status == "unpaid"
        ).all()
        
        for bill in bills:
            # Check if alert already exists for this bill to avoid daily duplicates
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.message.like(f"%{bill.bill_name}%"),
                Alert.is_read == False
            ).first()

            if not existing:
                new_alert = Alert(
                    user_id=user_id,
                    message=f"Bill Reminder: '{bill.bill_name}' (${bill.amount}) is due on {bill.due_date.date()}.",
                    is_read=False,
                    created_at=datetime.now()
                )
                db.add(new_alert)
        
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error in bill reminder check: {e}")