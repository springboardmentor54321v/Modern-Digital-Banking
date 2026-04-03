-- Add Milestone 4 alert columns to existing `alerts` table (PostgreSQL)
-- Run once if your DB was created before the M3+M4 merge.

ALTER TABLE alerts
    ADD COLUMN IF NOT EXISTS type VARCHAR(50) NOT NULL DEFAULT 'info';

ALTER TABLE alerts
    ADD COLUMN IF NOT EXISTS is_read BOOLEAN NOT NULL DEFAULT false;
