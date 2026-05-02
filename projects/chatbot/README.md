# Chatbot Project Series

This folder contains incremental chatbot versions used in my AI agent learning path.

## Versions

- `v1-basic`: baseline multi-turn chatbot with a fixed system prompt.
- `v2-tool-calling`: chatbot with function-calling support (`get_weather`).
- `v3-streaming-chat`: same chat pattern as v1, but with `stream=True` and incremental stdout.

## Run

From repository root:

```bash
python projects/chatbot/v1-basic/chatbot.py
python projects/chatbot/v2-tool-calling/chatbot.py
python projects/chatbot/v3-streaming-chat/streaming_chat.py
```
