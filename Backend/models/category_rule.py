from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class CategoryRule(Base):
    """
    MILESTONE 4: Intelligence Engine - Category Rules.
    Automatically maps transaction descriptions to categories based on user patterns.
    """
    __tablename__ = "category_rules"

    # --- Safety & Constraints ---
    __table_args__ = (
        # 1. Prevents duplicate rules for the same keyword per user
        UniqueConstraint('user_id', 'keyword', name='_user_keyword_uc'),
        # 2. Fixes potential registry errors during FastAPI hot-reloads
        {'extend_existing': True},
    )

    # --- Columns ---
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Intelligence Logic: 'Amazon' -> 'Shopping'
    keyword = Column(String, nullable=False) 
    category = Column(String, nullable=False)
    
    # match_type allows for 'exact' or 'contains' logic
    match_type = Column(String, default="keyword")

    # --- Relationships ---
    
    # This MUST match the back_populates="rules" in User model
    user = relationship("User", back_populates="rules")