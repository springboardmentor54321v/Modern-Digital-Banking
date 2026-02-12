from fastapi import FastAPI
from routes.accounts import account
app = FastAPI()
app.include_router(account)
# -----test------
@app.get("/test")
def test():
    return{"message":"fast Api"}