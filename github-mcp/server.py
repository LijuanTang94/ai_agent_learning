"""MCP server (stdio): exposes GitHub REST helpers as MCP tools via FastMCP."""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load `.env` from this folder and parent monorepo root (optional `GITHUB_TOKEN`).
_load_root = Path(__file__).resolve().parents[1] / ".env"
load_dotenv()
load_dotenv(_load_root)
mcp = FastMCP("github")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "github-mcp-server",
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


@mcp.tool()
async def search_repos(query: str, max_results: int = 5) -> str:
    """Search GitHub for repositories matching the query.

    Args:
        query: The search query string.
        max_results: Maximum number of results to return.

    Returns:
        A string containing the search results.
    """
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "per_page": max_results, "sort": "stars"}

    async with httpx.AsyncClient() as client:  # short-lived client per request
        response = await client.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
    if not data["items"]:
        return "No repositories found matching the query."
    
    results = []
    for repo in data["items"]:
        results.append(
            f"{repo['full_name']} (Star {repo['stargazers_count']})\n"
            f"Description: {repo['description']}\n"
            f"Language: {repo['language']}\n"
            f"URL: {repo['html_url']}\n"
        )
    return "\n\n".join(results)

@mcp.tool()
async def get_repo_info(owner: str, repo: str) -> str:
    """Get information about a specific GitHub repository.

    Args:
        owner: The owner of the repository.
        repo: The name of the repository.

    Returns:
        A string containing the repository information.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
    license_name = "No license"
    if data["license"]:
        license_name = data["license"].get("name", "No license")
    return (
        f"Repository: {data['full_name']}\n"
        f"Description: {data['description']}\n"
        f"Language: {data['language']}\n"
        f"Stars: {data['stargazers_count']}\n"
        f"Forks: {data['forks_count']}\n"
        f"Open Issues: {data['open_issues_count']}\n"
        f"License: {license_name}\n"
        f"URL: {data['html_url']}\n"
    )

if __name__ == "__main__":
    mcp.run(transport="stdio")