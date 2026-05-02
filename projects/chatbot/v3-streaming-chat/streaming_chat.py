import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API_KEY / BASE_URL from repo-root `.env`.
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise ValueError("API_KEY and BASE_URL must be set")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """you are a useful assistant that can help with tasks and questions."""

# Conversation history sent on every round (same as non-streaming chatbots).
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

print(f"[Persona]: {SYSTEM_PROMPT}")
print("[Hint] Type 'exit', 'quit', or 'bye' to leave.\n")

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit", "bye"]:
        break

    messages.append({"role": "user", "content": user_input})

    # `stream=True`: receive the reply in chunks and print as they arrive.
    stream = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=messages,
        stream=True,
        extra_body={"thinking": {"type": "disabled"}},
    )

    print("Assistant: ", end="", flush=True)
    full_reply = ""
    for chunk in stream:
        token = chunk.choices[0].delta.content
        if token:
            print(token, end="", flush=True)
            full_reply += token
    print()

    # Must store the full text for the next request; streaming only changes how you receive it.
    messages.append({"role": "assistant", "content": full_reply})
