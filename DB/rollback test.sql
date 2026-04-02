ROLLBACK;
ALTER TABLE users
DROP COLUMN IF EXISTS temp_test_column;
BEGIN;
ALTER TABLE users
ADD COLUMN temp_test_column TEXT;
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'users'
AND column_name = 'temp_test_column';
ROLLBACK;
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'users'
AND column_name = 'temp_test_column';