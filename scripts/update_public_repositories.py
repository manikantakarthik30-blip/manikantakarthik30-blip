#!/usr/bin/env python3
"""Refresh the profile README directory of public repositories."""
import json
import os
import urllib.error
import urllib.request

OWNER = os.environ.get("GITHUB_OWNER", "manikantakarthik30-blip")
CURRENT_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", f"{OWNER}/{OWNER}")
README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
START = "<!-- PUBLIC_REPOSITORIES:START -->"
END = "<!-- PUBLIC_REPOSITORIES:END -->"


def fetch_public_repositories():
    repos = []
    page = 1
    token = os.environ.get("GITHUB_TOKEN")
    while True:
        url = f"https://api.github.com/users/{OWNER}/repos?type=public&sort=updated&per_page=100&page={page}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-public-repository-index/1.0",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=25) as response:
            batch = json.loads(response.read().decode("utf-8"))
        if not batch:
            break
        repos.extend(
            item for item in batch
            if not item.get("private", True)
            and f'{item.get("owner", {}).get("login", OWNER)}/{item["name"]}'.lower() != CURRENT_REPOSITORY.lower()
        )
        if len(batch) < 100:
            break
        page += 1
    return sorted(repos, key=lambda item: item["name"].casefold())


def clean_cell(value):
    return " ".join((value or "Description not provided").replace("|", "\\|").split())


def render_table(repos):
    lines = []
    for repo in repos:
        name = repo["name"]
        url = repo.get("html_url") or f"https://github.com/{OWNER}/{name}"
        lines.append(f"- [{name}]({url})")
    if not repos:
        lines.append("- No public repositories found.")
    lines.extend(["", f"[View all public repositories](https://github.com/{OWNER}?tab=repositories)"])
    return "\n".join(lines)


def main():
    with open(README_PATH, "r", encoding="utf-8") as handle:
        readme = handle.read()
    if START not in readme or END not in readme:
        raise RuntimeError("README repository-list markers are missing; refusing to overwrite content.")
    left, remainder = readme.split(START, 1)
    _old_section, right = remainder.split(END, 1)
    replacement = f"{START}\n{render_table(fetch_public_repositories())}\n{END}"
    updated = left + replacement + right
    if updated != readme:
        with open(README_PATH, "w", encoding="utf-8") as handle:
            handle.write(updated)
        print("Public repository directory updated.")
    else:
        print("Public repository directory is already current.")


if __name__ == "__main__":
    main()
