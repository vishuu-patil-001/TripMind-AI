"""
Central configuration.

Everything that reads the environment lives here, so the rest of the
code never touches os.getenv directly.
"""

import os
from pathlib import Path

import certifi
from dotenv import load_dotenv

load_dotenv()


# Windows / corporate networks need an explicit CA bundle for outbound TLS.
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


# =========================
# Paths
# =========================

SRC_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = SRC_DIR.parent


# =========================
# API keys
# =========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


# =========================
# LLM
# =========================

# Groq retired the Llama 3.x chat models; check the live list with
#   GET https://api.groq.com/openai/v1/models
# if this ever starts returning model_not_found again.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


# =========================
# Prompt truncation limits
# =========================

AIRPORT_DATA_CHAR_LIMIT = int(os.getenv("AIRPORT_DATA_CHAR_LIMIT", "3000"))
AIRLINE_DATA_CHAR_LIMIT = int(os.getenv("AIRLINE_DATA_CHAR_LIMIT", "3000"))


# =========================
# Redis cache
# =========================

# No default. An unset REDIS_URL means "no cache", which is the safe answer
# on a hosted service - guessing localhost there would point at nothing and
# make every request pay a failed connection.
REDIS_URL = os.getenv("REDIS_URL") or None

# Explicit off switch. Caching also requires REDIS_URL to be set at all.
CACHE_ENABLED = (
    os.getenv("CACHE_ENABLED", "true").lower() not in ("false", "0", "no")
    and REDIS_URL is not None
)

# How long to wait before retrying a Redis connection that failed. Without
# this a single blip - a restart, a deploy - would disable the cache for the
# whole life of the process.
CACHE_RECONNECT_SECONDS = int(os.getenv("CACHE_RECONNECT_SECONDS", "60"))

CACHE_KEY_PREFIX = os.getenv("CACHE_KEY_PREFIX", "tripmind")

# TTLs in seconds, chosen to match how fast each source actually changes.
CACHE_TTL_AIRPORTS = int(os.getenv("CACHE_TTL_AIRPORTS", str(7 * 24 * 3600)))
CACHE_TTL_AIRLINES = int(os.getenv("CACHE_TTL_AIRLINES", str(7 * 24 * 3600)))
CACHE_TTL_HOTELS = int(os.getenv("CACHE_TTL_HOTELS", str(6 * 3600)))
CACHE_TTL_WEATHER = int(os.getenv("CACHE_TTL_WEATHER", str(10 * 60)))
CACHE_TTL_FORECAST = int(os.getenv("CACHE_TTL_FORECAST", str(3600)))
CACHE_TTL_DESTINATION = int(os.getenv("CACHE_TTL_DESTINATION", str(24 * 3600)))


# =========================
# Cross-origin / cookies
# =========================

# Comma-separated origins allowed to call this API from a browser. Leave unset
# when the frontend is proxied onto the same origin (see vercel.json), which
# keeps the session cookie first-party.
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

# A cross-site cookie must be SameSite=None, and SameSite=None requires
# Secure. Configuring CORS therefore implies both.
COOKIE_SAMESITE = os.getenv(
    "COOKIE_SAMESITE",
    "none" if CORS_ORIGINS else "lax",
).lower()

COOKIE_SECURE = os.getenv(
    "COOKIE_SECURE",
    "true" if COOKIE_SAMESITE == "none" else "false",
).lower() in ("true", "1", "yes")


def get_groq_api_key() -> str:
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Please add it to your .env file."
        )

    return GROQ_API_KEY


def normalize_database_url(database_url: str) -> str:
    """Default to sslmode=require, which managed Postgres providers expect."""

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url


def get_database_url() -> str:
    if not DATABASE_URL:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL "
            "External Database URL to .env"
        )

    return normalize_database_url(DATABASE_URL)

