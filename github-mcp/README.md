# github-mcp

Two pieces:

| File | Role |
|------|------|
| `server.py` | **MCP server** (stdio): registers GitHub REST tools (`search_repos`, `get_repo_info`) via FastMCP. |
| `agent_mcp.py` | **CLI agent**: calls your LLM (`API_KEY` / `BASE_URL`), spawns `server.py` as a subprocess, and runs `session.call_tool` when the model requests tools. |

Always run commands **from `github-mcp/`** with **`uv`** so dependencies stay inside **`github-mcp/.venv`** (do not `pip install` into conda `base` unless you know what you are doing).

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed (`uv` on your `PATH`).
- One-time in this folder:

```bash
cd github-mcp
uv sync
```

Dependencies are declared in `pyproject.toml` (`mcp`, `httpx`, `openai`, `python-dotenv`, …).

---

## Environment variables

| Variable | Used by | Purpose |
|----------|---------|---------|
| `GITHUB_TOKEN` | `server.py` | Optional. Higher GitHub API rate limits; put in `github-mcp/.env` or parent `ai_agent_learning/.env`. |
| `API_KEY` | `agent_mcp.py` | Required. LLM API key (same pattern as other projects in this repo). |
| `BASE_URL` | `agent_mcp.py` | Required. OpenAI-compatible base URL for chat completions. |

Example `.env` (never commit secrets):

```env
GITHUB_TOKEN=ghp_xxx
API_KEY=sk-xxx
BASE_URL=https://api.deepseek.com
```

---

## Run the MCP server alone (stdio)

Used by MCP clients (Cursor, Inspector, or `agent_mcp.py`):

```bash
cd github-mcp
uv run python server.py
```

Or explicit venv interpreter:

```bash
github-mcp/.venv/bin/python github-mcp/server.py
```

The process **blocks** waiting on stdin; that is normal for stdio MCP.

---

## Run the LLM + MCP agent (`agent_mcp.py`)

Spawns `server.py` via `uv --directory <dir> run python server.py`, lists tools, then chat loop:

```bash
cd github-mcp
uv run python agent_mcp.py
```

Ensure `MCP_SERVER` in `agent_mcp.py` points at the real `server.py` (default: same directory as `agent_mcp.py`).

---

## Optional: MCP Inspector (`mcp dev`)

For debugging only; may prompt to install an npm package:

```bash
cd github-mcp
uv run mcp dev server.py
```

Answer `y` once if you want the web inspector. For day-to-day use, `uv run python server.py` or Cursor MCP config is enough.

---

## Wrapper script

If present:

```bash
chmod +x run-server.sh   # once
./run-server.sh
```

---

## Cursor / IDE MCP config (server only)

Point the client at the **project venv**, not conda `base`:

- **command**: `/abs/path/to/github-mcp/.venv/bin/python`
- **args**: `server.py`
- **cwd**: `/abs/path/to/github-mcp`

Or:

- **command**: `uv`
- **args**: `run`, `python`, `server.py`
- **cwd**: `github-mcp`

---

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| `No module named 'mcp'` / `openai` | Wrong interpreter. Use `uv run …` or `.venv/bin/python`. Run `uv sync`. |
| `Failed to spawn server.py` | `MCP_SERVER` pointed at `/server.py` or wrong directory; use real path to `github-mcp/server.py`. |
| `Use @tool() instead of @tool` | FastMCP requires `@mcp.tool()` with parentheses in `server.py`. |
| `unexpected argument '#'` after `uv sync` | You pasted a comment (`# …`) on the same line as `uv`; run commands **without** pasted comments. |
| `Connection closed` right after start | Child `server.py` crashed (bad path, missing deps). Fix spawn command first. |
| Reasoning / multi-turn 400 errors | `reasoning_effort` gateways sometimes require echoing reasoning fields; shorten session or adjust `extra_body` if your provider documents it. |

---

## Project layout

```text
github-mcp/
├── pyproject.toml
├── uv.lock
├── server.py          # MCP server (stdio)
├── agent_mcp.py       # LLM client + MCP tool loop
├── run-server.sh      # optional helper
└── README.md
```
