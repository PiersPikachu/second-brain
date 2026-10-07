import os

import psycopg


def connect(url: str | None = None) -> psycopg.Connection:
    """autocommit: each conn.transaction() is a real transaction, not a savepoint."""
    return psycopg.connect(url or os.environ["DATABASE_URL"], autocommit=True,
                           application_name=os.environ.get("WORKER_ID", "factory"))