"""
Cheap liveness checks for credentials typed into the settings panel.

Both checks are free and fast: the Groq one lists models rather than
running a completion, and the PostgreSQL one opens and closes a connection.
The point is to fail in the settings dialog rather than 40 seconds into a
trip request.
"""

import psycopg
import requests

from src.config.settings import normalize_database_url

GROQ_MODELS_URL = "https://api.groq.com/openai/v1/models"


def check_groq_api_key(api_key: str) -> tuple[bool, str]:
    try:
        response = requests.get(
            GROQ_MODELS_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
    except requests.RequestException as error:
        return False, f"Could not reach Groq: {error}"

    if response.status_code == 401:
        return False, "Groq rejected this key (401 Unauthorized)."

    if not response.ok:
        return False, f"Groq returned HTTP {response.status_code}."

    return True, "Key accepted by Groq."


def check_database_url(database_url: str) -> tuple[bool, str]:
    try:
        connection = psycopg.connect(
            normalize_database_url(database_url),
            connect_timeout=10,
        )
    except Exception as error:
        return False, f"Could not connect: {error}"

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as error:
        return False, f"Connected, but the test query failed: {error}"
    finally:
        connection.close()

    return True, "Connected successfully."
