"""Entry point the API layer calls to run one travel planning request."""

import uuid

from src.config.session import require
from src.graph.graph import get_travel_graph
from src.graph.state import initial_state


def run_travel_agent(user_input: str, thread_id: str | None = None) -> dict:
    # Check everything up front so the caller learns about every missing key
    # at once, rather than one per failed attempt.
    require("GROQ_API_KEY", "DATABASE_URL")

    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = get_travel_graph().invoke(
        initial_state(user_input),
        config=config,
    )

    final_answer = result["messages"][-1].content

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "weather_results": result.get("weather_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0),
    }


if __name__ == "__main__":
    # Run with:  python -m src.graph.runner
    user_query = (
        "I want to plan a trip to Paris in July. "
        "Can you help me find flights, hotels, and an itinerary?"
    )

    output = run_travel_agent(user_query, thread_id="test_thread_001")
    print(output["answer"])
