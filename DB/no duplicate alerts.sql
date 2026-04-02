/*ALTER TABLE alerts
DROP CONSTRAINT unique_daily_alert;*/
INSERT INTO alerts (user_id, type, created_at, message)
VALUES (1, 'budget_exceeded', NOW(), 'Budget exceeded');
INSERT INTO alerts (user_id, type, created_at, message)
VALUES (1, 'budget_exceeded', NOW(), 'Budget exceeded');