SELECT pg_sleep(2);
SELECT deadlocks
FROM pg_stat_database
WHERE datname = current_database();