from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate
from app.services.auth_service import new_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return new_user(db, user)


# @router.get("/", response_model=list[UserResponse])
# def read_users(db: Session = Depends(get_db)):
#     return get_users(db)
