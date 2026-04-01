EXPLAIN ANALYZE
SELECT 
    category,
    SUM(amount) AS total_spent
FROM transactions
GROUP BY category;
EXPLAIN ANALYZE
SELECT 
    DATE_TRUNC('month', txn_date) AS month,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY month;
EXPLAIN ANALYZE
SELECT 
    merchant,
    SUM(amount) AS total_spent
FROM transactions
WHERE merchant IS NOT NULL
GROUP BY merchant
ORDER BY total_spent DESC
LIMIT 5;