# Coding Agent

CLI agent loop (labuladong-style): `read_file`, `write_file`, `run_command`, plus inner `while` for multi-step tasks.

## Run

From this directory (so relative paths match tutorial expectations):

```bash
cd projects/codingAgent
python agent.py
```

Requirements: repo-root `.env` with `API_KEY` and `BASE_URL` (see root `README.md`), and `pip install openai python-dotenv`.

## Practice files

- `buggy.py`: intentional bug exercise for the Agent to read, fix, and re-run.
- `fib.py`: sample solution the Agent can overwrite; safe to regenerate.

`run_command` executes arbitrary shell commands—use only in a trusted learning environment.
