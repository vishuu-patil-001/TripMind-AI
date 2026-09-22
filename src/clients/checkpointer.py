"""PostgreSQL checkpointer used by LangGraph to persist conversation threads."""

from functools import lru_cache

import psycopg
from psycopg.rows import dict_row

from langgraph.checkpoint.postgres import PostgresSaver

from src.config.session import require, resolve_database_url


@lru_cache(maxsize=4)
def get_connection(database_url: str) -> psycopg.Connection:
    return psycopg.connect(
        database_url,
        autocommit=True,
        row_factory=dict_row,
    )


@lru_cache(maxsize=4)
def get_checkpointer(database_url: str) -> PostgresSaver:
    checkpointer = PostgresSaver(get_connection(database_url))
    checkpointer.setup()

    return checkpointer


def get_session_checkpointer() -> PostgresSaver:
    """Checkpointer for whichever database URL the current session resolves to."""

    require("DATABASE_URL")

    return get_checkpointer(resolve_database_url())
