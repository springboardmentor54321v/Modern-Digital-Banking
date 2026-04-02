SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'category_rules'::regclass;