# Workflow vs Agent (demo)

This folder holds a **fixed pipeline** example: fetch data → parse → call an LLM → save a file. The steps are scripted in order (workflow), not decided at runtime by a tool loop (agent).

## Script

- `daily_report.py` — scrapes GitHub Trending (daily), extracts repo lines, asks the model for a short English summary, writes `trending_report_YYYY-MM-DD.md` in this directory.
- `daily_report_prefect.py` — same report goal, but organized with Prefect `@task` and `@flow` for retries and clearer workflow orchestration.

## Setup

From repo root (same `.env` as other projects: `API_KEY`, `BASE_URL`):

```bash
pip install openai python-dotenv requests beautifulsoup4 prefect
```

## Run

```bash
cd projects/workflow_vs_agent
python daily_report.py
python daily_report_prefect.py
```

Generated reports are ignored by git (`trending_report_*.md`) unless you force-add them.
