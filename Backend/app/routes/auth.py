from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/signup")
def signup(name: str, email: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        name=name,
        email=email,
        password_hash=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}


@router.post("/refresh")
def refresh():
    return {"message": "Token refreshed"}
