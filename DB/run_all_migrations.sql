-- ============================================================
-- Milestone 4 — Master Migration File
-- Run this AFTER the backend has started once
-- (so SQLAlchemy creates all tables first)
-- ============================================================

-- STEP 1: Validate and update alerts table structure
\i alert_table_validation.sql

-- STEP 2: Create performance indexes
\i indexing_4.sql

-- STEP 3: Add data consistency constraints
\i data_consistency.sql

-- STEP 4: Run performance tests (verify indexes work)
\i performance_measure.sql

-- ============================================================
-- Quick verification — run after all steps
-- ============================================================

-- Show all tables
\dt

-- Show all indexes created
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename IN ('transactions', 'budgets', 'alerts', 'bills', 'users')
ORDER BY tablename, indexname;

-- Show all check constraints
SELECT
    tc.table_name,
    tc.constraint_name,
    cc.check_clause
FROM information_schema.table_constraints tc
JOIN information_schema.check_constraints cc
    ON tc.constraint_name = cc.constraint_name
WHERE tc.table_name IN ('transactions', 'budgets', 'bills', 'users')
ORDER BY tc.table_name;
