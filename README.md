# ✈️ TripMind AI — AI-Powered Travel Planner

<p align="center">
  <strong>Plan smarter. Research less. Travel better.</strong>
</p>

<p align="center">
  An AI-powered travel planning application that uses multi-agent orchestration, external travel integrations, and natural-language interaction to generate structured, personalized travel plans.
</p>

<p align="center">
  <a href="https://trip-mind-ai-tau.vercel.app">🚀 Live Demo</a>
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

## 📸 Screenshots

### 🏠 Application Interface

<p align="center">
  <img src="docs/screenshots/01-home.png" alt="TripMind AI home interface" width="900">
</p>

### 📝 Natural-Language Trip Request

<p align="center">
  <img src="docs/screenshots/02-trip-request.png" alt="TripMind AI travel request" width="900">
</p>

### 🤖 AI-Generated Travel Plan

<p align="center">
  <img src="docs/screenshots/03-generated-plan.png" alt="TripMind AI generated travel plan" width="900">
</p>

### 📱 Responsive Interface

<p align="center">
  <img src="docs/screenshots/04-responsive-view.png" alt="TripMind AI responsive interface" width="700">
</p>

---

## 📌 Overview

**TripMind AI** is a full-stack AI travel planning application designed to simplify the process of researching and organizing a trip.

Instead of manually searching across multiple websites for destinations, flights, hotels, weather, activities, and itinerary ideas, users can describe their travel requirements using natural language.

TripMind AI processes the request through a **LangGraph-powered multi-agent workflow**, where specialized agents handle different parts of the planning process before the results are combined into a structured travel plan.

### Example Request

```text
Plan a 7 day trip to Tokyo from Dhaka in April with a mid-range budget
for 1 traveller. Include flights, hotels, weather, activities,
and a detailed day-by-day itinerary.
```

The application can coordinate:

- 🗺️ Destination research
- ✈️ Flight-related research
- 🏨 Hotel research
- 🌤️ Weather information
- 📅 Itinerary generation
- 💰 Budget-aware planning
- 🧠 Final travel-plan generation

---

# ✨ Features

## 🤖 Multi-Agent AI Planning

TripMind AI separates travel planning into specialized agents instead of relying on a single large prompt.

| Agent | Responsibility |
|---|---|
| 🗺️ Destination Agent | Destination research and recommendations |
| ✈️ Flight Agent | Flight and airport research |
| 🏨 Hotel Agent | Accommodation research |
| 🌤️ Weather Agent | Weather information |
| 📅 Itinerary Agent | Day-by-day itinerary generation |
| 🧠 Final Agent | Combines research into the final travel plan |

These agents are orchestrated through **LangGraph**.

---

## 💬 Natural-Language Interaction

Users do not need to fill out a complicated travel form.

They can describe their requirements naturally:

```text
I want a relaxed 5-day trip to Rome and Florence
for two people with a mid-range budget.
I am interested in food, history, and scenic places.
```

The application converts the request into a structured travel-planning workflow.

---

## 🔎 External Travel Research

The application includes integrations for travel-related research such as:

- Destination information
- Flight and aviation information
- Hotel information
- Weather information
- Web research

The external integrations are organized through the project's MCP-related components.

---

## 🧩 Model Context Protocol (MCP)

TripMind AI includes MCP-based components for connecting the AI workflow with external tools and data sources.

MCP-related functionality is organized under:

```text
src/mcp_servers/
```

The repository includes components for:

- Remote MCP integrations
- Local MCP integrations
- Weather information
- AviationStack integration
- MCP diagnostics

---

## ⚡ Redis Caching

Redis can be used as an optional caching layer for frequently requested travel information.

Caching can help:

- Reduce repeated external API requests
- Reduce unnecessary network calls
- Improve response times for repeated requests
- Reduce dependency on external services for cached information

Redis can be enabled or disabled through configuration.

---

## 💾 PostgreSQL Persistence

PostgreSQL is used for **LangGraph workflow checkpoint persistence**.

