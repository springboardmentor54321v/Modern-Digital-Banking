from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Local imports
from app.database import get_db
from app.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.services.alert_service import check_upcoming_bills

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    background_tasks: BackgroundTasks,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    MILESTONE 4: Secure Authentication & Login Automation.
    
    1. Authenticates user via Email OR Username.
    2. Issues a cryptographically signed JWT Access Token.
    3. Triggers proactive 'Intelligence' tasks (bill checks) in the background.
    """
    
    # --- 1. DEBUG LOGGING (Visible in your Terminal) ---
    print(f"--- Login Attempt ---")
    print(f"Credential: {form_data.username}")
    
    # --- 2. AUTHENTICATION LOGIC ---
    # authenticate_user (in app/auth.py) handles the Bcrypt password verification
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        print(f"RESULT: Authentication Failed for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"RESULT: Success! User {user.email} authenticated.")

    # --- 3. JWT TOKEN GENERATION ---
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )

    # --- 4. MILESTONE 4: PROACTIVE AUTOMATION ---
    # We trigger the bill check here so the 'Intelligence' engine is updated 
    # as soon as the user enters the app.
    background_tasks.add_task(check_upcoming_bills, db, user_id=user.id)

    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }