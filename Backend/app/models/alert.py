from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Alert(Base):
    """
    MILESTONE 4: Intelligence & Alerting Model.
    Stores automated notifications for low balances, budget caps, and system messages.
    """
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- FOREIGN KEYS ---
    # Links alert to the owner (Critical for GET /alerts/me)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Links alert to the specific bank account (Critical for "Low Balance" context)
    # nullable=True allows for general system alerts not tied to a specific account
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    
    # --- DATA FIELDS ---
    # Stores type: 'low_balance', 'transaction_success', 'security_warning'
    type = Column(String, nullable=False, default="general")
    
    message = Column(String, nullable=False)
    
    # default=False ensures new alerts are always unread
    is_read = Column(Boolean, default=False, nullable=False)
    
    # Automated timestamp for 'newest first' sorting (transaction_date style)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- RELATIONSHIPS ---
    # Note: Ensure your User and Account models have the corresponding 'alerts' 
    # relationship with back_populates="user" and back_populates="account".
    user = relationship("User", back_populates="alerts")
    account = relationship("Account", back_populates="alerts")

    def __repr__(self):
        return f"<Alert(id={self.id}, user_id={self.user_id}, type='{self.type}', is_read={self.is_read})>"