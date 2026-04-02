from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction
from app.models.budget import Budget
from datetime import datetime

class InsightsService:
    @staticmethod
    def get_category_spending(db: Session, user_id: int):
        """Aggregate expenses by category for the current month."""
        return db.query(
            Transaction.category,
            func.sum(Transaction.amount).label("total_amount")
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense"
        ).group_by(Transaction.category).all()

    @staticmethod
    def get_top_merchants(db: Session, user_id: int, limit: int = 5):
        """Identify top 5 merchants based on total spending."""
        return db.query(
            Transaction.merchant,
            func.sum(Transaction.amount).label("total_spent")
        ).filter(
            Transaction.user_id == user_id,
            Transaction.type == "expense"
        ).group_by(Transaction.merchant).order_by(func.sum(Transaction.amount).desc()).limit(limit).all()

    @staticmethod
    def calculate_burn_rate(db: Session, user_id: int):
        """Calculate percentage of total budget consumed."""
        total_budget = db.query(func.sum(Budget.limit)).filter(Budget.user_id == user_id).scalar() or 0
        total_spent = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id, 
            Transaction.type == "expense"
        ).scalar() or 0
        
        burn_percentage = (total_spent / total_budget * 100) if total_budget > 0 else 0
        
        return {
            "budget_limit": float(total_budget),
            "spent_so_far": float(total_spent),
            "burn_percentage": round(burn_percentage, 2),
            "status": "Over Budget" if burn_percentage > 100 else "Healthy"
        }

    @staticmethod
    def get_cash_flow(db: Session, user_id: int):
        """Compare total Income vs total Expenses."""
        income = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id, Transaction.type == "income"
        ).scalar() or 0
        
        expense = db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id, Transaction.type == "expense"
        ).scalar() or 0
        
        return {
            "month": datetime.now().strftime("%B"),
            "income": float(income),
            "expense": float(expense),
            "net_savings": float(income - expense)
        }