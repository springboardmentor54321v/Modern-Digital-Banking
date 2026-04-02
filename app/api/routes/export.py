import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

# 1. GET /export/transactions?format=csv
@router.get("/transactions")
def export_transactions(
    format: str = "csv", 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Exports all user transactions as a CSV file."""
    if format.lower() != "csv":
        raise HTTPException(status_code=400, detail="Only CSV format is supported for this endpoint")

    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()

    # Create an in-memory string buffer
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header Row
    writer.writerow(["ID", "Date", "Description", "Category", "Amount", "Type"])
    
    # Data Rows
    for tx in transactions:
        writer.writerow([tx.id, tx.created_at, tx.description, tx.category, tx.amount, tx.transaction_type])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"}
    )

# 2. GET /export/insights?format=pdf
@router.get("/insights")
def export_insights_pdf(
    format: str = "pdf", 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """Generates a simple PDF summary of the user's Financial Insights."""
    if format.lower() != "pdf":
        raise HTTPException(status_code=400, detail="Only PDF format is supported for this endpoint")

    # Fetch simple summary data
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    total_spent = sum(t.amount for t in transactions if t.transaction_type == "debit")
    total_income = sum(t.amount for t in transactions if t.transaction_type == "credit")

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # PDF Content (Basic Layout)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, f"Financial Insights Report: {current_user.email}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 720, f"Total Income: ${total_income:,.2f}")
    p.drawString(100, 700, f"Total Expenses: ${total_spent:,.2f}")
    p.drawString(100, 680, f"Net Cash Flow: ${(total_income - total_spent):,.2f}")
    
    p.line(100, 660, 500, 660)
    p.drawString(100, 640, "Status: Generated via Milestone 5 Export Engine")

    p.showPage()
    p.save()

    buffer.seek(0)
    return Response(
        content=buffer.getvalue(),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=insights_summary.pdf"}
    )