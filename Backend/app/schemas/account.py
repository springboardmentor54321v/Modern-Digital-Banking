from pydantic import BaseModel
from datetime import datetime
from typing import Literal


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
