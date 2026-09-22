"""Fetches current weather and forecast for the extracted destination."""

from langchain_core.messages import AIMessage

from src.agents.prompts import WEATHER_RESULTS_TEMPLATE
from src.graph.state import TravelState
from src.agents.destination import extract_destination
from src.mcp_servers.local import forecast_mcp_search, weather_mcp_search
from src.utils.async_utils import run_async


def weather_agent(state: TravelState):
    city = extract_destination(state["user_query"])

    weather_data = run_async(weather_mcp_search(city))
    forecast_data = run_async(forecast_mcp_search(city))

    return {
        "weather_results": WEATHER_RESULTS_TEMPLATE.format(
            weather_data=weather_data,
            forecast_data=forecast_data,
        ),
        "messages": [
            AIMessage(content="Weather information fetched")
        ],
    }