This allows workflow state to be persisted instead of relying entirely on in-memory execution.

---

## 🐳 Dockerized Development

The project includes Docker and Docker Compose configuration for local development.

The development environment can include:

- FastAPI application
- Redis
- PostgreSQL
- Persistent Docker volumes
- Health checks
- Non-root application execution

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │       Web User      │
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
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
       │ Destination │       │    Flight   │       │    Hotel    │
       │    Agent    │       │    Agent    │       │    Agent    │
       └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
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
                         │ Structured Travel   │
                         │       Plan          │
                         └─────────────────────┘

                  ┌────────────────┐   ┌──────────────────┐
                  │     Redis      │   │   PostgreSQL     │
                  │     Cache      │   │   Checkpointer   │
                  └────────────────┘   └──────────────────┘
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.11+** | Application runtime |
| **FastAPI** | Backend API |
| **LangGraph** | Multi-agent workflow orchestration |
| **LangChain** | AI application framework |
| **Groq** | LLM inference |
| **MCP** | External tool and data integration |
| **PostgreSQL** | Workflow checkpoint persistence |
| **Redis** | Optional caching layer |
| **uv** | Python dependency management |
| **Docker** | Containerization |
| **Docker Compose** | Local multi-service development |
| **HTML / CSS / JavaScript** | Frontend |
| **Jinja2** | Frontend templating |

---

# 📂 Project Structure

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
├── docs/
│   └── screenshots/
│       ├── 01-home.png
│       ├── 02-trip-request.png
│       ├── 03-generated-plan.png
│       └── 04-responsive-view.png
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

### Docker-based setup

- Git
- Docker Desktop

### Development without Docker

- Python 3.11+
- uv

You will also need credentials for the external services configured by the application.

---

## 1. Clone the Repository

```powershell
git clone https://github.com/vishuu-patil-001/TripMind-AI.git
cd TripMind-AI
```

---

## 2. Configure Environment Variables

The repository provides an environment-variable template:

```text
.env.example
```

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

Configure the required values in `.env`.

Example:

```env
GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b

TAVILY_API_KEY=
AVIATIONSTACK_API_KEY=
OPENWEATHER_API_KEY=

DATABASE_URL=

REDIS_URL=
CACHE_ENABLED=true
```

> **Security:** Never commit your real `.env` file or API credentials to GitHub.

---

## 3. Start the Application

Build and start the Docker services:

```powershell
docker compose up --build -d
```

Check the services:

```powershell
docker compose ps
```

---

## 4. Start Local PostgreSQL

If PostgreSQL persistence is required:

```powershell
docker compose --profile local-db up -d postgres
```

Check:

```powershell
docker compose ps
```

The local Docker PostgreSQL configuration uses:

```env
DATABASE_URL=postgresql://tripmind:tripmind@postgres:5432/tripmind?sslmode=disable
```

These credentials are intended only for the local development container.

---

## 5. Open the Application

```text
http://localhost:8000
```

---

# 🩺 Health Check

TripMind AI provides a health endpoint:

```http
GET /health
```

Windows PowerShell:

```powershell
Invoke-WebRequest "http://localhost:8000/health" -UseBasicParsing
```

A healthy deployment should return a successful HTTP response.

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

Returns application/frontend configuration and reports the configuration state used by the application.

---

## Travel Planning

```http
POST /api/travel
```

Submits a natural-language travel request and executes the AI travel-planning workflow.

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

A typical request follows this flow:

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

Each specialized agent focuses on a particular part of the travel-planning problem.

The final agent combines the available information into a user-facing travel plan.

---

# 📊 Caching

Redis is an optional caching layer.

Example:

```env
CACHE_ENABLED=true
```

When using Docker Compose, the internal Redis address can be:

```text
redis://redis:6379/0
```

Example cache TTL configuration:

