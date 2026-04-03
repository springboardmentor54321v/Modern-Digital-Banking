-- Seed test data for insights (March 2026)
-- Usage:
--   psql -U postgres -d banking_db -f Database/seed_test_data.sql

\set ON_ERROR_STOP on

DO $$
DECLARE
  v_user_id int;
  v_account_id int;
BEGIN
  SELECT id INTO v_user_id FROM users ORDER BY id ASC LIMIT 1;
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'No users found. Register a user first.';
  END IF;

  -- Ensure at least one account exists for the user (transactions require account_id)
  SELECT id INTO v_account_id FROM accounts WHERE user_id = v_user_id ORDER BY id ASC LIMIT 1;
  IF v_account_id IS NULL THEN
    INSERT INTO accounts (user_id, bank_name, account_type, masked_account, currency, balance, created_at)
    VALUES (v_user_id, 'Test Bank', 'Savings', '1234', 'INR', 50000, now())
    RETURNING id INTO v_account_id;
  END IF;

  -- Income (credit) transactions
  INSERT INTO transactions (user_id, account_id, amount, txn_type, txn_date, merchant, description, category, currency)
  VALUES
    (v_user_id, v_account_id, 85000.00, 'credit', '2026-03-05 10:00:00', 'Employer Inc', 'March Salary', 'Salary', 'INR'),
    (v_user_id, v_account_id, 15000.00, 'credit', '2026-03-12 14:30:00', 'Client A', 'Freelance Project', 'Investment', 'INR'),
    (v_user_id, v_account_id, 5000.00,  'credit', '2026-03-25 09:15:00', 'Employer Inc', 'Performance Bonus', 'Salary', 'INR');

  -- Expense (debit) transactions
  INSERT INTO transactions (user_id, account_id, amount, txn_type, txn_date, merchant, description, category, currency)
  VALUES
    (v_user_id, v_account_id, 499.00,  'debit', '2026-03-03 20:00:00', 'Netflix', 'Netflix subscription', 'Entertainment', 'INR'),
    (v_user_id, v_account_id, 2350.00, 'debit', '2026-03-08 11:45:00', 'Electricity Board', 'Electricity bill', 'Bills', 'INR'),
    (v_user_id, v_account_id, 1800.00, 'debit', '2026-03-10 19:20:00', 'Swiggy', 'Food order', 'Food', 'INR'),
    (v_user_id, v_account_id, 2200.00, 'debit', '2026-03-18 08:30:00', 'IndianOil', 'Petrol refill', 'Transport', 'INR'),
    (v_user_id, v_account_id, 7999.00, 'debit', '2026-03-22 16:10:00', 'Amazon', 'Shopping purchase', 'Shopping', 'INR');

  -- One budget record for March 2026
  INSERT INTO budgets (user_id, category, month, year, limit_amount, spent_amount, created_at)
  VALUES (v_user_id, 'Shopping', 3, 2026, 20000.00, 0.00, now())
  ON CONFLICT (user_id, category, month, year) DO NOTHING;
END $$;

