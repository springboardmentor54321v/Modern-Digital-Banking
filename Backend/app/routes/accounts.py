from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.account import AccountCreate, AccountOut
from app.models.account import Account
from app.database import get_db

router = APIRouter()


# GET all accounts
@router.get("/", response_model=list[AccountOut])
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).all()
    return accounts


# POST create new account
@router.post("/", response_model=AccountOut)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    # create account object
    new_account = Account(
        user_id=account.user_id,
        bank_name=account.bank_name,
        account_type=account.account_type,
        masked_account=account.masked_account,
        currency=account.currency,
        balance=account.balance
    )
    
    db.add(new_account)
    db.commit()             # <-- commit to DB
    db.refresh(new_account) # <-- get auto-generated ID
    
    return new_account
