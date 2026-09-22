"""Connectivity checks for every configured MCP server."""

from src.mcp_servers.config import (
    LOCAL_SERVERS,
    MCP_SERVERS,
    REMOTE_SERVERS,
    load_tools,
)


async def check_servers(server_names=None) -> dict:
    """
    Try each server independently and report what it exposes.

    Returns {server_name: {"kind": ..., "ok": bool, "tools": [...],
                           "error": str | None}}
    """

    names = server_names or list(MCP_SERVERS)
    report = {}

    for name in names:
        kind = "remote" if name in REMOTE_SERVERS else "local"

        try:
            tools = await load_tools(name)

            report[name] = {
                "kind": kind,
                "ok": True,
                "tools": sorted(tools),
                "error": None,
            }

        except Exception as error:
            report[name] = {
                "kind": kind,
                "ok": False,
                "tools": [],
                "error": str(error),
            }

    return report


async def get_all_tools() -> list:
    """Flat list of every tool object across all reachable servers."""

    all_tools = []

    for name in MCP_SERVERS:
        try:
            tools = await load_tools(name)
            all_tools.extend(tools.values())
        except Exception as error:
            print(f"\nCould not connect to {name} MCP:\n{error}\n")

    return all_tools


if __name__ == "__main__":
    # Run with:  python -m src.mcp_servers.diagnostics
    import asyncio

    for server, status in asyncio.run(check_servers()).items():
        label = "OK " if status["ok"] else "FAIL"
        print(f"[{label}] {status['kind']:<6} {server}")

        if status["ok"]:
            for tool_name in status["tools"]:
                print(f"          - {tool_name}")
        else:
            print(f"          {status['error']}")

    print(f"\nremote: {list(REMOTE_SERVERS)}")
    print(f"local:  {list(LOCAL_SERVERS)}")
