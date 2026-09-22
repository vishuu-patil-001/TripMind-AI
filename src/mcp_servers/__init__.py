"""
MCP integration layer.

    config.py       server registry, split into REMOTE_SERVERS / LOCAL_SERVERS
    remote.py       HTTP servers  - Tavily
    local.py        stdio servers - AviationStack, Weather
    weather_server.py  the local weather server we ship
    diagnostics.py  connectivity checks
"""

from src.mcp_servers.config import (
    LOCAL_SERVERS,
    MCP_SERVERS,
    REMOTE_SERVERS,
    get_client,
    load_tools,
)
from src.mcp_servers.diagnostics import check_servers, get_all_tools
from src.mcp_servers.local import (
    aviation_mcp_call,
    forecast_mcp_search,
    weather_mcp_search,
)
from src.mcp_servers.remote import tavily_mcp_search

__all__ = [
    "LOCAL_SERVERS",
    "MCP_SERVERS",
    "REMOTE_SERVERS",
    "aviation_mcp_call",
    "check_servers",
    "forecast_mcp_search",
    "get_all_tools",
    "get_client",
    "load_tools",
    "tavily_mcp_search",
    "weather_mcp_search",
]
