from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal

# =========================
# Users Schemas
# =========================

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None  # optional during signup


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# Accounts Schemas
# =========================

class AccountCreate(BaseModel):
    user_id: int
    bank_name: str
    account_type: Literal["savings", "checking", "credit_card", "loan", "investment"]
    masked_account: str
    currency: str   
    balance: float


class AccountOut(BaseModel):
    id: int
    user_id: int
    bank_name: str
    account_type: str
    masked_account: str
    currency: str
    balance: float
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# Transactions Schemas
# =========================

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
