from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP
from app.database import Base
from datetime import datetime

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
