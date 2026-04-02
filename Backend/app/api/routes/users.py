from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# --- 1. LOCAL IMPORTS ---
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse 
from app.auth import get_password_hash  # Imports centralized hashing logic

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    MILESTONE 4: Secure User Onboarding.
    1. Validates unique identity (Email & Username).
    2. Hashes password using Bcrypt.
    3. Persists user record to PostgreSQL.
    """
    
    # --- 2. IDENTITY VALIDATION ---
    # Ensure the email is not already in use
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already registered"
        )
    
    # Ensure the username is unique
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already taken"
        )

    # --- 3. PASSWORD HASHING & MODEL MAPPING ---
    # We map the UserCreate schema directly to the SQLAlchemy User model
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        username=user_in.username,
        # The password is hashed before it ever hits the database
        hashed_password=get_password_hash(user_in.password),
        phone=user_in.phone
    )

    # --- 4. DATABASE PERSISTENCE ---
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the account."
        )

    return new_user