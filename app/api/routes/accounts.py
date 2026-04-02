from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountResponse
from app.models.user import User

# Centralized dependency to prevent circular imports
from app.api.deps import get_current_user
from app.services.currency import CurrencyService 

# Using redirect_slashes=False for demo flexibility
router = APIRouter(redirect_slashes=False)

# --- 1. LIST ALL ACCOUNTS ---
@router.get("", response_model=List[AccountResponse])
def get_my_accounts(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Fetches all accounts for the current authenticated user."""
    accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    # DEBUG PRINT: Check your terminal to see if accounts exist for this user
    print(f"DEBUG: User {current_user.email} (ID: {current_user.id}) has {len(accounts)} accounts.")
    return accounts

# --- 2. CREATE ACCOUNT ---
@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(
    account_in: AccountCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creates a new banking account linked to the authenticated user."""
    new_account = Account(
        **account_in.model_dump(), 
        user_id=current_user.id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    print(f"DEBUG: Created Account ID {new_account.id} for User {current_user.id}")
    return new_account

# --- 3. SPECIFIC ACCOUNT DETAIL ---
# Endpoint: GET /accounts/detail/{account_id}
@router.get("/detail/{account_id}", response_model=AccountResponse)
def get_account_detail(
    account_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves full details with ownership verification."""
    # We filter by both Account ID AND User ID to ensure the user owns the account
    account = db.query(Account).filter(
        Account.id == account_id, 
        Account.user_id == current_user.id
    ).first()

    if not account:
        # If this triggers, either the ID is wrong or the logged-in user doesn't own it
        print(f"DEBUG: 404 Error - User {current_user.id} tried to access Account {account_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Account ID {account_id} not found for this user."
        )
    return account

# --- 4. GLOBAL CURRENCY SUMMARY ---
@router.get("/summary/{target_currency}")
def get_total_currency_summary(
    target_currency: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Milestone 4 Intelligence Layer: Total balance conversion."""
    user_accounts = db.query(Account).filter(Account.user_id == current_user.id).all()
    total_balance = sum(acc.balance for acc in user_accounts)
    
    rates = CurrencyService.get_latest_rates()
    target = target_currency.upper()
    
    is_fallback = "error" in rates or target not in rates
    converted_balance = CurrencyService.convert(total_balance, target)
    
    if converted_balance is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Currency '{target}' is not supported."
        )
        
    return {
        "user_name": current_user.name,
        "total_balance_usd": round(total_balance, 2),
        "converted_balance": round(converted_balance, 2),
        "target_currency": target,
        "account_count": len(user_accounts),
        "metadata": {
            "source": "Fallback (Static)" if is_fallback else "Live (ExchangeRate-API)",
            "last_calculated": datetime.now(timezone.utc).isoformat()
        }
    }