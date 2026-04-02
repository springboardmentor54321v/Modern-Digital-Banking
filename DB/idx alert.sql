CREATE INDEX idx_alerts_user_id
ON alerts(user_id);

CREATE INDEX idx_alerts_type
ON alerts(type);

CREATE INDEX idx_alerts_created_at
ON alerts(created_at);