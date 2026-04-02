/*CREATE TABLE IF NOT EXISTS budgets (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    month INT CHECK (month BETWEEN 1 AND 12),
    year INT,
    category VARCHAR(100),
    limit_amount NUMERIC(12,2),
    spent_amount NUMERIC(12,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT*FROM budgets;
ALTER TABLE budgets
ADD CONSTRAINT unique_budget
UNIQUE  IF NOT EXISTS (user_id, category, month, year);
CREATE INDEX IF NOT EXISTS idx_budgets_user_month_year_category
ON budgets(user_id, month, year, category);
EXPLAIN ANALYZE
SELECT SUM(amount)
FROM transactions
WHERE account_id = 1
AND category = 'Food'
AND txn_type = 'debit';
EXPLAIN ANALYZE
SELECT 
FROM budgets
WHERE user_id = 1
AND month = 2
AND year = 2026;8*/

SELECT conname
FROM pg_constraint
WHERE conrelid = 'budgets'::regclass;



