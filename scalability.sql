SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM transactions;
SHOW synchronous_commit;
CREATE TABLE IF NOT EXISTS transactions_archive
(LIKE transactions INCLUDING ALL);
SELECT COUNT(*) FROM transactions_archive;
SELECT COUNT(*) FROM transactions;