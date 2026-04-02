ALTER TABLE transactions
ADD CONSTRAINT amount_positive CHECK (amount > 0);