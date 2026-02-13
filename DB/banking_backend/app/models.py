from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20))
    kyc_status = Column(String(20), default="unverified")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    bank_name = Column(String(100))
    account_type = Column(String(50))
    masked_account = Column(String(50))
    currency = Column(String(3))
    balance = Column(Numeric(15,2), default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"))
    description = Column(String(255))
    amount = Column(Numeric(15,2))
    currency = Column(String(3))
    txn_type = Column(String(10))
    merchant = Column(String(100))
    txn_date = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
