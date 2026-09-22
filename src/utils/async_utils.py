"""
Helpers for calling async MCP tools from the synchronous graph nodes.

app.py applies nest_asyncio, which is what makes asyncio.run() safe to
call from inside FastAPI's already-running event loop.
"""

import asyncio
from typing import Any, Awaitable, TypeVar

T = TypeVar("T")


def run_async(coroutine: Awaitable[T]) -> T:
    """Run a coroutine to completion from synchronous code."""

    return asyncio.run(coroutine)


def bump_llm_calls(state: dict, count: int = 1) -> int:
    """Return the incremented LLM call counter for a node's state update."""

    return state.get("llm_calls", 0) + count


def truncate(value: Any, limit: int) -> str:
    """Stringify a tool payload and clip it so prompts stay within budget."""

    return str(value)[:limit]
