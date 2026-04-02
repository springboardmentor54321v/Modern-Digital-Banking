from pydantic import BaseModel
from typing import Optional
from datetime import date

class ExportRequest(BaseModel):
    format: str  # "csv" or "pdf"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    data_type: str # "transactions", "insights", or "summary"

    class Config:
        from_attributes = True