/*ALTER TABLE users
ADD COLUMN phone_number VARCHAR(15);*/
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'users';
SELECT COUNT(*) FROM users;