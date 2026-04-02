from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Bill(Base):
    """
    MILESTONE 4: Bill Management Model.
    Tracks recurring payments and connects to the User's financial profile.
    """
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    
    # 1. Foreign Key: Links this bill to a specific user
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 2. Bill Data
    biller_name = Column(String, nullable=False)      # e.g., "Electricity Board"
    amount_due = Column(Float, nullable=False)        # e.g., 120.50
    due_date = Column(Date, nullable=False)           # Tracks when payment is required
    
    # 3. Status Logic: 'upcoming', 'paid', or 'overdue'
    status = Column(String, default="upcoming") 
    
    # 4. Feature: Boolean to check if auto-payment is enabled
    auto_pay = Column(Boolean, default=False)

    # --- Intelligence Engine Relationships ---
    
    # FIX: This line connects back to the User model's 'bills' attribute
    owner = relationship("User", back_populates="bills")