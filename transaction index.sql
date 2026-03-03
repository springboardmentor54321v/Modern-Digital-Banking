DROP INDEX idx_transactions_txn_date;
CREATE INDEX idx_transactions_txn_date
ON transactions(txn_date);