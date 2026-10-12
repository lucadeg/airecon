"""Search public documentation through AIRecon's configured Parallel MCP server."""

from __future__ import annotations

import argparse
import asyncio
import json
import uuid

from airecon.proxy.mcp import mcp_call_tool, mcp_list_tools


async def call(tool: str, arguments: dict) -> dict:
    ok, payload = await mcp_call_tool("parallel", tool, arguments)
    result = payload.get("result", {})
    if not ok or result.get("isError"):
        raise RuntimeError(json.dumps(payload))
    return result


async def main(args: argparse.Namespace) -> None:
    ok, payload = await mcp_list_tools("parallel")
    if not ok:
        raise RuntimeError(json.dumps(payload))
    names = {tool["name"] for tool in payload.get("tools", [])}
    if not {"web_search", "web_fetch"}.issubset(names):
        raise RuntimeError("Parallel server must expose web_search and web_fetch")

    # Reuse the same identifier for related search and fetch calls.
    session_id = str(uuid.uuid4())
    result = await call("web_search", {
        "objective": args.objective,
        "search_queries": [args.query],
        "session_id": session_id,
    })
    print(json.dumps({"web_search": result}, indent=2))
    if args.fetch:
        result = await call("web_fetch", {
            "urls": [args.fetch],
            "session_id": session_id,
        })
        print(json.dumps({"web_fetch": result}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Concise web search query")
    parser.add_argument("--objective", required=True, help="What to find in public sources")
    parser.add_argument("--fetch", help="Optional public HTTP(S) page URL to fetch")
    try:
        asyncio.run(main(parser.parse_args()))
    except RuntimeError as error:
        parser.exit(1, f"{error}\n")
