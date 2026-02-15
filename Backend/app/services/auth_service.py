from sqlalchemy.orm import Session 
from fastapi import HTTPException
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import LoginUser
from argon2 import PasswordHasher 
from app.cors.security import create_token,create_refresh_token


# -----globally declared ---------
haser = PasswordHasher() 

def new_user(db:Session,user:UserCreate):
    hassed_password = haser.hash(user.password)
    newUser = User(
        name = user.name,
        email = user.email,
        password = hassed_password,
        phone = user.phone,
       
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser
def login(db:Session,loginuser:LoginUser):


    # ------------To get the particular thing from the Db-------

    passstmt = select(User.id,User.password).where(User.email == loginuser.email)
    result = db.execute(passstmt).one_or_none()
    if result is None:
        raise HTTPException(status_code=401,detail="User Not Found")
    
    user_id,hassed_password = result

    if not haser.verify(hassed_password,loginuser.password):
        raise HTTPException(status_code=401,detail="Incorrect Password")    
    token = create_token({
        "user_id":user_id
    })

    refresh_token = create_refresh_token({"user_id":user_id})
    
    return  refresh_token,token



        
        



