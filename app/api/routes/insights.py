from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.transaction import Transaction # Ensure these match your actual model paths
from app.models.user import User
# from app.models.budget import Budget # Uncomment if using Budget model
from app.api.deps import get_current_user

# --- THE FIX ---
# We leave APIRouter empty because main.py handles prefix="/insights" and tags=["4. Insights & Analytics"]
router = APIRouter()

# 1. Cash Flow: Income vs Expense
@router.get("/cashflow")
def get_cashflow(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Calculates the 'Pulse' of the account by comparing Total Credits (Income) 
    against Total Debits (Expenses).
    """
    results = db.query(
        Transaction.transaction_type,
        func.sum(Transaction.amount).label("total")
    ).filter(Transaction.user_id == current_user.id).group_by(Transaction.transaction_type).all()
    
    cashflow = {res.transaction_type: res.total for res in results}
    
    # Using 'credit' for income and 'debit' for expenses based on standard banking logic
    income = float(cashflow.get("credit", 0))
    expense = float(cashflow.get("debit", 0))
    
    return {
        "income": income,
        "expense": expense,
        "net_cash_flow": income - expense,
        "status": "Positive" if income > expense else "Deficit"
    }

# 2. Top Merchants (Merchant Intelligence)
@router.get("/top-merchants")
def get_top_merchants(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Identifies the top 5 merchants where the user spends the most money.
    """
    merchants = db.query(
        Transaction.description,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == current_user.id, 
        Transaction.transaction_type == "debit"
    ).group_by(Transaction.description).order_by(func.sum(Transaction.amount).desc()).limit(5).all()
    
    return [{"merchant": m.description, "amount": float(m.total)} for m in merchants]

# 3. Category-wise Spend (Spending DNA)
@router.get("/category-spend")
def get_category_spend(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Groups all expenses into categories (Food, Rent, etc.) for visual pie charts.
    """
    categories = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == current_user.id, 
        Transaction.transaction_type == "debit"
    ).group_by(Transaction.category).all()
    
    return {c.category: float(c.total) for c in categories}

# 4. Burn Rate (Budget Velocity)
@router.get("/burn-rate")
def get_burn_rate(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Measures how fast the user is spending their monthly budget.
    """
    total_spent = db.query(func.sum(Transaction.amount)) \
        .filter(Transaction.user_id == current_user.id, Transaction.transaction_type == "debit").scalar() or 0
    
    # Defaulting to 1 to avoid division by zero if no budget is set
    # replace 'Budget' with your actual budget limit logic if available
    total_budget = 5000 # Example hardcoded budget limit for Milestone 4
        
    burn_percentage = (float(total_spent) / total_budget) * 100
    
    return {
        "total_spent": float(total_spent),
        "budget_limit": total_budget,
        "burn_rate_percentage": round(burn_percentage, 2),
        "status": "Exceeded" if burn_percentage > 100 else "Safe"
    }