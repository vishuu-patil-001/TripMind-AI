"""
Helpers for calling async MCP tools from the synchronous graph nodes.
"""

import asyncio
from typing import Any, Awaitable, TypeVar

T = TypeVar("T")


def run_async(coroutine: Awaitable[T]) -> T:
    """Run a coroutine to completion from synchronous code."""

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coroutine)

    # A synchronous graph node is being called while an event loop
    # is already running. Execute the coroutine in a separate thread
    # with its own event loop.
    import concurrent.futures

    def _run() -> T:
        return asyncio.run(coroutine)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        return executor.submit(_run).result()


def bump_llm_calls(state: dict, count: int = 1) -> int:
    """Return the incremented LLM call counter for a node's state update."""

    return state.get("llm_calls", 0) + count


def truncate(value: Any, limit: int) -> str:
    """Stringify a tool payload and clip it so prompts stay within budget."""

    return str(value)[:limit]
