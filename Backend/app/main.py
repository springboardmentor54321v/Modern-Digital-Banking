from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app import models
from app.routes import users, accounts, transactions

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
# app.include_router(accounts.router)
# app.include_router(transactions.router)


@app.get("/")
def root():
    return {"status": "Banking backend running"}
