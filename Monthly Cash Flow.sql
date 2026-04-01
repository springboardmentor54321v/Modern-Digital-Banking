SELECT 
    DATE_TRUNC('month', txn_date) AS month,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY month
ORDER BY month;