import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load local environment variables from .env.
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
            "name": "get_weather",
            "description": "Get the weather of a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                         "description": "The city to get the weather of"
                    }

                },
                "required": ["city"]
            }
        }
    }
]


def get_weather(city: str) -> str:
    """Mock weather tool that returns a JSON string."""
    weather_data = {
        "beijing": {"temperature_c": 8, "condition": "cloudy"},
        "shanghai": {"temperature_c": 15, "condition": "sunny"},
        "guangzhou": {"temperature_c": 22, "condition": "showers"},
        "shenzhen": {"temperature_c": 25, "condition": "cloudy"},
        "chengdu": {"temperature_c": 18, "condition": "light rain"},
        "chongqing": {"temperature_c": 20, "condition": "overcast"},
        "xian": {"temperature_c": 16, "condition": "cloudy"},
    }

    city_key = city.strip().lower()
    data = weather_data.get(city_key, {"temperature_c": "unknown", "condition": "unknown"})
    return json.dumps(data)

tool_functions = {"get_weather": get_weather}

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to a weather tool. "
    "When users ask about weather, call the tool with a city name."
)
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print(f"[Persona]: {SYSTEM_PROMPT}")
print("[Hint] Type 'exit', 'quit', or 'bye' to leave.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        tools=tools,
        extra_body={"thinking": {"type": "disabled"}}
    )

    assistant_message = response.choices[0].message

    if assistant_message.tool_calls:
        messages.append(assistant_message)
        for tool_call in assistant_message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            func = tool_functions[tool_call.function.name]
            result = func(**args)
            print(f"Tool result: {tool_call.function.name}({args}) => {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            extra_body={"thinking": {"type": "disabled"}}
        )
        assistant_message = response.choices[0].message

    messages.append(assistant_message)
    print(f"Assistant: {assistant_message.content}\n")
