# AI Agent Learning Journey

This repository documents my hands-on learning path for building AI agents, from simple chatbots to more advanced agent workflows.

## Goal

- Build practical AI agent projects step by step.
- Keep a clear public learning trail on GitHub.
- Turn each learning module into runnable code and concise notes.

## Current Progress

- [x] Built a basic chatbot in `projects/chatbot/v1-basic/chatbot.py`
- [x] Built a tool-calling chatbot in `projects/chatbot/v2-tool-calling/chatbot.py`
- [x] Built a coding agent in `projects/codingAgent/agent.py`
- [x] Added streaming chat in `projects/chatbot/v3-streaming-chat/streaming_chat.py`
- [x] Added workflow-style demo in `projects/workflow_vs_agent/daily_report.py`
- [x] Added GitHub MCP examples in `github-mcp/` (`server.py`, `agent_mcp.py`; see `github-mcp/README.md`)
- [ ] Analyze MCP communication protocol (notes / deeper dive)
- [ ] Customize AI workflow with Skills
- [ ] Explore advanced traffic/debugging tools

## Planned Learning Path

1. Build an AI chatbot
2. Understand LLM API streaming mode
3. Workflow vs Agent
4. Build a coding agent
5. Develop an MCP tool
6. Analyze MCP protocol
7. Customize workflow with Skills
8. Advanced debugging and protocol analysis

## Repository Structure

```text
ai_agent_learning/
├── .gitignore
├── github-mcp/
│   ├── README.md
│   ├── server.py
│   ├── agent_mcp.py
│   └── pyproject.toml
├── projects/
│   ├── chatbot/
│   │   ├── README.md
│   │   ├── v1-basic/
│   │   │   └── chatbot.py
│   │   ├── v2-tool-calling/
│   │   │   └── chatbot.py
│   │   └── v3-streaming-chat/
│   │       └── streaming_chat.py
│   ├── codingAgent/
│   │   ├── README.md
│   │   ├── agent.py
│   │   ├── fib.py
│   │   └── buggy.py
│   └── workflow_vs_agent/
│       ├── README.md
│       ├── daily_report.py
│       └── daily_report_prefect.py
└── README.md
```

## Quick Start (Chatbot)

### 1) Create environment variables

Create a `.env` file in the project root:

```env
API_KEY=your_api_key
BASE_URL=your_model_base_url
```

### 2) Install dependencies

```bash
pip install openai python-dotenv requests beautifulsoup4 prefect
```

### 3) Run

```bash
python projects/chatbot/v1-basic/chatbot.py
```

Or run the tool-calling version:

```bash
python projects/chatbot/v2-tool-calling/chatbot.py
```

Streaming (token-by-token output):

```bash
python projects/chatbot/v3-streaming-chat/streaming_chat.py
```

Type `exit`, `quit`, or `bye` to stop (v1, v2, v3).

### Coding Agent

```bash
cd projects/codingAgent
python agent.py
```

Exit with `q`, `exit`, `quit`, or `bye`. Run from `codingAgent/` so file paths in tasks match the tutorial.

### Workflow demo (GitHub Trending daily report)

```bash
cd projects/workflow_vs_agent
python daily_report.py
python daily_report_prefect.py
```

Writes `trending_report_YYYY-MM-DD.md` in that folder (gitignored by default).

### GitHub MCP (`github-mcp/`)

Use **`uv`** in that folder (keeps dependencies in `github-mcp/.venv`; see `github-mcp/README.md`):

```bash
cd github-mcp
uv sync
uv run python server.py
# or: uv run python agent_mcp.py
```

Optional: `GITHUB_TOKEN` in `.env` for higher GitHub API rate limits (documented in `github-mcp/README.md`).

## Notes

- This is a learning-focused repository, so code and notes will evolve continuously.
- Module sections track learning milestones, while `v1/v2/...` folders track implementation iterations within a single project.
- Each module will be expanded with:
  - runnable demos
  - implementation notes
  - lessons learned

## Module 01 - Build an AI Chatbot

### What I built

