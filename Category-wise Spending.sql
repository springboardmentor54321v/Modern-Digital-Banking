SELECT 
    category,
    SUM(amount) AS total_spent
FROM transactions
GROUP BY category
ORDER BY total_spent DESC;