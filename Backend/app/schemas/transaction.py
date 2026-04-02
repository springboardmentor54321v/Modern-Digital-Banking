from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# 1. ENUM FOR TYPE SAFETY
# This creates a dropdown in Swagger to prevent typos
class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"

# 2. BASE SCHEMA
# Contains fields shared by both Create and Response models
class TransactionBase(BaseModel):
    amount: float = Field(
        ..., 
        gt=0, 
        example=150.75, 
        description="The transaction amount must be greater than zero."
    )
    description: str = Field(
        ..., 
        example="Monthly Grocery Store", 
        description="A brief description of the transaction."
    )
    transaction_type: TransactionType = Field(
        ..., 
        example=TransactionType.WITHDRAWAL,
        description="Must be 'deposit', 'withdrawal', or 'transfer'."
    )
    account_id: int = Field(
        ..., 
        example=1, 
        description="The ID of the primary account involved."
    )
    category: str = Field(
        "General", 
        example="Food & Dining", 
        description="The budget category for the Insights API."
    )

# 3. CREATE SCHEMA (Request Body)
# Used in POST /transactions/
class TransactionCreate(TransactionBase):
    """
    Schema used when creating a new transaction.
    recipient_account_id is required ONLY for 'transfer' types.
    """
    recipient_account_id: Optional[int] = Field(
        None, 
        example=2, 
        description="The destination account ID (for transfers only)."
    )

# 4. RESPONSE SCHEMA (Response Body)
# Used to return data to the frontend after a successful operation
class TransactionResponse(TransactionBase):
    id: int = Field(..., example=101)
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="The exact time the transaction was recorded."
    )
    balance_after: float = Field(
        ..., 
        example=1250.50, 
        description="The account balance immediately following this transaction."
    )

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models