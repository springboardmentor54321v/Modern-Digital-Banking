-- Demo seed data for Milestone 2 + 3
-- Safe to re-run: uses WHERE NOT EXISTS / ON CONFLICT where possible.

BEGIN;

-- 1) Users (email is unique)
WITH u AS (
    INSERT INTO users (name, email, hashed_password, phone, kyc_status, role)
    VALUES
        ('Demo User', 'demo@example.com', 'demo-password', '9999999999', 'verified', 'user')
    ON CONFLICT (email) DO UPDATE SET
        name = EXCLUDED.name,
        role = EXCLUDED.role
    RETURNING id
)
SELECT id AS demo_user_id FROM u;

-- Helper: demo user id
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
-- 2) Accounts
INSERT INTO accounts (user_id, bank_name, account_type, masked_account, currency, balance)
SELECT d.user_id, 'HDFC Bank', 'Savings', '1234', 'INR', 25000.00
FROM demo_user d
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a
    WHERE a.user_id = d.user_id AND a.bank_name='HDFC Bank' AND a.account_type='Savings' AND a.masked_account='1234'
);

WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
INSERT INTO accounts (user_id, bank_name, account_type, masked_account, currency, balance)
SELECT d.user_id, 'ICICI Bank', 'Checking', '5678', 'INR', 8200.00
FROM demo_user d
WHERE NOT EXISTS (
    SELECT 1 FROM accounts a
    WHERE a.user_id = d.user_id AND a.bank_name='ICICI Bank' AND a.account_type='Checking' AND a.masked_account='5678'
);

-- 3) Category rules (unique per (user_id, keyword))
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
INSERT INTO category_rules (user_id, keyword, category, rule_type)
SELECT d.user_id, v.keyword, v.category, 'keyword'
FROM demo_user d
CROSS JOIN (VALUES
    ('starbucks', 'Food'),
    ('uber', 'Transport'),
    ('netflix', 'Entertainment')
) AS v(keyword, category)
ON CONFLICT (user_id, keyword) DO NOTHING;

-- 4) Budgets (unique per (user_id, category, month, year))
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
),
period AS (
    SELECT EXTRACT(MONTH FROM CURRENT_DATE)::int AS month,
           EXTRACT(YEAR FROM CURRENT_DATE)::int AS year
)
INSERT INTO budgets (user_id, category, month, year, limit_amount, spent_amount)
SELECT d.user_id, v.category, p.month, p.year, v.limit_amount, 0
FROM demo_user d
CROSS JOIN period p
CROSS JOIN (VALUES
    ('Food', 5000.00),
    ('Transport', 2500.00),
    ('Entertainment', 1500.00)
) AS v(category, limit_amount)
ON CONFLICT (user_id, category, month, year) DO NOTHING;

-- 5) Transactions (needs a valid account_id)
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
),
acc AS (
    SELECT a.id AS account_id, a.user_id
    FROM accounts a
    JOIN demo_user d ON d.user_id = a.user_id
    WHERE a.bank_name='HDFC Bank' AND a.masked_account='1234'
    LIMIT 1
)
INSERT INTO transactions (
    user_id, account_id, amount, txn_type, txn_date, posted_date,
    merchant, description, category, currency
)
SELECT
    a.user_id,
    a.account_id,
    v.amount,
    v.txn_type,
    v.txn_date,
    v.posted_date,
    v.merchant,
    v.description,
    v.category,
    'INR'
FROM acc a
CROSS JOIN (VALUES
    (299.00, 'debit',  NOW() - INTERVAL '3 days', NOW() - INTERVAL '3 days', 'Starbucks', 'Coffee purchase', 'Food'),
    (1200.00, 'debit', NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days', 'Uber', 'Ride to office', 'Transport'),
    (499.00, 'debit',  NOW() - INTERVAL '1 day',  NOW() - INTERVAL '1 day',  'Netflix', 'Monthly subscription', 'Entertainment'),
    (5000.00, 'credit', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days', 'Employer', 'Salary credit', 'Salary')
) AS v(amount, txn_type, txn_date, posted_date, merchant, description, category);

-- 6) Rewards
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
INSERT INTO rewards (user_id, program_name, points_balance, last_updated)
SELECT d.user_id, v.program_name, v.points_balance, CURRENT_DATE
FROM demo_user d
CROSS JOIN (VALUES
    ('HDFC Rewards', 1200),
    ('Amazon Pay', 450)
) AS v(program_name, points_balance)
WHERE NOT EXISTS (
    SELECT 1 FROM rewards r WHERE r.user_id=d.user_id AND r.program_name=v.program_name
);

-- 7) Bills
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
INSERT INTO bills (user_id, biller_name, amount_due, due_date, status, auto_pay)
SELECT d.user_id, v.biller_name, v.amount_due, v.due_date, v.status, v.auto_pay
FROM demo_user d
CROSS JOIN (VALUES
    ('Electricity', 1200.00, CURRENT_DATE + 1, 'upcoming', false),
    ('Internet', 799.00, CURRENT_DATE + 3, 'upcoming', true)
) AS v(biller_name, amount_due, due_date, status, auto_pay)
WHERE NOT EXISTS (
    SELECT 1 FROM bills b
    WHERE b.user_id=d.user_id AND b.biller_name=v.biller_name AND b.due_date=v.due_date
);

-- 8) Alerts (simple demo alert)
WITH demo_user AS (
    SELECT id AS user_id FROM users WHERE email = 'demo@example.com'
)
INSERT INTO alerts (user_id, type, message, is_read)
SELECT d.user_id, 'info', 'Welcome! Demo data loaded successfully.', false
FROM demo_user d
WHERE NOT EXISTS (
    SELECT 1 FROM alerts a WHERE a.user_id=d.user_id AND a.message='Welcome! Demo data loaded successfully.'
);

COMMIT;

