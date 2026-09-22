"""
Local MCP servers, spawned as stdio child processes.

* aviationstack - third party server run via `uvx aviationstack-mcp`
* weather       - our own server in this package (weather_server.py)
"""

from src.clients.cache import async_cached
from src.config.settings import (
    CACHE_TTL_AIRLINES,
    CACHE_TTL_AIRPORTS,
    CACHE_TTL_FORECAST,
    CACHE_TTL_WEATHER,
)
from src.mcp_servers.config import (
    WEATHER_SERVER_PATH,
    load_tools,
    require_tools,
)

AVIATION_SERVER_NAME = "aviationstack"
WEATHER_SERVER_NAME = "weather"

CURRENT_WEATHER_TOOL = "get_current_weather"
FORECAST_TOOL = "get_forecast"


# Reference data that effectively never changes, so it is worth a long TTL.
LONG_LIVED_AVIATION_TOOLS = {
    "list_airports": CACHE_TTL_AIRPORTS,
    "list_airlines": CACHE_TTL_AIRLINES,
}


# =========================
# AviationStack
# =========================

_aviation_tools: dict = {}


async def _get_aviation_tools() -> dict:
    global _aviation_tools

    if _aviation_tools:
        return _aviation_tools

    tools = await load_tools(AVIATION_SERVER_NAME)

    if not tools:
        raise RuntimeError(
            "AviationStack MCP connected but returned no tools."
        )

    _aviation_tools = tools

    return _aviation_tools


async def _aviation_call(tool_name: str, tool_args: dict | None = None):
    tools = await _get_aviation_tools()

    tool = tools.get(tool_name)

    if tool is None:
        available = ", ".join(sorted(tools)) or "none"

        raise ValueError(
            f"AviationStack tool '{tool_name}' was not found. "
            f"Available tools: {available}"
        )

    return await tool.ainvoke(tool_args or {})


@async_cached(prefix="aviation:reference", ttl=CACHE_TTL_AIRPORTS)
async def _aviation_call_cached(tool_name: str, tool_args: dict | None = None):
    return await _aviation_call(tool_name, tool_args)


async def aviation_mcp_call(tool_name: str, tool_args: dict | None = None):
    """
    Call an AviationStack tool.

    Reference lookups (airports, airlines) are cached for a week. Live
    flight status is never cached, since stale data would be misleading.
    """

    if tool_name in LONG_LIVED_AVIATION_TOOLS:
        return await _aviation_call_cached(tool_name, tool_args)

    return await _aviation_call(tool_name, tool_args)


# =========================
# Weather
# =========================

_weather_tools: dict = {}


async def _get_weather_tools() -> dict:
    global _weather_tools

    if _weather_tools:
        return _weather_tools

    if not WEATHER_SERVER_PATH.exists():
        raise FileNotFoundError(
            f"Weather MCP server file was not found: {WEATHER_SERVER_PATH}"
        )

    tools = await load_tools(WEATHER_SERVER_NAME)

    require_tools(
        WEATHER_SERVER_NAME,
        tools,
        CURRENT_WEATHER_TOOL,
        FORECAST_TOOL,
    )

    _weather_tools = tools

    return _weather_tools


@async_cached(prefix="weather:current", ttl=CACHE_TTL_WEATHER)
async def weather_mcp_search(city: str):
    """Current conditions. Short TTL, because this genuinely changes."""

    tools = await _get_weather_tools()

    return await tools[CURRENT_WEATHER_TOOL].ainvoke({"city": city})


@async_cached(prefix="weather:forecast", ttl=CACHE_TTL_FORECAST)
async def forecast_mcp_search(city: str):
    """Multi-day forecast. OpenWeather only refreshes this hourly anyway."""

    tools = await _get_weather_tools()

    return await tools[FORECAST_TOOL].ainvoke({"city": city})
