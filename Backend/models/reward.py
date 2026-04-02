from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class Reward(Base):
    """
    MILESTONE 4: Rewards & Loyalty Model.
    Handles both the Reward Catalog items and User Point tracking.
    """
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True, index=True)
    
    # Link to the User (Required for Milestone 4 tracking)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Catalog Details (The fields causing your recent error)
    name = Column(String, nullable=False)           # e.g., "Amazon Gift Card"
    description = Column(String, nullable=True)     # e.g., "$10 Digital Code"
    points_cost = Column(Integer, default=0)        # Cost to redeem
    
    # Tracking Details (From your previous logic)
    points_balance = Column(Integer, default=0)     # Current points available
    is_active = Column(Boolean, default=True)
    last_updated = Column(Date, default=date.today)

    # Relationship to User model
    owner = relationship("User", back_populates="rewards")