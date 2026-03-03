DROP INDEX idx_transactions_acc_cat_date;
CREATE INDEX idx_transactions_acc_cat_date
ON transactions(account_id, category, txn_date);