CREATE TABLE IF NOT EXISTS bills (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    biller_name VARCHAR(100),
    due_date DATE,
    amount_due NUMERIC(12,2),
    status bill_status_enum DEFAULT 'upcoming',
    auto_pay BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT*FROM bills;