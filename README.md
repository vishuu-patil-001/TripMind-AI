# ✈️ TripMind AI — AI-Powered Travel Planner

<p align="center">
  <strong>Plan smarter. Research less. Travel better.</strong>
</p>

<p align="center">
  An AI-powered travel planning application that combines multi-agent orchestration, external travel data, and natural-language interaction to generate personalized trip plans.
</p>

<p align="center">
  <a href="YOUR_DEPLOYED_DEMO_URL">🚀 Live Demo</a>
  &nbsp;•&nbsp;
  <a href="https://github.com/vishuu-patil-001/TripMind-AI">💻 GitHub Repository</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.141+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-Multi--Agent-1C3C3C?style=for-the-badge" alt="LangGraph">
  <img src="https://img.shields.io/badge/MCP-Integration-6B46C1?style=for-the-badge" alt="MCP">
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

---

## 📌 Overview

**TripMind AI** is a full-stack AI travel planning application designed to simplify the process of researching and organizing a trip.

Instead of manually searching across multiple websites for destinations, flights, hotels, weather, and itinerary ideas, users can describe their travel requirements in natural language.

TripMind AI then processes the request through a **LangGraph-powered multi-agent workflow**, where specialized agents handle different parts of the planning process before combining their results into a structured travel plan.

### Example

```text
Plan a 7 day Japan trip from Dhaka in April with a mid-range budget,
focused on food and temples.
```

The application can coordinate:

- Destination research
- Flight research
- Hotel research
- Weather information
- Itinerary generation
- Budget-aware planning
- Final travel-plan generation

---

## ✨ Features

### 🤖 Multi-Agent AI Planning

TripMind AI separates travel planning into specialized agents rather than relying on one large prompt.

| Agent | Responsibility |
|---|---|
| 🗺️ Destination Agent | Destination research and recommendations |
| ✈️ Flight Agent | Flight and airport research |
| 🏨 Hotel Agent | Accommodation research |
| 🌤️ Weather Agent | Weather information |
| 📅 Itinerary Agent | Day-by-day itinerary generation |
| 🧠 Final Agent | Combines results into the final travel plan |

The agents are orchestrated using **LangGraph**.

---

### 💬 Natural-Language Interaction

Users can describe a trip conversationally instead of filling out a complex form.

For example:

```text
I want a relaxed 5-day trip to Rome and Florence
for two people with a mid-range budget.
I am interested in food, history, and scenic places.
```

The application converts the request into a structured travel-planning workflow.

---

### 🔎 External Travel Research

TripMind AI integrates external services to retrieve travel-related information such as:

- Destination information
- Flight and aviation data
- Hotel information
- Weather information
- Web research

External integrations are organized through the project's MCP-related components.

---

### 🧩 Model Context Protocol (MCP)

The project includes MCP-based integrations for connecting the AI workflow with external tools and data sources.

MCP-related functionality is organized under:

```text
src/mcp_servers/
```

The repository contains components for:

- Remote MCP integrations
- Local MCP integrations
- Weather information
- AviationStack integration
- MCP diagnostics

---

### ⚡ Redis Caching

Redis can be used as a caching layer for frequently requested travel information.

Caching helps:

- Reduce repeated external API requests
- Reduce unnecessary network calls
- Improve response time for repeated requests
- Reduce dependency on external services for cached information

Redis is optional and can be disabled when required.

---

### 💾 PostgreSQL Persistence

PostgreSQL is used for **LangGraph workflow checkpoint persistence**.

This allows workflow state to be persisted rather than relying only on in-memory execution.

---

### 🐳 Dockerized Development

The project includes Docker and Docker Compose configuration for running the application and supporting services locally.

The development environment can include:

- FastAPI application
- Redis
- PostgreSQL
- Persistent Docker volumes
- Health checks
- Non-root application execution

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Web User       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │    Application      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      LangGraph      │
                         │   Agent Workflow    │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
      │ Destination │        │    Flight   │        │    Hotel    │
      │    Agent    │        │    Agent    │        │    Agent    │
      └──────┬──────┘        └──────┬──────┘        └──────┬──────┘
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Weather Agent     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Itinerary Agent    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Final Agent     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Structured Travel  │
                         │        Plan         │
                         └─────────────────────┘

              ┌────────────────┐       ┌──────────────────┐
              │     Redis      │       │   PostgreSQL     │
              │     Cache      │       │   Checkpointer   │
              └────────────────┘       └──────────────────┘
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application runtime |
| **FastAPI** | Backend API |
| **LangGraph** | Multi-agent workflow orchestration |
| **LangChain** | AI application framework |
| **Groq** | LLM inference |
| **MCP** | External tool and data integration |
| **PostgreSQL** | Workflow checkpoint persistence |
| **Redis** | Caching |
| **uv** | Python dependency management |
| **Docker** | Containerization |
| **Docker Compose** | Local multi-service environment |
| **HTML / CSS / JavaScript** | Frontend |
| **Jinja2** | Frontend templating |

