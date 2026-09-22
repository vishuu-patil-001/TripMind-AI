"""
Per-session credentials.

Keys can come from two places:

* the server's .env  - shared by everyone, set once at deploy time
* the browser session - typed into the settings panel, held in memory only

Session values take precedence, are never written to disk, and disappear
when the session expires. Resolution happens through a ContextVar so the
agents can stay unaware of where a key came from.
"""

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

from src.config import settings


@dataclass(frozen=True)
class Credentials:
    groq_api_key: str | None = None
    database_url: str | None = None


EMPTY = Credentials()

_current: ContextVar[Credentials] = ContextVar("tripmind_credentials", default=EMPTY)


class MissingCredentialsError(RuntimeError):
    """Raised when a required key is configured in neither .env nor the session."""

    def __init__(self, missing: list[str]):
        self.missing = missing

        super().__init__(
            "Missing credentials: "
            + ", ".join(missing)
            + ". Add them in Settings, or set them in the server's .env file."
        )


def get_credentials() -> Credentials:
    return _current.get()


@contextmanager
def use_credentials(credentials: Credentials | None):
    """Bind session credentials for the duration of one request."""

    token = _current.set(credentials or EMPTY)

    try:
        yield
    finally:
        _current.reset(token)


# =========================
# Resolution
# =========================

def resolve_groq_api_key() -> str | None:
    return get_credentials().groq_api_key or settings.GROQ_API_KEY


def resolve_database_url() -> str | None:
    url = get_credentials().database_url or settings.DATABASE_URL

    return settings.normalize_database_url(url) if url else None


def require(*names: str) -> None:
    """Raise MissingCredentialsError listing whichever of these is absent."""

    resolvers = {
        "GROQ_API_KEY": resolve_groq_api_key,
        "DATABASE_URL": resolve_database_url,
    }

    missing = [name for name in names if not resolvers[name]()]

    if missing:
        raise MissingCredentialsError(missing)


# =========================
# Status, for the settings UI
# =========================

CREDENTIAL_LABELS = {
    "GROQ_API_KEY": {
        "label": "Groq API key",
        "hint": "Powers every agent. Create one at console.groq.com/keys.",
        "placeholder": "gsk_...",
    },
    "DATABASE_URL": {
        "label": "PostgreSQL URL",
        "hint": "Stores LangGraph conversation checkpoints.",
        "placeholder": "postgresql://user:password@host:5432/dbname",
    },
}


def credential_status() -> dict:
    """
    Describe what is configured and where it came from, without ever
    returning the secret itself.
    """

    session = get_credentials()

    sources = {
        "GROQ_API_KEY": (
            "session" if session.groq_api_key
            else "env" if settings.GROQ_API_KEY
            else None
        ),
        "DATABASE_URL": (
            "session" if session.database_url
            else "env" if settings.DATABASE_URL
            else None
        ),
    }

    credentials = {
        name: {
            **CREDENTIAL_LABELS[name],
            "configured": source is not None,
            "source": source,
        }
        for name, source in sources.items()
    }

    missing = [name for name, source in sources.items() if source is None]

    return {
        "ready": not missing,
        "missing": missing,
        "credentials": credentials,
    }

