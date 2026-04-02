from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Transaction(Base):
    """
    MILESTONE 4: Standardized Transaction Model.
    Supports Atomic Balance Tracking and Inter-Account Transfers.
    FIXED: Resolved AmbiguousForeignKeysError by specifying foreign_keys.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- DATES ---
    # Standardized to match Dashboard JSON input (UTC enabled)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now()) 
    
    # --- FOREIGN KEYS ---
    # Links the transaction to the owner
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Primary Account (The account where the balance is primarily affected)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False, index=True)
    
    # Recipient Account (Used for Milestone 4 Transfer functionality)
    # Having two FKs to the same table is what requires the relationship 'fix' below.
    recipient_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    
    # --- FINANCIAL DATA ---
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    transaction_type = Column(String, default="withdrawal") # 'deposit', 'withdrawal', or 'transfer'
    category = Column(String, default="Uncategorized")
    
    # Snapshot of balance after transaction - Essential for audit trails
    balance_after = Column(Float, nullable=True)
    
    # --- METADATA ---
    # Critical for 'Top Merchants' spending analysis
    merchant_name = Column(String, index=True, nullable=True) 
    description = Column(String, nullable=True)

    # --- RELATIONSHIPS ---
    
    # FIX: We explicitly tell SQLAlchemy to use 'account_id' for this link.
    # This ignores 'recipient_account_id' when populating account.transactions.
    account = relationship(
        "Account", 
        back_populates="transactions", 
        foreign_keys=[account_id]
    )
    
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, balance_after={self.balance_after})>"