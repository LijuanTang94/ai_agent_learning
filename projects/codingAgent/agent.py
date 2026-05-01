import json
import os
import subprocess
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY and BASE_URL must be set")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["path"]
            }
        }
    }, 
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "The contents to write to the file"
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return the output",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run"
                    }
                },
                "required": ["command"]
            }
        }
    }
]

def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {path}"
    except Exception as e:
        return f"Error reading file {path}: {e}"

def write_file(path, content):
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Written to {path}"
    except Exception as e:
        return f"Error writing file {path}: {e}"

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        output = result.stdout
        if result.returncode != 0:
            output += f"\n[Error] {result.stderr}"
        return output or "No output"
    except subprocess.TimeoutExpired:
        return "[Error] Command timed out(10 seconds)"
    except Exception as e:
        return f"Error running command {command}: {e}"

tool_functions = {
    "read_file": read_file,
    "write_file": write_file,
    "run_command": run_command
}

SYSTEM_PROMPT = """
you are a coding assistant that can help with coding tasks. you can read files, write files and run commands. your workflow is as follows: first you need to understand the user's request and then you need to decide which tool to use. then you need to use the tool to complete the task. and you can run commands to validate the results. if you find the error, you need to correct the code and run again, and you can repeat this process until you get the correct result.
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]
print("Welcome to the coding assistant! Type 'exit', 'quit' or 'bye' to end the session.")

while True:
    user_input = input("you: ")
    if user_input.strip().lower() in ["exit", "quit", "bye", "q"]:
        print("Goodbye!")
        break
    messages.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            tools=tools,
            extra_body={"reasoning_effort": "high"},
        )
        assistant_message = response.choices[0].message

        if not assistant_message.tool_calls:
            break

        # Must append assistant turn (with tool_calls) before each tool message.
        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:
            # arguments is a JSON string — use loads, not load (load reads files).
            args = json.loads(tool_call.function.arguments or "{}")
            func = tool_functions[tool_call.function.name]
            result = func(**args)
            result_str = result if isinstance(result, str) else str(result or "")
            print(f"[tool] {tool_call.function.name}({args})")
            print(f"[result] {result_str[:200]}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_str,
                }
            )
    messages.append({"role": "assistant", "content": assistant_message.content})
    print(f"AI: {assistant_message.content}\n")

