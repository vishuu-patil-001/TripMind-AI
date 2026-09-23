import os
from pathlib import Path
import traceback
import uvicorn

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.api.sessions import (
    SESSION_COOKIE,
    SESSION_TTL_SECONDS,
    clear_credentials,
    get_credentials_for,
    new_session_id,
    store_credentials,
)
from src.api.validation import check_database_url, check_groq_api_key
from src.clients import cache
from src.config.session import (
    MissingCredentialsError,
    credential_status,
    use_credentials,
)
from src.config.settings import COOKIE_SAMESITE, COOKIE_SECURE, CORS_ORIGINS
from src.graph.runner import run_travel_agent



BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="TripMind AI",
    description="LangGraph Multi-Agent Travel Planner with FastAPI Frontend",
    version="1.0.0"
)


# Only needed when the browser talks to this API on a different origin. With
# the Vercel rewrite the frontend is same-origin, so this stays inactive.
if CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )


app.mount(
    "/static",
    StaticFiles(directory=str(FRONTEND_DIR / "static")),
    name="static"
)


templates = Jinja2Templates(
    directory=str(FRONTEND_DIR / "templates")
)



class TravelRequest(BaseModel):
    message: str
    thread_id: str | None = None


class ConfigRequest(BaseModel):
    """
    None leaves a field untouched, "" clears it. Keys are held in server
    memory for this session only and are never echoed back.
    """

    groq_api_key: str | None = None
    database_url: str | None = None



def _session_id(request: Request) -> str | None:
    return request.cookies.get(SESSION_COOKIE)


def _set_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        session_id,
        max_age=SESSION_TTL_SECONDS,
        httponly=True,
        samesite=COOKIE_SAMESITE,
        secure=COOKIE_SECURE,
    )



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# =========================
# Credentials
# =========================

@app.get("/api/config")
async def read_config(request: Request):
    """What is configured, and where it came from. Never returns a secret."""

    credentials = get_credentials_for(_session_id(request))

    with use_credentials(credentials):
        return JSONResponse(content=credential_status())


@app.post("/api/config")
async def write_config(request: Request, body: ConfigRequest):
    """
    Store credentials for this browser session. Each supplied value is
    checked against the real service before being accepted.
    """

    session_id = _session_id(request) or new_session_id()

    errors = {}

    groq_key = (body.groq_api_key or "").strip()
    if groq_key:
        ok, detail = check_groq_api_key(groq_key)
        if not ok:
            errors["groq_api_key"] = detail

    database_url = (body.database_url or "").strip()
    if database_url:
        ok, detail = check_database_url(database_url)
        if not ok:
            errors["database_url"] = detail

    if errors:
        response = JSONResponse(
            status_code=400,
            content={"success": False, "errors": errors},
        )
        _set_session_cookie(response, session_id)
        return response

    credentials = store_credentials(
        session_id,
        groq_api_key=body.groq_api_key,
        database_url=body.database_url,
    )

    with use_credentials(credentials):
        payload = {"success": True, **credential_status()}

    response = JSONResponse(content=payload)
    _set_session_cookie(response, session_id)

    return response


@app.delete("/api/config")
async def reset_config(request: Request):
    """Drop session keys and fall back to whatever the server's .env has."""

    clear_credentials(_session_id(request))

    with use_credentials(None):
        return JSONResponse(content={"success": True, **credential_status()})


# =========================
# Planning
# =========================

@app.post("/api/travel")
async def travel_planner(request: Request, request_data: TravelRequest):
    credentials = get_credentials_for(_session_id(request))

    try:
        user_message = request_data.message.strip()

        if not user_message:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Message cannot be empty."
                }
            )

        with use_credentials(credentials):
            result = run_travel_agent(
                user_input=user_message,
                thread_id=request_data.thread_id
            )

        return JSONResponse(
            content={
                "success": True,
                "thread_id": result["thread_id"],
                "answer": result["answer"],
                "flight_results": result["flight_results"],
                "hotel_results": result["hotel_results"],
                "weather_results": result.get("weather_results", ""),
                "itinerary": result["itinerary"],
                "llm_calls": result["llm_calls"],
            }
        )

    except MissingCredentialsError as e:
        # The frontend turns this into a prompt to open Settings.
        return JSONResponse(
            status_code=428,
            content={
                "success": False,
                "error": str(e),
                "missing": e.missing,
            }
        )

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )



@app.head("/", include_in_schema=False)
async def home_head():
    """Hosting platforms probe with HEAD to detect an open port."""

    return Response(status_code=200)


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check(request: Request):
    credentials = get_credentials_for(_session_id(request))

    with use_credentials(credentials):
        status = credential_status()

    return {
        "status": "ok",
        "message": "AI Travel Planner API is running",
        "ready": status["ready"],
        "missing": status["missing"],
        "cache": cache.status(),
    }


@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(content={})



if __name__ == "__main__":
    # Defaults suit local development. In Docker, HOST is set to 0.0.0.0
    # so the port is reachable from outside the container.
    uvicorn.run(
        "app:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "true").lower() not in ("false", "0", "no")
    )

