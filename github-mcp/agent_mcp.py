"""
CLI agent: OpenAI-compatible chat + MCP tools from local `server.py` (stdio subprocess).

Flow: spawn MCP server → list_tools → map to OpenAI `tools` → agent loop that calls
`session.call_tool` when the model returns function calls.
"""

import os
import asyncio
import json
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY and BASE_URL must be set")

# Absolute path to `server.py`. Never use a bare "/server.py" — that points at filesystem root.
MCP_SERVER = str(Path(__file__).resolve().parent / "server.py")

llm = OpenAI(api_key=API_KEY, base_url=BASE_URL)


@asynccontextmanager
async def mcp_connect(server_script):
    """Spawn `server_script` via uv and attach an MCP ClientSession over stdio."""
    server_dir, script = os.path.split(server_script)
    # `run python <script>` ensures uv executes it as Python (not as a raw executable).
    params = StdioServerParameters(
        command="uv",
        args=["--directory", server_dir, "run", "python", script],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session

async def main():
    async with mcp_connect(MCP_SERVER) as session:
        # MCP exposes JSON Schema per tool as `inputSchema`; OpenAI expects `parameters`.
        mcp_tools = await session.list_tools()
        tools = []
        for tool in mcp_tools.tools:
            tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            })
        
        print(f"Found {len(tools)} tools: {tools}")

        for t in tools:
            print(f"Tool: {t['function']['name']}")
            print(f"Description: {t['function']['description']}")
            print(f"Parameters: {t['function']['parameters']}")
        print()

        messages = [{
            "role": "system",
            "content": "you are a helpful assistant that can use the following tools to answer questions and help the user."
        }]
        print("Ready to chat! (type 'exit' to quit)")
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            messages.append({
                "role": "user",
                "content": user_input
            })

            # Inner loop: keep asking the model until it replies without tool_calls,
            # forwarding each tool result back into `messages` (same pattern as a coding agent).
            while True:
                response = llm.chat.completions.create(
                    model="deepseek-v4-flash",
                    messages=messages,
                    tools=tools,
                    extra_body={"reasoning_effort": "high"},
                )
                msg = response.choices[0].message

                if not msg.tool_calls:
                    break

                messages.append(msg)

                for tool_call in msg.tool_calls:
                    args = json.loads(tool_call.function.arguments or "{}")
                    # MCP tools/call → usually TextContent blocks in `result.content`.
                    result = await session.call_tool(
                        tool_call.function.name, arguments=args
                    )
                    block = result.content[0] if result.content else None
                    tool_result = getattr(block, "text", "") if block else ""
                    print(f"  [MCP] {tool_call.function.name}({args})")
                    print(f"  [result] {tool_result[:200]}")
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_result,
                        }
                    )

            messages.append({"role": "assistant", "content": msg.content})
            print(f"AI: {msg.content}\n")

asyncio.run(main())

