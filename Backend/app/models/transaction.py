from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    account_id = Column(Integer, ForeignKey("accounts.id"))

    description = Column(String)
    category = Column(String, nullable=True)

    amount = Column(Float)
    currency = Column(String)

    txn_type = Column(String)
    merchant = Column(String, nullable=True)

    txn_date = Column(DateTime)
    posted_date = Column(DateTime, nullable=True)  

    is_categorized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
