# TripMind AI

> A multi-agent AI travel planner that researches flights, hotels, weather, and destinations, then turns the results into a personalized day-by-day itinerary.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB.svg" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/FastAPI-0.141+-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-1.x-1C3C3C.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/PostgreSQL-required-336791.svg" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/License-GPL--3.0-blue.svg" alt="License">
</p>

---

## Overview

Planning a trip often means switching between multiple services for flights, hotels, weather, destination research, and itinerary planning.

**TripMind AI** brings these tasks together into a single conversational travel-planning experience.

You describe the trip you want in natural language, for example:

> Plan a 10 day Europe trip from India in April with a mid-range budget.

The application uses a multi-agent workflow to research different parts of the trip and combine the results into a structured travel plan.

### What it can help with

| Area | Description |
|---|---|
| Flights | Airport and airline information for the requested route |
| Hotels | Accommodation research for the destination |
| Weather | Current conditions and forecast information |
| Destination | Destination-specific research and recommendations |
| Itinerary | A structured day-by-day travel plan |
| Budget | Estimated trip costs based on the generated plan |
| Conversations | Saved trips and follow-up questions |

---

## How It Works

TripMind AI is built around a multi-agent workflow.

A typical request moves through several specialized components:

```text
User Request
     |
     v
TripMind AI Application
     |
     v
+-------------------+
| LangGraph Workflow|
+-------------------+
     |
     +----> Destination Research
     |
     +----> Flight Research
     |
     +----> Hotel Research
     |
     +----> Weather Research
     |
     +----> Itinerary Generation
     |
     v
Final Travel Plan
     |
     +----> Plan
     +----> Itinerary
     +----> Flights
     +----> Hotels
     +----> Weather
```

The project uses LangGraph to coordinate the workflow and external services to retrieve travel-related information.

---

## Key Features

- Natural-language trip planning
- Multi-agent research workflow
- Flight and airport research
- Hotel research
- Weather and forecast information
- Destination research
- Day-by-day itinerary generation
- Budget estimation
- Saved trip sessions
- Follow-up questions on existing trips
- Markdown export
- Print-friendly results
- Light and dark mode
- PostgreSQL-backed persistence
- Optional Redis caching
- API-key based integration with external services

---

## Technology Stack

### Backend

- Python 3.11+
- FastAPI
- Uvicorn
- LangGraph
- LangChain
- LangChain-Groq
- MCP
- PostgreSQL
- Psycopg
- Redis

### External Services

- Groq — LLM inference
- Tavily — web research
- AviationStack — aviation information
- OpenWeather — weather information

### Frontend

The frontend is implemented with:

- HTML
- CSS
- JavaScript
- Jinja2 templates
- Markdown rendering

### Development & Deployment

- `uv` for Python dependency management
- Docker
- Docker Compose
- Vercel configuration included
- PostgreSQL for persistent application state
- Optional Redis caching

---

## Project Structure

```text
TripMind-AI/
│
├── app.py
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
├── vercel.json
├── .env.example
├── .gitignore
├── .dockerignore
├── LICENSE
├── README.md
│
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       ├── app.js
│   │       └── markdown.js
│   │
│   └── templates/
│       └── index.html
│
├── src/
│   ├── agents/
│   │   ├── destination.py
│   │   ├── final_agent.py
│   │   ├── flight_agent.py
│   │   ├── hotel_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── prompts.py
│   │   └── weather_agent.py
│   │
│   ├── api/
│   │   ├── sessions.py
│   │   └── validation.py
│   │
│   ├── clients/
│   │   ├── cache.py
│   │   ├── checkpointer.py
│   │   └── llm.py
│   │
│   ├── config/
│   │   ├── session.py
│   │   └── settings.py
│   │
│   ├── graph/
│   │   ├── graph.py
│   │   ├── runner.py
│   │   └── state.py
│   │
│   ├── mcp_servers/
│   │   ├── config.py
│   │   ├── diagnostics.py
│   │   ├── local.py
│   │   ├── remote.py
│   │   └── weather_server.py
│   │
│   └── utils/
│       └── async_utils.py
│
└── scripts/
    └── build-frontend.sh
```

---

## Getting Started

### Prerequisites

Before running TripMind AI locally, install:

- Python 3.11 or newer
- `uv`
- PostgreSQL
- Git

You will also need API credentials for the external services used by the application.

---

### 1. Clone the repository

```bash
git clone https://github.com/vishuu-patil-001/TripMind-AI.git
cd TripMind-AI
```

---

### 2. Install dependencies

This project uses `uv` for dependency management.

```bash
uv sync
```

---

### 3. Configure environment variables

Create a `.env` file in the project root.

You can use `.env.example` as the starting point:

```bash
copy .env.example .env
```

Then edit `.env` and provide your actual credentials.

Example:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

DATABASE_URL=postgresql://username:password@host:5432/database

REDIS_URL=redis://localhost:6379/0
CACHE_ENABLED=true

