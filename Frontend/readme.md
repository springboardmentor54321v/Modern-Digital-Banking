# Modern Digital Banking Dashboard - Frontend

## Project Overview
The Frontend is a React.js application with Tailwind CSS that provides a unified personal banking hub. It enables users to manage multiple accounts, track transactions, set budgets, monitor bills, earn rewards, and gain financial insights through an intuitive and responsive interface.

## Tech Stack
- **Framework**: React.js (v18+)
- **Styling**: Tailwind CSS
- **State Management**: Redux/Context API
- **HTTP Client**: Axios
- **Routing**: React Router
- **UI Components**: Custom + TailwindUI
- **Charts & Visualization**: Chart.js / Recharts
- **Forms**: React Hook Form / Formik
- **Authentication**: JWT (stored in localStorage/httpOnly cookies)

## Project Structure
```
Frontend/
├── public/
├── src/
│   ├── components/           # Reusable React components
│   │   ├── Auth/            # Login, signup, password reset
│   │   ├── Dashboard/       # Main dashboard layout
│   │   ├── Accounts/        # Account overview & CRUD
│   │   ├── Transactions/    # Transaction list, filters, details
│   │   ├── Budgets/         # Budget creation & progress
│   │   ├── Bills/           # Bill management & reminders
│   │   ├── Rewards/         # Rewards tracking & insights
│   │   ├── Insights/        # Analytics & charts
│   │   ├── Alerts/          # Alert center & notifications
│   │   ├── Common/          # Headers, footers, navigation
│   │   └── Admin/           # Admin dashboard (Module E)
│   ├── pages/               # Page-level components
│   ├── services/            # API calls & business logic
│   │   ├── authService.js
│   │   ├── accountService.js
│   │   ├── transactionService.js
│   │   ├── budgetService.js
│   │   ├── billService.js
│   │   ├── rewardService.js
│   │   ├── insightService.js
│   │   └── alertService.js
│   ├── store/               # Redux store & slices
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Helper functions
│   │   ├── api.js           # Axios instance with auth
│   │   ├── validators.js
│   │   ├── formatters.js    # Currency, date formatting
│   │   └── constants.js
│   ├── styles/              # Global CSS / Tailwind config
│   ├── App.jsx
│   └── index.jsx
├── .env.example             # Environment variables template
├── tailwind.config.js
├── package.json
└── README.md
```

## 8-Week Milestone Plan

### **Milestone 1: Weeks 1–2 – Foundations & Accounts**

#### Week 1: Auth & Base Setup
**Deliverables:**
- [ ] Login/Signup pages with JWT token management
- [ ] Protected routes & route guards
- [ ] User profile display
- [ ] Navigation sidebar/header
- [ ] Base styling with Tailwind

**Components to Build:**
- `LoginPage.jsx` – Email + password form
- `SignupPage.jsx` – User registration (name, email, password, phone)
- `DashboardLayout.jsx` – Main app layout with sidebar
- `Navigation.jsx` – Top navbar
- `ProtectedRoute.jsx` – Route guard component

**API Endpoints (Backend):**
- `POST /api/auth/login` – JWT token generation
- `POST /api/auth/signup` – User creation
- `POST /api/auth/refresh` – Refresh token
- `GET /api/users/me` – Current user profile

---

#### Week 2: Transaction Ingestion & List UI
**Deliverables:**
- [ ] Account list display with balances
- [ ] Transaction list with filters (date, amount, merchant)
- [ ] CSV import modal
- [ ] Transaction details view

**Components to Build:**
- `AccountsList.jsx` – Multi-account overview
- `AccountDetail.jsx` – Single account + transactions
- `TransactionList.jsx` – Paginated table
- `TransactionFilters.jsx` – Date, amount, merchant filters
- `TransactionDetail.jsx` – Modal/drawer with full details
- `CSVImportModal.jsx` – File upload & preview

**API Endpoints (Backend):**
- `GET /api/accounts` – List user accounts
- `GET /api/accounts/{id}` – Account details
- `GET /api/transactions` – List transactions (with filters)
- `GET /api/transactions/{id}` – Transaction details
- `POST /api/transactions/import` – CSV import

---

### **Milestone 2: Weeks 3–4 – Categorization & Budgets**

