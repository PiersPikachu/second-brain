-- Application roles. Passwords are set by db/03-roles.sh from environment variables.
--   bot_role    — Telegram bot: the only one that sees the pd schema (Telegram ID and consents)
--   worker_role — shop workers: core, line, billing, growth; without access to pd
-- Executed by the schema owner (postgres). Re-running is safe.

DO $$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'bot_role') THEN
    CREATE ROLE bot_role LOGIN;
  END IF;
  IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'worker_role') THEN
    CREATE ROLE worker_role LOGIN;
  END IF;
END $$;

-- Shared access to the working schemas
GRANT USAGE ON SCHEMA core, line, billing, growth TO bot_role, worker_role;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA core, line, billing, growth
  TO bot_role, worker_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA core, line, billing, growth
  TO bot_role, worker_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA core, line, billing, growth
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO bot_role, worker_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA core, line, billing, growth
  GRANT USAGE, SELECT ON SEQUENCES TO bot_role, worker_role;

-- Self-learning rules with self_tunable = false are changed by no application
REVOKE INSERT, UPDATE, DELETE ON growth.rules FROM bot_role, worker_role;

-- Personal data — bot only (see the end of schema_v0_1.sql)
REVOKE ALL ON SCHEMA pd FROM worker_role;
GRANT USAGE ON SCHEMA pd TO bot_role;
GRANT SELECT, INSERT, DELETE ON pd.telegram_links TO bot_role;