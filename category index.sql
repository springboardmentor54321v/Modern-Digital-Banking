DROP INDEX idx_transactions_category;
CREATE INDEX  idx_transactions_category
ON transactions(category);