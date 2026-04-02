from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AlertBase(BaseModel):
    message: str = Field(..., example="Low balance alert: Your balance is below $100")
    is_read: bool = Field(default=False)

class AlertCreate(AlertBase):
    user_id: int

class MarkReadRequest(BaseModel):
    alert_id: int = Field(..., example=1)

class AlertResponse(AlertBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AlertCountResponse(BaseModel):
    unread_count: int