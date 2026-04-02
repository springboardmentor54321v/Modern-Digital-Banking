/*CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(id) ON DELETE CASCADE,
    description VARCHAR(255),
    category VARCHAR(100),
    amount NUMERIC(12,2),
    currency CHAR(3),
    txn_type txn_type_enum,
    merchant VARCHAR(100),
    txn_date TIMESTAMP,
    posted_date TIMESTAMP
);*/
CREATE INDEX IF NOT EXISTS idx_transactions_account_category_date
ON transactions(account_id, category, txn_date);
SELECT *
FROM transactions
WHERE account_id=101
AND category= 'food'
ORDER BY txn_date;






