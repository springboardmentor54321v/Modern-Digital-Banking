from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional

# 1. Base Class: Shared attributes with rich Swagger documentation
class AccountBase(BaseModel):
    account_name: str = Field(..., min_length=1, example="Primary Savings", description="User-defined name for the account")
    account_type: str = Field(..., example="Savings", description="Type of account (e.g., Checking, Savings, Credit)")
    balance: float = Field(default=0.0, example=1250.50)
    currency: str = Field(default="USD", min_length=3, max_length=3, example="USD", description="3-letter currency code")
    bank_name: str = Field(..., example="Global Digital Bank")
    masked_account: Optional[str] = Field(None, example="****6789", description="Security-masked account number")

    # Milestone 4 validation: Ensure currency is always uppercase for the conversion service
    @field_validator('currency')
    @classmethod
    def currency_must_be_uppercase(cls, v: str) -> str:
        return v.upper()

# 2. Create Class: Used for POST /accounts
class AccountCreate(AccountBase):
    """Schema for creating a new account. Inherits all fields from AccountBase."""
    pass

# 3. Response Class: What the API sends back (SQLAlchemy compatible)
class AccountResponse(AccountBase):
    """Schema for returning account data, including database IDs."""
    id: int
    user_id: int

    # Pydantic V2 configuration to allow reading from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

# 4. Intelligence Layer: Summary dashboard logic
class AccountSummary(BaseModel):
    """Schema for the Milestone 4 Intelligence Layer summary dashboard."""
    total_balance: float = Field(..., example=5400.25)
    currency: str = Field(..., example="USD")
    account_count: int = Field(..., example=3)
    user_name: Optional[str] = Field(None, example="Kavya Dev")

    model_config = ConfigDict(from_attributes=True)