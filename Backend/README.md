# 🏦 Modern Digital Banking Dashboard (Full Stack API)

![Version](https://img.shields.io/badge/version-4.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688)

## 📌 Milestone 4: Logic, Serving, and Automation Layer
This milestone transforms the application from a data-entry tool into a smart banking engine. It introduces automated financial monitoring and cross-currency analytics.

---

## 🛠️ System Architecture
The system follows a modular architecture to ensure scalability:
* **API Layer:** FastAPI routers for modularized endpoints.
* **Logic Layer:** Services for Currency Conversion and Spending Analytics.
* **Data Layer:** SQLAlchemy ORM with SQLite for persistent storage.
* **Automation Layer:** APScheduler running background health checks.

---

## 📂 Key Features (Milestone 4)

### 💰 Multi-Currency Account Management
* **Real-time Conversion:** Endpoints to view balances in `USD`, `EUR`, `GBP`, and `JPY`.
* **Logic Service:** A centralized `CurrencyService` handles all mathematical conversions.

### 📊 Automated Spending Insights
* **Category Analysis:** Automatically groups transactions into categories (Food, Rent, Entertainment).
* **Budget Tracking:** Real-time calculation of "Remaining Budget" based on monthly limits.

### 🔔 Proactive Alert System
* **Background Monitoring:** A startup scheduler runs every 24 hours (or on demand) to check:
    * **Low Balance Alerts:** Triggered if account balance falls below $100.
    * **Budget Overruns:** Notifies the user if they spend more than their set limit.
    * **Upcoming Bills:** Identifies bills due within the next 3 days.

---

## 🚀 Installation & Running

1. **Activate Virtual Environment:**
   ```bash
   .\venv\Scripts\activate