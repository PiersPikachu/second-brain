Line: database, bot, workers

docker-compose.yml in the root brings up with a single command:

Service What it does Database role
db PostgreSQL 16, schema schema_v0_1.sql, reference data db/02-seed.sql postgres
bot Telegram bot, shop 3 (funnel). Currently a stub: checks the token and access to pd bot_role — the only one with access to pd
worker-leads, worker-mini-audit, worker-sales, worker-monitoring, worker-retention shops 1, 2, 4, 5, 6 worker_role — without access to pd

The website is brought up separately: docker-compose.site.yml.

Running on the server

```sh
cp .env.example .env && chmod 600 .env   # fill in passwords, bot token, AITUNNEL key
docker compose up -d --build
docker compose ps                        # all services must be healthy
```

The database is accessible only to containers; the port is not published externally. Console:
docker compose exec db psql -U postgres factory.

Initialization runs once, on an empty pgdata volume: schema, reference data, roles.
If it did not complete, the database stays unhealthy, and the bot and workers do not start.
On a new server where there is no data yet, fix the cause and start over:
docker compose down -v && docker compose up -d. -v deletes all data — on a running
line this must not be done. Schema changes after startup — via migrations (not yet implemented).

How the worker is structured

python -m factory.worker --workshop <shop code> takes cards from its shop's buffers
(line.buffers.workshop_id) and for each calls the handler from factory/handlers.py:

1. claim — the card becomes in_progress (FOR UPDATE SKIP LOCKED, short transaction);
2. the handler works outside the transaction and returns a Result with cards for the next buffers;
3. complete in one transaction creates these cards and marks done. If the next buffer
   is full (limit N trigger), the card is returned to the queue after a minute, the attempt is not spent.

Handler failure — retry after 5, 10 minutes, after three attempts — defect isolator
(quarantined + a record in line.defects). A defect found by the check (QC) — the
kanban.Defect exception: the card immediately goes to the isolator. Once a minute the worker marks
expired cards older than the buffer's max_age and returns those abandoned by a crashed worker
(in_progress longer than 30 minutes). A failure of one card does not stop the worker.

For now all handlers are stubs: the card goes to the isolator with check_code = 'not_implemented'.
To implement a shop, replace the function for its buffer in HANDLERS.

Healthcheck: the worker and bot update the heartbeat file while they work with the database. Without a
database connection for longer than 15 minutes, the container becomes unhealthy.

Tests

Integration, on a real PostgreSQL 16 (each run creates and drops its own database):

```sh
docker run -d --name pgtest -e POSTGRES_PASSWORD=test -p 55432:5432 postgres:16-alpine
TEST_DATABASE_URL=postgresql://postgres:test@localhost:55432/postgres make test-factory
```

Not included in the skeleton

Shop and bot logic, schema migrations, database backups (for now — automatic hosting
backups), export of ratings for the website.