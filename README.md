# AI Agent Learning Journey

This repository documents my hands-on learning path for building AI agents, from simple chatbots to more advanced agent workflows.

## Goal

- Build practical AI agent projects step by step.
- Keep a clear public learning trail on GitHub.
- Turn each learning module into runnable code and concise notes.

## Current Progress

- [x] Built a basic chatbot in `projects/chatbot/v1-basic/chatbot.py`
- [x] Built a tool-calling chatbot in `projects/chatbot/v2-tool-callinig/chatbot.py`
- [ ] Add streaming response support
- [ ] Compare workflow-based systems vs agent-based systems
- [ ] Build a coding agent prototype
- [ ] Build and test an MCP tool
- [ ] Analyze MCP communication protocol
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
├── projects/
│   └── chatbot/
│       ├── README.md
│       ├── v1-basic/
│       │   └── chatbot.py
│       └── v2-tool-callinig/
│           └── chatbot.py
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
pip install openai python-dotenv
```

### 3) Run

```bash
python projects/chatbot/v1-basic/chatbot.py
```

Or run the tool-calling version:

```bash
python projects/chatbot/v2-tool-callinig/chatbot.py
```

Type `exit`, `quit`, or `bye` to stop.

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

- Implemented a tool-calling chatbot in `projects/chatbot/v2-tool-callinig/chatbot.py`.
- Added a function tool schema (`get_weather`) to the chat completion request.
- Parsed tool arguments from model-generated tool calls.
- Executed local Python functions and appended tool outputs back to messages.
- Triggered a follow-up model response after tool execution.

### What I learned

- Tool calling requires clear function schemas with strict parameter definitions.
- The assistant-tool-assistant loop is essential for turning tool output into final answers.
- Message ordering matters: user message, assistant tool call, tool result, final assistant reply.
- Tool outputs should be structured and predictable to reduce model confusion.
