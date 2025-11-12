-- V2: add status column and created_at index
ALTER TABLE subscribers
  ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'active';

CREATE INDEX idx_subscribers_created_at ON subscribers(created_at);
