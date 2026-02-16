from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routes import users, accounts, transactions, auth





app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])


@app.get("/")
def root():
    return {"status": "Banking backend running"}
