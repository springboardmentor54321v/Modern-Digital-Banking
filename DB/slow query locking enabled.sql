SHOW log_min_duration_statement;
SET log_min_duration_statement = 1000;
SHOW log_min_duration_statement;
SELECT pg_sleep(2);
SELECT 1;