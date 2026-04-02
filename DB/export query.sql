SELECT 
    account_id,
    SUM(amount) AS total_spending
FROM transactions
GROUP BY account_id;