import csv
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from datetime import datetime

class ExportService:
    @staticmethod
    def generate_transaction_csv(transactions):
        """
        Converts a list of Transaction models into a CSV string.
        Stored in memory using StringIO for fast performance.
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header - Professional banking columns
        writer.writerow(["ID", "Date", "Merchant", "Category", "Amount", "Type"])
        
        # Data Rows
        for tx in transactions:
            # Use getattr to safely handle potential missing attributes
            writer.writerow([
                tx.id,
                getattr(tx, 'date', 'N/A'),
                tx.merchant,
                tx.category,
                f"{tx.amount:.2f}", # Formats as currency 0.00
                getattr(tx, 'type', 'expense')
            ])
            
        return output.getvalue()

    @staticmethod
    def generate_summary_pdf(username, transactions, insights):
        """
        Generates a professional financial summary PDF report.
        Includes Burn Rate, Budget Status, and Recent Activity.
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # --- 1. Header Section ---
        p.setFont("Helvetica-Bold", 18)
        p.drawString(100, 750, "Modern Digital Banking")
        
        p.setFont("Helvetica", 10)
        p.drawRightString(500, 750, f"Report Date: {current_date}")
        
        p.setLineWidth(1)
        p.line(100, 740, 500, 740)
        
        # --- 2. User Info & Insights ---
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 710, f"Financial Summary for: {username}")
        
        p.setFont("Helvetica", 12)
        # Safely fetch from insights dictionary using .get()
        burn_rate = insights.get('burn_percentage', insights.get('burn_rate', 0))
        status = insights.get('status', 'Healthy')
        spent = insights.get('spent_so_far', 0)

        p.drawString(120, 680, f"• Burn Rate: {burn_rate}%")
        p.drawString(120, 660, f"• Budget Status: {status}")
        p.drawString(120, 640, f"• Total Spent: ${spent:,.2f}")
        p.drawString(120, 620, f"• Total Transactions: {len(transactions)}")
        
        # --- 3. Recent Activity (Table View) ---
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 580, "Recent Transactions Activity")
        
        p.setFont("Helvetica-Bold", 10)
        p.drawString(100, 560, "Date")
        p.drawString(180, 560, "Merchant")
        p.drawString(350, 560, "Category")
        p.drawString(450, 560, "Amount")
        p.line(100, 555, 500, 555)
        
        p.setFont("Helvetica", 10)
        y = 540
        # Show top 10 transactions to keep it on one page
        for tx in transactions[:10]:
            if y < 100: # Simple pagination check
                break
            p.drawString(100, y, str(getattr(tx, 'date', 'N/A')))
            p.drawString(180, y, str(tx.merchant)[:25]) # Truncate long names
            p.drawString(350, y, str(tx.category))
            p.drawString(450, y, f"${tx.amount:,.2f}")
            y -= 20
            
        # --- 4. Footer ---
        p.setFont("Helvetica-Oblique", 8)
        p.drawCentredString(300, 50, "This is an automated system-generated report.")
        
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer