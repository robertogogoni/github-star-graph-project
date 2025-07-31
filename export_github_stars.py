#!/usr/bin/env python3
"""
Script para exportar todos os repositórios estrelados de um usuário do GitHub.

O script utiliza a API pública do GitHub, autenticada com um Personal Access Token (PAT)
fornecido via variável de ambiente `GITHUB_TOKEN`. Ele realiza chamadas paginadas
para o endpoint `https://api.github.com/users/<username>/starred` e compila todos
os resultados em uma única lista. Ao final, grava o JSON consolidado em um arquivo
``starred_repos.json`` no diretório corrente.

Uso:
  1. Defina a variável de ambiente ``GITHUB_TOKEN`` com o seu PAT antes de
     executar este script. No shell fish, você pode fazê-lo da seguinte forma:

         set -x GITHUB_TOKEN "seu_token"

     substituindo ``seu_token`` pelo valor do seu PAT.
  2. Execute o script:

         python3 export_github_stars.py

  3. Após a execução, um arquivo ``starred_repos.json`` será criado contendo
     todos os repositórios estrelados.
  4. Nunca compartilhe o seu PAT com terceiros ou inclua-o em arquivos de script.

Autor: Gerado por assistente.
"""

import json
import os
import sys
from typing import List, Dict

import requests


def fetch_starred_repositories(username: str, token: str) -> List[Dict]:
    """Recupera todos os repositórios estrelados para um usuário.

    Args:
        username: Nome de usuário do GitHub.
        token: Personal Access Token (PAT) para autenticação.

    Returns:
        Lista de dicionários representando cada repositório estrelado.
    """
    per_page = 100
    page = 1
    all_repos: List[Dict] = []
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    while True:
        url = f"https://api.github.com/users/{username}/starred"
        params = {"per_page": per_page, "page": page}
        response = requests.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            sys.stderr.write(f"Erro ao recuperar página {page}: {exc}\n")
            break
        repos = response.json()
        if not repos:
            break
        all_repos.extend(repos)
        page += 1

    return all_repos


def main():
    username = "robertogogoni"
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        sys.stderr.write(
            "Variável de ambiente GITHUB_TOKEN não definida. Defina-a com seu PAT antes de executar.\n"
        )
        sys.exit(1)

    starred_repos = fetch_starred_repositories(username, token)
    print(f"Repositórios estrelados encontrados: {len(starred_repos)}")
    out_file = "starred_repos.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(starred_repos, f, ensure_ascii=False, indent=2)
    print(f"Arquivo salvo: {out_file}")


if __name__ == "__main__":
    main()