HOST=127.0.0.1
PORT=8000
RELOAD=true
```

### Environment variables

| Variable | Required | Purpose |
|---|:---:|---|
| `GROQ_API_KEY` | Yes | LLM access |
| `GROQ_MODEL` | No | Model used by the application |
| `TAVILY_API_KEY` | Yes | Web/travel research |
| `AVIATIONSTACK_API_KEY` | Yes | Aviation and airport information |
| `OPENWEATHER_API_KEY` | Yes | Weather information |
| `DATABASE_URL` | Yes | PostgreSQL persistence |
| `REDIS_URL` | No | Redis cache connection |
| `CACHE_ENABLED` | No | Enables/disables caching |
| `HOST` | No | Application host |
| `PORT` | No | Application port |
| `RELOAD` | No | Development reload option |

> **Security:** Never commit your `.env` file or real API keys to GitHub.

---

## 4. Start the application

Run:

```bash
uv run python app.py
```

The application should start on:

```text
http://127.0.0.1:8000
```

Open that address in your browser.

---

## Using TripMind AI

### Natural-language planning

Enter a request such as:

```text
Plan a 7 day trip to Japan from India in October for two people with a mid-range budget.
```

Or:

```text
Plan a relaxed 5 day trip to Rome and Florence for two people.
```

The application processes the request through its research and planning workflow.

---

### Trip Builder

The application also provides a structured trip builder.

You can provide information such as:

- Origin
- Destination
- Dates
- Duration
- Number of travelers
- Budget
- Travel interests

The application then helps construct the trip request.

---

### Generated Results

Trip results are organized into sections such as:

- **Plan**
- **Itinerary**
- **Flights**
- **Hotels**
- **Weather**

You can review the different parts of the generated travel plan without having to manually research each category separately.

---

## Data Persistence

TripMind AI uses PostgreSQL to persist application state.

The PostgreSQL connection is configured through:

```dotenv
DATABASE_URL=...
```

The project also supports Redis as an optional caching layer.

```dotenv
REDIS_URL=redis://localhost:6379/0
CACHE_ENABLED=true
```

When Redis is not configured, the application can operate without the cache.

---

## Docker

A Docker configuration is included in the repository.

To start the application using Docker Compose:

```bash
docker compose up --build
```

The included Compose configuration can provide the application, PostgreSQL, and Redis services for local development.

Before using Docker, make sure the required environment variables are configured in your `.env` file.

---

## Troubleshooting

### The application does not start

Check that Python and `uv` are installed:

```bash
python --version
uv --version
```

Then reinstall/synchronize dependencies:

```bash
uv sync
```

---

### `GROQ_API_KEY` is missing

Make sure the project root contains a `.env` file with:

```dotenv
GROQ_API_KEY=your_actual_key
```

Do not put the key into source code.

---

### `DATABASE_URL` is missing

The application requires PostgreSQL persistence.

Make sure `.env` contains a valid PostgreSQL connection string:

```dotenv
DATABASE_URL=postgresql://username:password@host:5432/database
```

Do not commit the real connection string to Git.

---

### The selected model is unavailable

LLM providers may change the models available to an API key over time.

If the configured model is unavailable, update:

```dotenv
GROQ_MODEL=your_available_model
```

using a model currently available to your Groq account.

---

### The application takes time to generate a plan

Trip planning involves multiple research and AI operations. Depending on the configured services and network conditions, generation can take some time.

---

## Security

This repository is designed to keep credentials outside the source code.

The following types of values should remain private:

- API keys
- Database passwords
- PostgreSQL connection strings containing credentials
- Redis credentials
- Langfuse secret keys
- Other service credentials

Use `.env` for local secrets and environment-variable configuration for deployment.

Before pushing changes, verify that no credentials have been added accidentally:

```bash
git status
```

You can also search the tracked files for common credential names:

```bash
git grep -n -I -E "GROQ_API_KEY|TAVILY_API_KEY|AVIATIONSTACK_API_KEY|OPENWEATHER_API_KEY|DATABASE_URL|REDIS_URL"
```

Seeing variable names or placeholders in documentation is expected. Real credential values should not appear in tracked source files.

---

## Development

Create a feature branch before making larger changes:

```bash
git checkout -b feature/your-feature-name
```

After making changes, test the application locally:

```bash
uv sync
uv run python app.py
```

Keep commits focused and descriptive.

Example:

```bash
git commit -m "Improve trip planning workflow"
```

---

## Contributing

Contributions and improvements are welcome.

A typical contribution workflow is:

1. Fork the repository.
2. Clone your fork.
3. Create a feature branch.
4. Make your changes.
5. Test the application.
6. Commit the changes.
7. Push the branch.
8. Open a pull request.

Please avoid committing secrets, generated credentials, or local environment files.

---

## License

This project is licensed under the **GNU General Public License v3.0**.

See [LICENSE](LICENSE) for the complete license text.

---

## Acknowledgements

TripMind AI uses several open-source libraries and external services, including:

- FastAPI
- LangChain
- LangGraph
- MCP
- PostgreSQL
- Redis
- Groq
- Tavily
- AviationStack
- OpenWeather

The respective projects and services retain their own licenses and terms of use.