- Implemented a CLI chatbot in `projects/chatbot/v1-basic/chatbot.py`.
- Loaded API credentials from `.env` using `python-dotenv`.
- Sent chat history (`messages`) to the model for multi-turn context.
- Added a system prompt to control assistant persona and tone.
- Added simple exit commands: `exit`, `quit`, and `bye`.

### What I learned

- A chatbot loop is mostly input -> append history -> request model -> print response.
- The system prompt strongly influences output style and role behavior.
- Keeping conversation history is the foundation of context-aware interaction.
- Environment variables are required for safer local development.

## Module 02 - Tool Calling Chatbot

### What I built

- Implemented a tool-calling chatbot in `projects/chatbot/v2-tool-calling/chatbot.py`.
- Added a function tool schema (`get_weather`) to the chat completion request.
- Parsed tool arguments from model-generated tool calls.
- Executed local Python functions and appended tool outputs back to messages.
- Triggered a follow-up model response after tool execution.

### What I learned

- Tool calling requires clear function schemas with strict parameter definitions.
- The assistant-tool-assistant loop is essential for turning tool output into final answers.
- Message ordering matters: user message, assistant tool call, tool result, final assistant reply.
- Tool outputs should be structured and predictable to reduce model confusion.

## Module 03 - Coding Agent (tool loop)

### What I built

- Implemented `projects/codingAgent/agent.py` with tools: `read_file`, `write_file`, `run_command`.
- Inner `while True` agent loop so the model can chain multiple tool steps before the final reply.
- Used `extra_body` with `reasoning_effort` for step-by-step decisions (per course notes).
- Practice targets: `fib.py` (generate and test) and `buggy.py` (read, fix, verify).

### What I learned

- Chatbot-style “one tool round then answer” hits a ceiling; an agent loop removes that cap.
- Ordering still matters: assistant (with `tool_calls`) must precede each `tool` message in `messages`.
- Long sessions with reasoning enabled can require careful message replay or a fresh process; production agents add limits, retries, and context management.

## Module 04 - Streaming completions

### What I built

- Implemented `projects/chatbot/v3-streaming-chat/streaming_chat.py` with `stream=True` on `chat.completions.create`.
- Printed each `delta.content` chunk as it arrives, then concatenated into `full_reply` for `messages` history.

### What I learned

- Streaming improves perceived latency: the user sees output before the model finishes the whole answer.
- Client code must still accumulate tokens into one string if the next turn needs a full assistant message in `messages`.
- Provider options (e.g. `extra_body` / thinking) behave the same streaming vs non-streaming; only the response shape is chunked.

## Module 05 - Workflow-style pipeline (vs agent loop)

### What I built

- Implemented `projects/workflow_vs_agent/daily_report.py`: fetch GitHub Trending HTML, parse repository rows with BeautifulSoup, take the top entries, call the chat API for an English summary, save a dated Markdown report.
- Added `projects/workflow_vs_agent/daily_report_prefect.py` to express the same workflow with Prefect `@task` / `@flow` orchestration and retries.

### What I learned

- A **workflow** runs a fixed sequence (fetch → transform → LLM → write); an **agent** lets the model choose tools and iterate until done.
- Workflows are simpler to reason about and debug; agents trade that for flexibility on messy tasks.
- Workflow frameworks like Prefect make retries and execution structure explicit without changing the business logic.
- Scraping public pages is brittle (markup changes); production systems prefer stable APIs or cached feeds.

## Module 06 - MCP: GitHub tools + LLM client

### What I built

- `github-mcp/server.py`: FastMCP stdio server exposing GitHub REST helpers as MCP tools.
- `github-mcp/agent_mcp.py`: spawns the server as a subprocess, lists tools, and runs the same “agent loop” pattern (LLM `tool_calls` → `call_tool` → follow-up).

### What I learned

- MCP splits **tool implementation** (server) from **orchestration** (client / LLM); stdio is the default local transport.
- The client must map MCP `inputSchema` to OpenAI-style `parameters`, and keep **spawn paths** and **`uv run python …`** correct or the child server never starts.
- Optional tokens (`GITHUB_TOKEN`) and LLM keys stay in `.env` (gitignored), not in source.
