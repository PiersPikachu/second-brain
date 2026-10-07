#!/bin/sh
# Run by the postgres image once, when the database is created (docker-entrypoint-initdb.d).
set -eu
: "${BOT_DB_PASSWORD:?BOT_DB_PASSWORD is not set}"
: "${WORKER_DB_PASSWORD:?WORKER_DB_PASSWORD is not set}"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /factory-db/roles.sql
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
     -v bot_pw="$BOT_DB_PASSWORD" -v worker_pw="$WORKER_DB_PASSWORD" <<'SQL'
ALTER ROLE bot_role    PASSWORD :'bot_pw';
ALTER ROLE worker_role PASSWORD :'worker_pw';
SQL