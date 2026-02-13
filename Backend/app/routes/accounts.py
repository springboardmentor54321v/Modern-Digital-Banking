from fastapi import APIRouter

account = APIRouter()
# ----------------------test--------------
@account.get("/accounts")
def account_check():
    return{"message":"Router Works"}