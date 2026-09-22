"""Every prompt template used by the travel agents."""

FLIGHT_SYSTEM_PROMPT = "You are an expert travel flight planner."

FLIGHT_AGENT_PROMPT = """
You are a travel flight expert.

User Query:
{query}

Airport Information:
{airport_data}

Airline Information:
{airline_data}

Generate:

1. Likely departure airport
2. Likely arrival airport
3. Airlines serving this route
4. Typical flight duration
5. Estimated airfare range
6. Peak season pricing warning
7. Booking advice

Return concise travel guidance.
"""


ITINERARY_SYSTEM_PROMPT = "You are an expert travel planner."

ITINERARY_AGENT_PROMPT = """
Create a complete travel itinerary.

User Query:
{user_query}

Flight Results:
{flight_results}

Hotel Results:
{hotel_results}

Weather Results:
{weather_results}

Make the itinerary practical, budget-aware, and easy to follow.
"""


FINAL_SYSTEM_PROMPT = "You are a professional AI travel booking assistant."

FINAL_AGENT_PROMPT = """
Generate the final travel response for the user.

User Request:
{user_query}

Flights:
{flight_results}

Hotels:
{hotel_results}

Weather:
{weather_results}

Itinerary:
{itinerary}

Format the final answer beautifully using these sections:

1. Trip Summary
2. Flight Information
3. Hotel Suggestions
4. Weather Information
5. Day-by-Day Itinerary
6. Estimated Budget
7. Final Recommendations


Important:
- Be clear and practical.
- Mention that live flight API may not provide ticket prices if pricing is unavailable.
- Include weather-based travel advice.
- Keep the response useful for real travel planning.
"""


HOTEL_SEARCH_QUERY = "Best hotels for {user_query}"


WEATHER_RESULTS_TEMPLATE = """
        Current Weather:
        {weather_data}

        Forecast:
        {forecast_data}
        """


DESTINATION_EXTRACTION_PROMPT = """
    Extract only the destination city or country.

    Query:
    {query}

    Return only destination name.
    """
