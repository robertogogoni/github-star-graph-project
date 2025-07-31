#!/usr/bin/env python3
"""
Fetch topics for each repository in a list of starred repositories.

This script takes a JSON file containing a list of repositories (as
returned by GitHub's starred API) and retrieves topics for each
repository using the GitHub API. It requires a Personal Access Token
(PAT) with public_repo scope, provided via the GITHUB_TOKEN environment
variable.

Usage:
  set -x GITHUB_TOKEN "<your_token>"  # in fish shell
  python3 fetch_repo_topics.py input.json output.json

The script reads the input JSON, adds a `topics` field to each
repository record (list of strings), writes the enriched list to the
output JSON, and prints progress.
"""
import os
import sys
import json
import time
import requests

TOPIC_ENDPOINT_TEMPLATE = "https://api.github.com/repos/{full_name}/topics"
ACCEPT_HEADER = "application/vnd.github.mercy-preview+json"


def fetch_topics(full_name: str, token: str) -> list:
    url = TOPIC_ENDPOINT_TEMPLATE.format(full_name=full_name)
    headers = {"Authorization": f"token {token}", "Accept": ACCEPT_HEADER}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("names", [])
    else:
        print(f"Falha ao obter tópicos de {full_name}: {resp.status_code}")
        return []


def main(input_path: str, output_path: str) -> None:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("Defina a variável GITHUB_TOKEN com seu PAT.")
    with open(input_path, "r", encoding="utf-8") as f:
        repos = json.load(f)
    enriched = []
    total = len(repos)
    for idx, repo in enumerate(repos, 1):
        full_name = repo.get("full_name")
        topics = fetch_topics(full_name, token)
        repo["topics"] = topics
        enriched.append(repo)
        if idx % 10 == 0 or idx == total:
            print(f"{idx}/{total} repositórios processados")
        # Sleep to avoid hitting rate limits
        time.sleep(1)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print(f"Arquivo salvo com tópicos: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python fetch_repo_topics.py input.json output.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