#### Week 3: Category Rules & Manual Recategorization
**Deliverables:**
- [ ] Category dropdown on transactions
- [ ] Categorize bulk transactions by merchant/keywords
- [ ] Manual recategorization UI

**Components to Build:**
- `TransactionCategorize.jsx` – Modal for manual categorization
- `CategoryRulesList.jsx` – View & manage category rules
- `CategoryRuleForm.jsx` – Create keyword/merchant rules

**API Endpoints (Backend):**
- `GET /api/categories` – List predefined categories
- `PUT /api/transactions/{id}/category` – Update category
- `POST /api/categories/rules` – Create categorization rule
- `PUT /api/categories/rules/{id}` – Update rule

---

#### Week 4: Monthly Budgets & Progress
**Deliverables:**
- [ ] Budget creation modal (category, monthly limit)
- [ ] Budget progress bars with % spent
- [ ] Budget charts & summaries
- [ ] Alerts when approaching limit

**Components to Build:**
- `BudgetList.jsx` – All budgets overview
- `BudgetCard.jsx` – Individual budget card with progress
- `BudgetCreateForm.jsx` – New budget modal
- `BudgetChart.jsx` – Spending breakdown (pie/bar chart)

**API Endpoints (Backend):**
- `POST /api/budgets` – Create budget
- `GET /api/budgets` – List budgets
- `PUT /api/budgets/{id}` – Update budget
- `DELETE /api/budgets/{id}` – Delete budget
- `GET /api/budgets/{id}/progress` – Budget vs. spent

---

### **Milestone 3: Weeks 5–6 – Bills & Rewards**

#### Week 5: Bills CRUD & Reminders
**Deliverables:**
- [ ] Bill management UI (create, edit, pay, delete)
- [ ] Bill reminders & status (upcoming, paid, overdue)
- [ ] Auto-pay toggle
- [ ] Email/SMS notification opt-in

**Components to Build:**
- `BillsList.jsx` – All bills overview
- `BillCard.jsx` – Individual bill status
- `BillCreateForm.jsx` – New bill modal
- `ReminderSettings.jsx` – Configure reminders (email/SMS)

**API Endpoints (Backend):**
- `POST /api/bills` – Create bill
- `GET /api/bills` – List bills
- `PUT /api/bills/{id}` – Update bill
- `PUT /api/bills/{id}/pay` – Mark as paid
- `DELETE /api/bills/{id}` – Delete bill
- `POST /api/bills/{id}/send-reminder` – Trigger reminder

---

#### Week 6: Rewards Tracking & Currency
**Deliverables:**
- [ ] Rewards programs display (points balance)
- [ ] Currency conversion summary
- [ ] ExchangeRate API integration
- [ ] Rewards redemption insights

**Components to Build:**
- `RewardsList.jsx` – All rewards programs
- `RewardCard.jsx` – Individual program details
- `CurrencyConverter.jsx` – Multi-currency view
- `RewardsInsights.jsx` – Earning trends

**API Endpoints (Backend):**
- `GET /api/rewards` – List rewards
- `PUT /api/rewards/{id}` – Update points balance
- `GET /api/currency/rates` – Exchange rates (ExchangeRate API)
- `GET /api/currency/summary` – Account summaries in base currency

---

### **Milestone 4: Weeks 7–8 – Insights & Alerts**

#### Week 7: Insights & Alerts Dashboard
**Deliverables:**
- [ ] Cash flow chart (income vs. expenses)
- [ ] Top merchants breakdown
- [ ] Burn rate trends
- [ ] Alert center with notifications
- [ ] Alert filtering & dismissal

**Components to Build:**
- `InsightsDashboard.jsx` – Main insights page
- `CashFlowChart.jsx` – Monthly income/expense
- `TopMerchantsChart.jsx` – Spending by merchant
- `BurnRateChart.jsx` – Trend analysis
- `AlertsCenter.jsx` – Alert feed
- `AlertNotification.jsx` – Toast/banner notifications

**API Endpoints (Backend):**
- `GET /api/insights/cash-flow` – Monthly summary
- `GET /api/insights/merchants` – Top merchants
- `GET /api/insights/burn-rate` – Spending trends
- `GET /api/alerts` – List alerts
- `PUT /api/alerts/{id}/dismiss` – Dismiss alert
- `DELETE /api/alerts/{id}` – Delete alert

