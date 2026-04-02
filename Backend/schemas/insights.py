from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- 1. COMPONENT SCHEMAS ---

class CategorySpending(BaseModel):
    """Used for rendering Pie/Donut charts of spending by category."""
    category: str
    total_amount: float
    percentage: Optional[float] = None  # Added to help frontend calculations

    model_config = ConfigDict(from_attributes=True)

class CashFlowSummary(BaseModel):
    """High-level view of monthly financial health."""
    income: float
    expenses: float
    net_savings: float  # income - expenses

class BurnRateResponse(BaseModel):
    """Real-time budget tracking (e.g., 'Spent 80% of Food budget')."""
    category: str
    budget_limit: float
    spent_so_far: float
    burn_percentage: float
    status: str  # e.g., "Under Budget", "Warning", "Over Budget"

# --- 2. MAIN RESPONSE SCHEMAS ---

class MonthlyInsightResponse(BaseModel):
    """
    MILESTONE 4: The Primary Dashboard Schema.
    Combines spending breakdown with total monthly stats.
    """
    month: str
    year: int
    total_spent: float
    total_income: float
    net_savings: float
    breakdown: List[CategorySpending]
    
    model_config = ConfigDict(from_attributes=True)

class DetailedDashboardResponse(BaseModel):
    """
    Extensive schema for the full 'Insights' tab.
    Includes cashflow, category breakdown, and burn rates.
    """
    month_label: str
    cash_flow: CashFlowSummary
    categories: List[CategorySpending]
    budgets: List[BurnRateResponse]