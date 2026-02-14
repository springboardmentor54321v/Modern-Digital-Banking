from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal


class TransactionCreate(BaseModel):
    account_id: int
    description: str
    category: Optional[str] = None
    amount: float
    currency: str
    txn_type: Literal["debit", "credit"]
    merchant: Optional[str] = None
    txn_date: datetime
    posted_date: Optional[datetime] = None


class TransactionOut(BaseModel):
    id: int
    account_id: int
    description: str
    category: Optional[str] = None
    amount: float
    currency: str
    txn_type: str
    merchant: Optional[str] = None
    txn_date: datetime
    posted_date: Optional[datetime] = None
    is_categorized: bool
    created_at: datetime

    class Config:
        from_attributes = True
