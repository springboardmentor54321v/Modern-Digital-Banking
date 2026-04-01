SELECT 
    merchant,
    SUM(amount) AS total_spent
FROM transactions
GROUP BY merchant
ORDER BY total_spent DESC
LIMIT 5;