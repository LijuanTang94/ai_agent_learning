import os
from openai import OpenAI
from dotenv import load_dotenv

# Load local environment variables from .env.
load_dotenv()

# Read required API configuration.
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY and BASE_URL must be set")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
# Keep a fixed assistant persona for every turn.
SYSTEM_PROMPT = (
    "You are a pirate captain. Reply in a pirate tone and frequently use words like "
    "'ahoy' and 'treasure'."
)

# Store full conversation history for multi-turn context.
messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print(f"[Persona]: {SYSTEM_PROMPT}")
print("[Hint] Type 'exit', 'quit', or 'bye' to leave.\n")

while True:
    user_input = input("You: ")
    if user_input.strip() in ["exit", "quit", "bye"]:
        break
    messages.append({"role":"user", "content": user_input})

    # Send the full message list so the model remembers prior turns.
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        extra_body={"thinking": {"type": "disabled"}}
    )

    reply = response.choices[0].message.content
    messages.append({"role":"assistant", "content": reply})

    print(f"Assistant: {reply}")

