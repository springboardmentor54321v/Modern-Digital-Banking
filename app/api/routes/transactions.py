from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.api.deps import get_current_user 
from app.services.alert_service import check_low_balance, check_budget_exceeded

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    MILESTONE 4: Atomic Transaction Processing & Proactive Guarding.
    This endpoint synchronizes the ledger and triggers automated financial audits.
    """
    
    # 1. OWNERSHIP & EXISTENCE CHECK
    # Validates that the account exists and belongs to the authenticated user.
    account = db.query(Account).filter(
        Account.id == transaction_in.account_id, 
        Account.user_id == current_user.id
    ).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Account not found or unauthorized access."
        )

    # 2. BALANCE CALCULATION LOGIC
    tx_type = str(transaction_in.transaction_type).lower()
    
    if "withdrawal" in tx_type or "transfer" in tx_type:
        if account.balance < transaction_in.amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Insufficient funds: Transaction aborted."
            )
        account.balance -= transaction_in.amount
    elif "deposit" in tx_type:
        account.balance += transaction_in.amount

    # 3. ATOMIC PERSISTENCE LAYER
    try:
        # Create the transaction record
        new_transaction = Transaction(
            user_id=current_user.id,
            account_id=transaction_in.account_id,
            amount=transaction_in.amount,
            transaction_type=transaction_in.transaction_type,
            category=transaction_in.category,
            description=transaction_in.description,
            recipient_account_id=transaction_in.recipient_account_id,
            balance_after=account.balance
        )
        
        db.add(new_transaction)
        db.add(account) # Update balance
        
        db.commit()
        db.refresh(new_transaction)

        # 4. MILESTONE 4: PROACTIVE AUTOMATION (Background Tasks)
        # Ensure these arguments match your service function signatures exactly.
        
        # Check if the specific account has dropped below a safety threshold
        background_tasks.add_task(
            check_low_balance, 
            db, 
            current_user.id, 
            transaction_in.account_id
        )

        # Check if this specific spending category has exceeded the monthly budget
        # FIXED: Passing db, user_id, amount, AND category to satisfy the service requirements
        background_tasks.add_task(
            check_budget_exceeded, 
            db, 
            current_user.id, 
            transaction_in.amount, 
            transaction_in.category
        )

        print(f"DEBUG: Processed TX {new_transaction.id}. New Balance: {account.balance}")
        return new_transaction
        
    except Exception as e:
        db.rollback()
        print(f"CRITICAL ERROR: {str(e)}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Database synchronization error: Transaction rolled back."
        )