from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginUser
from app.services.auth_service import new_user,login
from app.cors.security import verify_token,refreh


router = APIRouter(tags=["Users"])


@router.post("/register")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    return new_user(db, user)


# @router.get("/", response_model=list[UserResponse])
# def read_users(db: Session = Depends(get_db)):
#     return get_users(db)

@router.post("/login")
def login_user(user:LoginUser,db:Session = Depends(get_db)):
    refresh,access = login(db,user)
    return {
    "access_token": access,
    "refresh_token": refresh,
    "token_type": "bearer"
}

@router.get("/profile")
def profile(user_id:int = Depends(verify_token)):

    return {"user_id":user_id}
@router.post("/refresh")
def refresh(user_id:int = Depends(refreh)):

    return{"user_id":user_id}
    


