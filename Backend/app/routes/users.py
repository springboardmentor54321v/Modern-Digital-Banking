from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginUser
from app.services.auth_service import new_user,login

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return new_user(db, user)


# @router.get("/", response_model=list[UserResponse])
# def read_users(db: Session = Depends(get_db)):
#     return get_users(db)

@router.post("/login")
def login_user(user:LoginUser,db:Session = Depends(get_db)):
    return login(db,user)

