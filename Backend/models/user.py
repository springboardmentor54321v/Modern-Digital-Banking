from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class User(Base):
    """
    MILESTONE 4: Central User Hub.
    Links Authentication, Banking, and the Intelligence Engine.
    """
    __tablename__ = "users"
    
    # --- 1. Primary Key ---
    id = Column(Integer, primary_key=True, index=True)
    
    # --- 2. Auth & Profile ---
    # username is now mandatory for registration consistency
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # --- 3. Banking Specifics ---
    # Defaulting to "Pending" as per our KYC verification logic
    kyc_status = Column(String, default="Pending")
    
    # Using server_default=func.now() is better for database-level timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # --- 4. Relationships (The Intelligence & Banking Engine) ---
    # These 'back_populates' must match the attribute names in child models.
    
    # Linked to app/models/account.py
    accounts = relationship("Account", back_populates="owner", cascade="all, delete-orphan")
    
    # Linked to app/models/bill.py
    bills = relationship("Bill", back_populates="owner", cascade="all, delete-orphan")
    
    # Linked to app/models/reward.py
    rewards = relationship("Reward", back_populates="owner", cascade="all, delete-orphan")
    
    # Linked to app/models/transaction.py
    transactions = relationship(
        "Transaction", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    # Linked to app/models/category_rule.py (Fixes the 'rules' KeyError)
    rules = relationship(
        "CategoryRule", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )
    
    # Linked to app/models/budget.py
    budgets = relationship(
        "Budget", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )

    # Linked to app/models/alert.py
    alerts = relationship(
        "Alert", 
        back_populates="user", 
        cascade="all, delete-orphan"
    )