CREATE INDEX  IF NOT EXISTS idx_bills_user_id
ON bills(user_id);

CREATE INDEX IF NOT EXISTS idx_bills_due_date
ON bills(due_date);

CREATE INDEX IF NOT EXISTS  idx_bills_status
ON bills(status);