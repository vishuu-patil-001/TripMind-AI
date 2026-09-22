# syntax=docker/dockerfile:1.7

###############################################################################
# Builder - resolve and install dependencies into a self-contained /app/.venv
###############################################################################
FROM python:3.11-slim-bookworm AS builder

# uv is copied from its official image rather than pip-installed, so the
# builder never needs a network round trip for uv itself.
COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependency layer. Only pyproject.toml + uv.lock are copied here, so this
# layer is reused on every build where the dependency set has not changed.
COPY pyproject.toml uv.lock ./

# --no-install-project: this project has no [build-system], the source is
# copied in directly rather than installed as a package.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev


###############################################################################
# Runtime
###############################################################################
FROM python:3.11-slim-bookworm AS runtime

COPY --from=ghcr.io/astral-sh/uv:0.9.17 /uv /uvx /bin/

# curl is used by the container healthcheck against /health.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Run as a non-root user. The local MCP servers are spawned as child
# processes, so they inherit this user too.
RUN groupadd --system --gid 1001 app \
    && useradd --system --uid 1001 --gid app --create-home app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:/home/app/.local/bin:$PATH" \
    VIRTUAL_ENV=/app/.venv \
    UV_CACHE_DIR=/home/app/.cache/uv \
    UV_TOOL_DIR=/home/app/.local/share/uv/tools \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

# The aviationstack MCP server is launched at runtime with `uvx
# aviationstack-mcp` (see src/mcp_servers/config.py). Installing it at build
# time means the first flight request does not have to download it, and the
# container works even when outbound PyPI access is blocked.
#
# The mcp<2 pin matches src/mcp_servers/config.py - aviationstack-mcp uses the
# v1 FastMCP API that mcp 2.x renamed to MCPServer. It also requires Python
# >= 3.13, so uv provisions that interpreter for the tool environment only;
# the app itself still runs on 3.11.
USER app
RUN uv tool install --with "mcp<2" aviationstack-mcp \
    || echo "WARNING: could not pre-install aviationstack-mcp; uvx will fetch it on first use"

COPY --chown=app:app app.py ./
COPY --chown=app:app src/ ./src/
COPY --chown=app:app frontend/ ./frontend/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl --fail --silent http://127.0.0.1:${PORT}/health || exit 1

# Always bind 0.0.0.0. Inside a container that is the only correct answer, and
# hard-coding it means a stray HOST=127.0.0.1 in the environment - copied from
# a local .env into a hosting dashboard, say - cannot make the service
# unreachable. PORT stays configurable because hosts assign it (Render sends
# 10000 by default).
CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
