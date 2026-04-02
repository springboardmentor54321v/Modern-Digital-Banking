CREATE INDEX IF NOT EXISTS idx_transactions_account_id 
ON transactions(account_id);

CREATE INDEX IF NOT EXISTS idx_transactions_txn_date 
ON transactions(txn_date);

CREATE INDEX IF NOT EXISTS idx_transactions_txn_type 
ON transactions(txn_type);