```env
CACHE_TTL_AIRPORTS=604800
CACHE_TTL_AIRLINES=604800
CACHE_TTL_HOTELS=21600
CACHE_TTL_FORECAST=3600
CACHE_TTL_WEATHER=600
CACHE_TTL_DESTINATION=86400
```

These values can be adjusted according to application requirements.

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

### Restart application

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

Verify that `.env` is ignored:

```powershell
git check-ignore -v .env
```

Verify that `.env` is not tracked:

```powershell
git ls-files ".env"
```

An empty result means Git is not currently tracking `.env`.

---

# ⚠️ External Service & Data Limitations

TripMind AI depends on external APIs, services, and AI-generated planning.

External information can be affected by:

- API availability
- API rate limits
- Provider subscription restrictions
- Unsupported API features
- Provider outages
- Network failures
- Changes to third-party APIs
- AI-generated estimates

### Important

Travel information displayed by the application should be treated as **planning assistance**, not as a guaranteed booking result.

In particular:

- Flight prices and schedules may not represent live bookable inventory.
- Hotel prices and availability can change.
- Weather information depends on the available weather source and forecast horizon.
- AI-generated recommendations and estimated budgets should be independently verified before making travel or financial decisions.

Always verify final flight, hotel, visa, weather, and booking information through the relevant official or booking provider before travelling.

---

# 🧪 Deployment Verification

The deployed application is available at:

**[🚀 TripMind AI — Live Demo](https://trip-mind-ai-tau.vercel.app)**

The production deployment has been tested for:

- ✅ Website availability
- ✅ Successful HTTP response
- ✅ API configuration readiness
- ✅ Required production credentials being configured
- ✅ Successful AI travel-plan generation
- ✅ Frontend-to-backend API communication

Production configuration includes the required Groq and PostgreSQL environment variables.

---

# 🌐 Live Demo

<p align="center">

### 🚀 [Open TripMind AI](https://trip-mind-ai-tau.vercel.app)

</p>

Try a request such as:

```text
Plan a 5 day trip from Mumbai to Tokyo starting October 15, 2026
for 1 traveller.
```

Or:

```text
Plan a 7 day trip to Tokyo from Dhaka in April
with a mid-range budget for 1 traveller.
Include flights, hotels, weather, activities,
and a detailed day-by-day itinerary.
```

---

# 💻 Source Code

**[View TripMind AI on GitHub](https://github.com/vishuu-patil-001/TripMind-AI)**

---

# 🎯 Project Highlights

TripMind AI demonstrates practical implementation of:

- Multi-agent AI systems
- LangGraph workflow orchestration
- LangChain-based AI application development
- Groq LLM integration
- Model Context Protocol (MCP)
- External API integration
- Natural-language application interfaces
- Travel research automation
- Structured itinerary generation
- PostgreSQL workflow persistence
- Redis caching
- FastAPI backend development
- Docker containerization
- Docker Compose development
- Production environment configuration
- REST API design
- Frontend/backend integration
- Environment-based secret management

---

# 📌 Project Status

**Status: Deployed and operational**

TripMind AI is currently available as a live web application and demonstrates an end-to-end AI travel-planning workflow from natural-language user input to a structured travel plan.

The project is intended as a practical demonstration of building and deploying an AI-powered application that combines:

```text
Natural Language
       ↓
FastAPI
       ↓
LangGraph
       ↓
Specialized AI Agents
       ↓
External Tools / APIs
       ↓
PostgreSQL / Redis
       ↓
Final Travel Plan
```

---

# 📄 License

This project is licensed under the **GNU General Public License v3.0**.

See [`LICENSE`](./LICENSE) for the complete license text.

---

## 👨‍💻 Project

**TripMind AI**

Built as an AI-powered travel-planning project demonstrating:

- Multi-agent AI architecture
- LangGraph orchestration
- MCP integrations
- External API integration
- Persistent workflow state
- Redis caching
- Dockerized architecture
- FastAPI backend development
- Full-stack web development

---

<p align="center">
  <strong>✈️ TripMind AI — Plan smarter. Research less. Travel better.</strong>
</p>