---

## 📂 Project Structure

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
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── css/
│       │   └── styles.css
│       │
│       └── js/
│           ├── app.js
│           └── markdown.js
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

# 🚀 Running Locally

## Prerequisites

For the Docker-based setup:

- Git
- Docker Desktop

For development without Docker:

- Python 3.11+
- uv

You will also need API credentials for the external services used by the application.

---

## 1. Clone the Repository

```powershell
git clone https://github.com/vishuu-patil-001/TripMind-AI.git
cd TripMind-AI
```

---

## 2. Configure Environment Variables

The repository includes:

```text
.env.example
```

Create your local `.env` file.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Open `.env` and configure your API credentials.

The primary configuration includes:

```env
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b

TAVILY_API_KEY=
AVIATIONSTACK_API_KEY=
OPENWEATHER_API_KEY=
```

If PostgreSQL persistence is enabled:

```env
DATABASE_URL=
```

If Redis caching is enabled:

```env
REDIS_URL=
CACHE_ENABLED=true
```

> **Important:** Never commit your actual `.env` file or API keys to GitHub.

---

## 3. Start the Application

Build and start the default Docker services:

```powershell
docker compose up --build -d
```

Check the running services:

```powershell
docker compose ps
```

The default setup starts the TripMind AI application and Redis.

---

## 4. Start Local PostgreSQL

If PostgreSQL persistence is required, start the optional database service:

```powershell
docker compose --profile local-db up -d postgres
```

Check:

```powershell
docker compose ps
```

The included local PostgreSQL configuration uses:

```env
DATABASE_URL=postgresql://tripmind:tripmind@postgres:5432/tripmind?sslmode=disable
```

These credentials are intended **only for the local development container**.

---

## 5. Open the Application

Once the containers are running:

```text
http://localhost:8000
```

---

## 🩺 Health Check

TripMind AI provides a health endpoint:

```http
GET /health
```

On Windows PowerShell:

```powershell
Invoke-WebRequest "http://localhost:8000/health" -UseBasicParsing
```

A healthy application should return an HTTP success response.

The exact response can vary depending on the configured environment and external services.

---

# 🔌 API Endpoints

## Health

```http
GET /health
```

Checks application health and dependency readiness.

---

## Application Configuration

```http
GET /api/config
```

Returns application/frontend configuration used by the client.

---

## Travel Planning

```http
POST /api/travel
```

Submits a travel request and executes the multi-agent travel-planning workflow.

---

# ⚙️ Environment Variables

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Groq API authentication |
| `GROQ_MODEL` | LLM model used by the application |
| `TAVILY_API_KEY` | Web/travel research |
| `AVIATIONSTACK_API_KEY` | Aviation and flight-related information |
| `OPENWEATHER_API_KEY` | Weather information |
| `DATABASE_URL` | PostgreSQL connection |
| `REDIS_URL` | Redis connection |
| `CACHE_ENABLED` | Enables/disables Redis caching |
| `HOST` | Application host |
| `PORT` | Application port |
| `RELOAD` | Development reload configuration |
| `LANGFUSE_SECRET_KEY` | Optional Langfuse secret |
| `LANGFUSE_PUBLIC_KEY` | Optional Langfuse public key |
| `LANGFUSE_BASE_URL` | Optional Langfuse endpoint |

See `.env.example` for the complete configuration options.

---

# 🧠 How the AI Workflow Works

A typical request follows this general flow:

```text
User Travel Request
        │
        ▼
Request Validation
        │
        ▼
LangGraph Workflow
        │
        ├──► Destination Research
        │
        ├──► Flight Research
        │
        ├──► Hotel Research
        │
        ├──► Weather Research
        │
        ▼
Itinerary Generation
        │
        ▼
Final Agent
        │
        ▼
Structured Travel Plan
```

The architecture allows different parts of the travel-planning problem to be handled independently before the final response is assembled.

---

# 📊 Caching

