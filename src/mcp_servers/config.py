"""
MCP server registry, split by where the server actually runs.

REMOTE servers are reached over HTTP and are operated by someone else.
LOCAL servers are spawned as child processes over stdio on this machine.

Keeping the two apart matters operationally: a remote server can be down
or rate limited, while a local one fails on missing binaries, a bad
interpreter path or a missing file.
"""

import os
import sys
from functools import lru_cache
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient

from src.config.settings import (
    AVIATIONSTACK_API_KEY,
    OPENWEATHER_API_KEY,
    TAVILY_API_KEY,
)

# This package holds the weather server we ship ourselves.
MCP_DIR = Path(__file__).resolve().parent
WEATHER_SERVER_PATH = MCP_DIR / "weather_server.py"


def _child_env(**overrides: str) -> dict:
    """
    Full copy of the current environment plus explicit overrides.

    stdio servers are launched as subprocesses, and on Windows they need
    the complete parent environment (PATH, SystemRoot, ...) to start.
    """

    env = os.environ.copy()
    env.update({key: value or "" for key, value in overrides.items()})

    return env


# =========================
# Remote MCP servers (HTTP)
# =========================

REMOTE_SERVERS = {
    "tavily": {
        "transport": "streamable_http",
        "url": (
            "https://mcp.tavily.com/mcp/"
            f"?tavilyApiKey={TAVILY_API_KEY}"
        ),
    },
}


# =========================
# Local MCP servers (stdio)
# =========================

LOCAL_SERVERS = {
    "aviationstack": {
        "transport": "stdio",
        "command": "uvx",

        # aviationstack-mcp still imports mcp.server.fastmcp, which mcp 2.x
        # renamed to MCPServer. Without this pin uvx resolves mcp 2.x into
        # the server's isolated environment and it dies on import - which
        # flight_agent then swallows as "Flight information unavailable".
        "args": ["--with", "mcp<2", "aviationstack-mcp"],
        "env": _child_env(
            AVIATION_STACK_API_KEY=AVIATIONSTACK_API_KEY,
        ),
    },

    "weather": {
        "transport": "stdio",

        # Use the same interpreter that runs the app, so the server
        # gets the project's virtualenv.
        "command": sys.executable,
        "args": [str(WEATHER_SERVER_PATH)],
        "env": _child_env(
            OPENWEATHER_API_KEY=OPENWEATHER_API_KEY,
        ),
    },
}


MCP_SERVERS = {**REMOTE_SERVERS, **LOCAL_SERVERS}


@lru_cache(maxsize=1)
def get_client() -> MultiServerMCPClient:
    """Shared client covering every configured server."""

    return MultiServerMCPClient(MCP_SERVERS)


async def load_tools(server_name: str) -> dict:
    """
    Load one server's tools as {name: tool}.

    Deliberately loads a single server at a time. Loading them together
    meant one broken server took the working ones down with it.
    """

    tools = await get_client().get_tools(server_name=server_name)

    return {tool.name: tool for tool in tools}


def require_tools(server_name: str, tools: dict, *names: str) -> None:
    """Raise a readable error when a server is missing expected tools."""

    missing = [name for name in names if name not in tools]

    if not missing:
        return

    available = ", ".join(sorted(tools)) or "none"

    raise RuntimeError(
        f"Missing {server_name} MCP tools: {', '.join(missing)}. "
        f"Available tools: {available}"
    )
