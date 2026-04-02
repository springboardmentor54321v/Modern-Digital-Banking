from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

# Use HTTPBearer so Swagger only asks for a "Token" value
security = HTTPBearer()

def get_current_user(
    db: Session = Depends(get_db), 
    auth: HTTPAuthorizationCredentials = Depends(security)
):
    """
    MILESTONE 4: Simplified Dependency for Presentation.
    1. Clicking 'Authorize' in Swagger now only asks for a token 'Value'.
    2. Logic: It verifies a token is present, then returns the first DB user 
       to ensure Account 10 (which belongs to user_id 1) is accessible.
    """
    
    # In a real app, we would decode the JWT here. 
    # For the demo, we fetch User #1 to match your 'Main Savings' account.
    user = db.query(User).filter(User.id == 1).first()
    
    if not user:
        # Fallback: just get the first available user
        user = db.query(User).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Demo Error: No users found. Please register a user first."
        )
        
    return user