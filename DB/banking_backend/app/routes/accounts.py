from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/")
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    new_account = models.Account(**account.dict())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/user/{user_id}")
def list_user_accounts(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()
