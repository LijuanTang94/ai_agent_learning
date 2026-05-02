import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from datetime import date
from prefect import flow, task
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
if not API_KEY or not BASE_URL:
    raise ValueError("Environment variables API_KEY and BASE_URL must be set")


@task(retries=3)
def fetch_trending():
    # Pull today's trending page HTML from GitHub.
    url = "https://github.com/trending?since=daily"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


@task
def parse_repos(page_html):
    # Extract repository basics used for LLM summarization.
    soup = BeautifulSoup(page_html, "html.parser")
    repos = []
    for article in soup.select("article.Box-row"):
        link = article.select_one("h2 a")
        name = link["href"].strip("/") if link else "unknown"

        desc_tag = article.select_one("p.col-9")
        desc = desc_tag.text.strip() if desc_tag else "no description"

        lang_tag = article.select_one("span[itemprop='programmingLanguage']")
        lang = lang_tag.text.strip() if lang_tag else ""

        stars_tag = article.select_one("span.d-inline-block.float-sm-right")
        stars = stars_tag.text.strip() if stars_tag else ""

        repos.append(f"- {name} ({lang}) - {stars} \n {desc}")
    return repos


@task
def summarize(repos):
    # Keep the prompt input bounded for cost and latency.
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    repo_text = "\n".join(repos[:15])
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes GitHub trending repositories."
            },
             {
                "role": "user",
                "content": f"Here is today's GitHub Trending repository list. "
                       f"Write a short daily report in English. "
                       f"Select the 5 most noteworthy projects and explain "
                       f"what each project does, what is the link to the project, and why it matters."
                       f"\n\n{repo_text}"
             }
        ],
        extra_body={"thinking": {"type": "disabled"}}
    )
    return response.choices[0].message.content.strip()


@task
def save_report(summary):
    # Persist one markdown report per day.
    filename = f"trending_report_{date.today().strftime('%Y-%m-%d')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# GitHub Trending Daily ({date.today().strftime('%Y-%m-%d')})\n\n")
        f.write(summary)
    print(f"Report saved to {filename}")


@flow
def daily_report():
    # Task orchestration entrypoint: fetch -> parse -> summarize -> save.
    html_content = fetch_trending()
    repos = parse_repos(html_content)
    summary = summarize(repos)
    save_report(summary)


daily_report()