Redis is used as an optional caching layer.

Example configuration:

```env
CACHE_ENABLED=true
```

When running through Docker Compose, the application can communicate with Redis through:

```text
redis://redis:6379/0
```

Example cache TTL settings include:

```env
CACHE_TTL_AIRPORTS=604800
CACHE_TTL_AIRLINES=604800
CACHE_TTL_HOTELS=21600
CACHE_TTL_FORECAST=3600
CACHE_TTL_WEATHER=600
CACHE_TTL_DESTINATION=86400
```

These values are optional and can be adjusted according to the application's requirements.

---

# 🐳 Useful Docker Commands

### Check services

```powershell
docker compose ps
```

### View application logs

```powershell
docker compose logs --tail=100 app
```

### Follow application logs

```powershell
docker compose logs -f app
```

### View Redis logs

```powershell
docker compose logs --tail=100 redis
```

### View PostgreSQL logs

```powershell
docker compose logs --tail=100 postgres
```

### Restart the application

```powershell
docker compose restart app
```

### Stop services

```powershell
docker compose stop
```

### Stop PostgreSQL

```powershell
docker compose --profile local-db stop postgres
```

### Stop and remove containers

```powershell
docker compose down
```

---

# 🔐 Security

TripMind AI uses environment variables for sensitive configuration.

The following should **never** be committed to GitHub:

- API keys
- Database passwords
- Private database connection strings
- Redis credentials
- Langfuse secret keys
- Other service credentials

The repository should contain:

```text
.env.example
```

but not:

```text
.env
```

Verify that `.env` is ignored before pushing:

```powershell
git check-ignore -v .env
```

You can also verify that `.env` is not tracked:

```powershell
git ls-files ".env"
```

An empty result means Git is not tracking `.env`.

---

# ⚠️ External Service Limitations

TripMind AI depends on external APIs and services.

Individual integrations may be affected by:

- Invalid API credentials
- API rate limits
- Subscription restrictions
- Unsupported API features
- Provider outages
- Network failures
- Changes to external APIs

Therefore, an external integration may occasionally return incomplete information even when the main application itself is running correctly.

---

# 🛠️ Troubleshooting

## Application is not running

Check:

```powershell
docker compose ps
```

Then inspect:

```powershell
docker compose logs --tail=100 app
```

---

## Health endpoint fails

Run:

```powershell
Invoke-WebRequest "http://localhost:8000/health" -UseBasicParsing
```

Then inspect:

```powershell
docker compose logs --tail=100 app
```

---

## PostgreSQL connection error

Start PostgreSQL:

```powershell
docker compose --profile local-db up -d postgres
```

Check:

```powershell
docker compose ps
```

If `.env` was changed, recreate the application container:

```powershell
docker compose up -d --force-recreate app
```

---

## Redis connection problem

Check:

```powershell
docker compose ps
```

Then:

```powershell
docker compose logs --tail=100 redis
```

When using Docker Compose, the expected internal Redis address is:

```text
redis://redis:6379/0
```

---

## External API errors

Check the application logs:

```powershell
docker compose logs --tail=100 app
```

Verify:

- API keys
- Provider account limits
- Subscription availability
- Requested API functionality
- Network connectivity

---

# 📌 Project Status

TripMind AI currently demonstrates:

- Full-stack AI travel planning
- FastAPI backend
- Web frontend
- LangGraph multi-agent orchestration
- Groq LLM integration
- MCP-based external integrations
- Flight research
- Hotel research
- Weather information
- Destination research
- Itinerary generation
- Redis caching
- PostgreSQL checkpoint persistence
- Docker containerization
- Docker Compose local development
- Health monitoring
- Environment-based configuration

The project demonstrates how multiple AI agents, external tools, caching, persistence, and a web interface can be combined into a practical AI application.

---

# 🌐 Demo

### Live Demo

**[🚀 Try TripMind AI](YOUR_DEPLOYED_DEMO_URL)**

> The live demo link will be added here once the application is deployed.

### Source Code

**[💻 GitHub Repository](https://github.com/vishuu-patil-001/TripMind-AI)**

---

# 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](./LICENSE) for the complete license text.

---

## 👨‍💻 Project

**TripMind AI**

Built as an AI-powered travel-planning project demonstrating:

- Multi-agent AI systems
- LangGraph workflow orchestration
- MCP integrations
- API integration
- Persistent workflow state
- Redis caching
- Dockerized application architecture
- Full-stack web development

---