---

#### Week 8: Exports, QA & Deployment
**Deliverables:**
- [ ] CSV export for transactions
- [ ] PDF export with statement
- [ ] Full QA testing
- [ ] Production build & optimization
- [ ] Error handling & loading states

**Components to Build:**
- `ExportModal.jsx` – CSV/PDF export options
- `LoadingSpinner.jsx` – Global loading states
- `ErrorBoundary.jsx` – Error handling

**API Endpoints (Backend):**
- `POST /api/export/csv` – Generate CSV
- `POST /api/export/pdf` – Generate PDF statement

---

## Setup Instructions

### Prerequisites
- Node.js v16+
- npm or yarn
- Backend API running on `http://localhost:8000`

### Installation
```bash
# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Update .env with backend URL
VITE_API_BASE_URL=http://localhost:8000
VITE_JWT_TOKEN_KEY=access_token
```

### Development
```bash
# Start dev server
npm run dev

# Build for production
npm run build

# Run tests
npm run test
```

## Key Features Implementation

### Authentication Flow
1. User logs in → JWT token stored
2. Axios interceptor adds token to headers
3. Token refresh on expiry
4. Logout clears token

### API Integration Pattern
```javascript
// Example: transactionService.js
import api from '@/utils/api';

export const getTransactions = (filters = {}) => 
  api.get('/transactions', { params: filters });

export const importCSV = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/transactions/import', formData);
};
```

### State Management
- Redux for global app state (user, auth)
- Context API for feature-level state (budgets, bills)
- React Query for server state (if using)

## Environment Variables
```
VITE_API_BASE_URL=http://localhost:8000
VITE_JWT_TOKEN_KEY=access_token
VITE_APP_NAME=Modern Digital Banking
VITE_CURRENCY_API_KEY=<your_exchangerate_api_key>
```

## Testing Strategy
- Unit tests: Jest + React Testing Library
- E2E tests: Cypress / Playwright
- Coverage target: 80%+

## Performance Optimization
- Code splitting by route
- Image optimization
- Lazy loading for charts/heavy components
- Memoization of expensive computations

## Accessibility
- WCAG 2.1 AA compliance
- Semantic HTML
- ARIA labels for forms & dynamic content
- Keyboard navigation support

## Deployment
- Build: `npm run build`
- Deploy to Vercel / Netlify / AWS S3 + CloudFront
- Environment-specific configs

---

## Progress Tracker

| Feature | Week | Status |
|---------|------|--------|
| Auth & Login | 1 | ⬜ Not Started |
| Dashboard Layout | 1 | ⬜ Not Started |
| Accounts List | 2 | ⬜ Not Started |
| Transaction List & Filters | 2 | ⬜ Not Started |
| CSV Import | 2 | ⬜ Not Started |
| Category Rules | 3 | ⬜ Not Started |
| Manual Categorization | 3 | ⬜ Not Started |
| Budget CRUD | 4 | ⬜ Not Started |
| Budget Progress Charts | 4 | ⬜ Not Started |
| Bill Management | 5 | ⬜ Not Started |
| Reminders (Email/SMS) | 5 | ⬜ Not Started |
| Rewards Tracking | 6 | ⬜ Not Started |
| Currency Conversion | 6 | ⬜ Not Started |
| Insights Dashboard | 7 | ⬜ Not Started |
| Alerts Center | 7 | ⬜ Not Started |
| CSV/PDF Export | 8 | ⬜ Not Started |
| QA & Deployment | 8 | ⬜ Not Started |

## Common Issues & Solutions

### JWT Token Issues
- Clear localStorage and re-login
- Check token expiry with `jwt.io`
- Verify backend refresh endpoint

### CORS Errors
- Ensure backend allows frontend origin
- Check API headers in network tab

### Build Errors
- Clear `node_modules` and reinstall
- Check Node version compatibility

## Contributing Guidelines
- Follow naming conventions (camelCase for files, PascalCase for components)
- Create branches for features: `feature/module-name`
- Write commit messages in imperative mood
- Test before pushing

## Resources
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Redux Toolkit](https://redux-toolkit.js.org)
- [React Router](https://reactrouter.com)
