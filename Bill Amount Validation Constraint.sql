ALTER TABLE bills
ADD CONSTRAINT amount_positive
CHECK (amount_due > 0);
