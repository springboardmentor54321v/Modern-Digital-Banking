from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

router = APIRouter()

@router.get("/")
def get_transactions():
    return {"message": "Transactions working"}


@router.post("/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):

    # txn_type use karo
    if transaction.txn_type == "credit":
        print("Money added")

    elif transaction.txn_type == "debit":
        print("Money deducted")

    new_txn = Transaction(
        account_id = transaction.account_id,
        description = transaction.description,
        category = transaction.category,
        amount = transaction.amount,
        currency = transaction.currency,
        txn_type = transaction.txn_type,
        merchant = transaction.merchant,
        txn_date = transaction.txn_date,
        posted_date = transaction.posted_date
    )

    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)

    return {"message": "Transaction created", "id": new_txn.id}