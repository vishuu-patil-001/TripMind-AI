"""Finds hotel options for the destination through the Tavily MCP server."""

from langchain_core.messages import AIMessage

from src.agents.prompts import HOTEL_SEARCH_QUERY
from src.graph.state import TravelState
from src.mcp_servers.remote import tavily_mcp_search
from src.utils.async_utils import bump_llm_calls, run_async


def hotel_agent(state: TravelState):
    query = HOTEL_SEARCH_QUERY.format(user_query=state["user_query"])

    hotel_results = run_async(tavily_mcp_search(query))

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched.")
        ],
        "llm_calls": bump_llm_calls(state),
    }
