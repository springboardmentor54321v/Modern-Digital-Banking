from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 1. DATABASE & ARCHITECTURE ---
from app.database import engine, Base

# IMPORTING MODELS: Explicitly importing ensures SQLAlchemy "sees" the 
# recipient_account_id and balance_after columns during table creation.
from app.models.user import User
from app.models.account import Account 
from app.models.transaction import Transaction
from app.models.alert import Alert

# --- 2. ROUTER IMPORTS ---
from app.api.routes.users import router as users_router 
from app.api.routes.auth import router as auth_router
from app.api.routes.accounts import router as accounts_router
from app.api.routes.transactions import router as transactions_router
from app.api.routes.insights import router as insights_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.automation import router as automation_router 
from app.api.routes.export import router as export_router 

# ---------------------------------------------------------
# Database Initialization
# ---------------------------------------------------------
# CRITICAL: This line creates tables only if they don't exist.
# After you "DROP TABLE transactions", this line will recreate it 
# with the correct Milestone 4 schema.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Modern Digital Banking Dashboard",
    description="Backend API for Milestone 4: Features Insights, Automation, and Reporting.",
    version="4.0.0",
    docs_url="/docs", 
)

# ---------------------------------------------------------
# CORS Configuration (Security)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# ROUTER REGISTRATION (Order 0-7)
# ---------------------------------------------------------

# 0. USER REGISTRATION: Create your user here first!
app.include_router(users_router, prefix="/users", tags=["0. User Registration"])

# 1. AUTHENTICATION: Secure Entry Point
app.include_router(auth_router, prefix="/auth", tags=["1. Authentication"])

# 2. ACCOUNT MANAGEMENT: Financial Foundation
app.include_router(accounts_router, prefix="/accounts", tags=["2. Account Management"])

# 3. TRANSACTIONS & AUTOMATOR: The Data Engine
app.include_router(transactions_router, prefix="/transactions", tags=["3. Transactions & Automator"])

# 4. INSIGHTS & ANALYTICS: Intelligence Layer
app.include_router(insights_router, prefix="/insights", tags=["4. Insights & Analytics"])

# 5. ALERT SYSTEM: Proactive Guardian
app.include_router(alerts_router, prefix="/alerts", tags=["5. Alert System"])

# 6. AUTOMATION ENGINE: Scheduled Jobs
app.include_router(automation_router, prefix="/automation", tags=["6. Automation Engine"])

# 7. DATA EXPORT: CSV & PDF Reporting
app.include_router(export_router, prefix="/export", tags=["7. Data Export"])

# ---------------------------------------------------------
# SYSTEM HEALTH & STARTUP LOGS
# ---------------------------------------------------------
@app.get("/", tags=["System"])
def health_check():
    """Returns the current status of the Milestone 4 backend."""
    return {
        "status": "online",
        "milestone": 4,
        "message": "Banking API is fully operational.",
        "version": "4.0.0"
    }

@app.on_event("startup")
def on_startup():
    """Terminal logs for the demo."""
    print("=========================================================")
    print("      MILESTONE 4: BANKING API IS NOW ACTIVE             ")
    print("=========================================================")
    print(" Local Server: http://127.0.0.1:8000")
    print(" Swagger UI Docs: http://127.0.0.1:8000/docs")
    print("=========================================================")