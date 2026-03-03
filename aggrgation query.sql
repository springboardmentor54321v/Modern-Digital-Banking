EXPLAIN ANALYZE
SELECT category,
       SUM(amount) AS total_amount
FROM transactions
WHERE account_id = 1
AND txn_date BETWEEN '2025-01-01' AND '2025-01-31'
GROUP BY category;