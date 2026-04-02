from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):
    """
    MILESTONE 4: Account Model with Intelligence Tracking.
    Stores financial balances and links to user-specific intelligence (Alerts & Transactions).
    """
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 1. Foreign Key: Links this account to a specific user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 2. Account Details
    account_name = Column(String, nullable=False)      # e.g., "Chase Premier"
    bank_name = Column(String, nullable=False)         # e.g., "Chase"
    account_type = Column(String)                      # e.g., "Savings", "Checking"
    masked_account = Column(String)                    # e.g., "****6789"
    
    # 3. Financial Data
    currency = Column(String(3), default="USD")
    balance = Column(Float, default=0.00) 
    
    # 4. Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Intelligence Engine Relationships ---
    
    # Links back to the User model
    owner = relationship("User", back_populates="accounts")

    # FIX: Explicitly specify foreign_keys to resolve AmbiguousForeignKeysError.
    # This tells SQLAlchemy that 'account.transactions' refers specifically to 
    # records where this account is the primary 'account_id'.
    transactions = relationship(
        "Transaction", 
        back_populates="account", 
        foreign_keys="[Transaction.account_id]",
        cascade="all, delete-orphan"
    )

    # Links back to the Alert model for Milestone 4 proactive notifications
    alerts = relationship(
        "Alert", 
        back_populates="account", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Account(id={self.id}, name='{self.account_name}', balance={self.balance})>"