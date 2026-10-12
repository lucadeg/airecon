# Parallel Search MCP

Use [Parallel Search MCP](https://docs.parallel.ai/integrations/mcp/search-mcp)
to search public security documentation and fetch web pages through AIRecon's
existing HTTP MCP caller. Anonymous search uses Fast mode and needs no Parallel
account or API key. The free endpoint has rate limits; LLM inference is separate.

## Setup

From an AIRecon source checkout, install the package and its declared dependencies
with Python 3.12 or newer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install .
```

Merge the `parallel` entry from [parallel-search.json](parallel-search.json) into
the `mcpServers` object in `~/.airecon/mcp.json`. If that file does not exist, create
`~/.airecon/` and copy the example there as `mcp.json`. Keep any existing server
entries. This is opt-in and does not change AIRecon's built-in web search provider.
Set `enabled` to `false` to disable it. The configured `User-Agent` identifies
AIRecon on discovery, search and fetch requests.

## Run a search and fetch

From the same checkout:

```bash
.venv/bin/python examples/mcp/parallel_search.py \
  --objective 'Find the Python documentation for parsing URLs' \
  --query 'Python urllib.parse documentation' \
  --fetch 'https://docs.python.org/3/library/urllib.parse.html'
```

The example loads your MCP configuration, discovers `web_search` and `web_fetch`,
then prints their MCP results as JSON, including source URLs and excerpts. Omit
`--fetch` to search only. It uses AIRecon's `mcp_list_tools` and `mcp_call_tool`
functions directly, so this check needs neither a running LLM nor Docker. It
reuses one generated session identifier for the related calls and reports HTTP
and tool errors, including rate limits, with a nonzero exit code.

Send only public research queries and URLs that you intend to share with Parallel.
Requests go to an external service; do not include credentials or private target
data. This example exercises AIRecon's JSON-over-HTTP MCP path, which the Parallel
endpoint supports; it does not require a legacy SSE endpoint or stdio bridge.
