from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- 1. USER IDENTITY SCHEMAS ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    username: str  # Matches your SQLAlchemy Model
    password: str
    phone: Optional[str] = None

# We use "UserResponse" to match the import in your routes/users.py
class UserResponse(BaseModel):
    id: int
    name: str
    username: str 
    email: EmailStr
    kyc_status: Optional[str] = "pending"
    created_at: datetime

    class Config:
        from_attributes = True

# --- 2. AUTHENTICATION SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- 3. INTELLIGENCE ENGINE SCHEMAS ---

class CategoryRuleCreate(BaseModel):
    keyword_pattern: str 
    category: str
    match_type: Optional[str] = "partial"

    class Config:
        from_attributes = True

class CategoryRuleOut(BaseModel):
    id: int
    keyword_pattern: str
    category: str
    match_type: str

    class Config:
        from_attributes = True