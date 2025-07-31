#!/usr/bin/env python3
"""
classify_repos.py
===================

Script que lê um arquivo JSON contendo repositórios estrelados (no
formato retornado pela API do GitHub) e produz um CSV com
classificações por domínio, tipo de projeto e subdomínio.

O objetivo é oferecer uma visão inicial estruturada do universo
de repositórios, agrupando‑os em áreas técnicas (Web, Mobile,
Data & AI etc.) e em tipos (biblioteca, framework, aplicação,
CLI/Tool, template, plugin, dataset, configuração, exemplos).

Uso:

    python classify_repos.py input.json output.csv

O script não depende de chamadas externas e pode ser executado
diretamente após exportar seus repositórios com
`export_github_stars.py`.
"""

import sys
import json
import csv
from typing import Dict, List


DOMAIN_KEYWORDS: Dict[str, List[str]] = {
    'Web': ['web', 'browser', 'http', 'https', 'html', 'css', 'javascript', 'react', 'vue', 'angular', 'frontend', 'backend', 'server', 'django', 'flask', 'api', 'rest', 'graphql', 'express', 'nextjs', 'nuxt', 'svelte'],
    'Mobile': ['android', 'ios', 'flutter', 'react native', 'kotlin', 'swift', 'mobile', 'xamarin', 'android tv', 'cordova'],
    'Data & AI': ['machine learning', 'deep learning', 'ml', 'ai ', ' artificial', 'data ', 'dataset', 'nlp', 'vision', 'model', 'training', 'neural', 'pytorch', 'tensorflow', 'keras', 'xgboost', 'scikit', 'huggingface'],
    'DevOps & Cloud': ['devops', 'docker', 'container', 'kubernetes', 'helm', 'terraform', 'ansible', 'ci', 'cd', 'pipeline', 'jenkins', 'github actions', 'gitlab', 'ci/cd', 'aws', 'azure', 'gcp', 'cloud', 'infrastructure', 'deployment'],
    'Systems & Networking': ['kernel', 'linux', 'driver', 'network', 'tcp', 'udp', 'socket', 'proxy', 'vpn', 'firewall', 'embedded', 'firmware', 'operating system', 'serial'],
    'Productivity & Tools': ['cli', 'command line', 'script', 'tool', 'automation', 'productivity', 'workflow', 'testing', 'formatter', 'lint', 'utility', 'editor', 'plugin', 'extension', 'generator', 'packager'],
    'Games & Multimedia': ['game', 'gaming', 'engine', 'unity', 'unreal', 'graphics', 'render', 'audio', 'video', 'media', 'animation'],
    'Security & Crypto': ['security', 'crypto', 'cryptography', 'blockchain', 'wallet', 'encryption', 'decryption', 'auth', 'authentication', 'authorization', 'jwt', 'tls', 'ssl', 'pentest', 'hacking'],
    'Finance & Business': ['finance', 'trading', 'stock', 'forex', 'cryptocurrency', 'market', 'investment', 'portfolio', 'business', 'billing', 'payment'],
}

TYPE_KEYWORDS: Dict[str, List[str]] = {
    'Framework': ['framework'],
    'Library': ['library', 'lib', 'sdk', 'package', 'module'],
    'Application': ['application', 'app', 'project'],
    'CLI/Tool': ['cli', 'command line', 'tool', 'script', 'utility'],
    'Template': ['template', 'starter', 'boilerplate', 'seed'],
    'Plugin/Extension': ['plugin', 'extension'],
    'Dataset': ['dataset', 'data set', 'collection'],
    'Configuration': ['config', 'dotfile', 'configuration'],
    'Examples': ['example', 'sample'],
}

SUBDOMAIN_KEYWORDS: Dict[str, List[str]] = {
    'React': ['react', 'reactjs', 'react.js'],
    'Vue': ['vue', 'vuejs', 'vue.js'],
    'Angular': ['angular'],
    'Node.js': ['node.js', 'nodejs', 'node '],
    'Express': ['express'],
    'Next.js': ['next.js', 'nextjs'],
    'Django': ['django'],
    'Flask': ['flask'],
    'FastAPI': ['fastapi'],
    'Spring': ['spring', 'spring boot'],
    'Kotlin': ['kotlin'],
    'Swift': ['swift'],
    'Flutter': ['flutter'],
    'PyTorch': ['pytorch'],
    'TensorFlow': ['tensorflow'],
    'Keras': ['keras'],
    'Kubernetes': ['kubernetes'],
    'Docker': ['docker'],
    'Terraform': ['terraform'],
    'Ansible': ['ansible'],
    'Helm': ['helm'],
    'Jenkins': ['jenkins'],
    'GitHub Actions': ['github actions'],
    'AWS': ['aws', 'amazon web services'],
    'Azure': ['azure'],
    'GCP': ['gcp', 'google cloud'],
    'Unity': ['unity'],
    'Unreal': ['unreal'],
    'Blockchain': ['blockchain'],
    'Cryptocurrency': ['crypto', 'cryptocurrency'],
}


def find_category(text: str, mapping: Dict[str, List[str]], default: str = 'Other') -> str:
    """Retorna a primeira categoria cujo termo exista no texto."""
    for category, keywords in mapping.items():
        for kw in keywords:
            if kw in text:
                return category
    return default


def classify_repositories(repos: List[dict]) -> List[dict]:
    classified = []
    for repo in repos:
        name = repo.get('name') or ''
        full_name = repo.get('full_name') or ''
        description = (repo.get('description') or '').lower()
        language = repo.get('language') or 'Unknown'
        url = repo.get('html_url')
        text = f"{name} {full_name} {description}"
        domain = find_category(text, DOMAIN_KEYWORDS, default='Other')
        project_type = find_category(text, TYPE_KEYWORDS, default='Other')
        subdomain = find_category(text, SUBDOMAIN_KEYWORDS, default=domain)
        classified.append({
            'Área de Domínio': domain,
            'Tipo de Projeto': project_type,
            'Subdomínio': subdomain,
            'Linguagem': language,
            'Repositório': full_name,
            'Descrição': repo.get('description') or '',
            'URL': url,
        })
    return classified


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python classify_repos.py <input.json> <output.csv>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    with open(input_path, 'r', encoding='utf-8') as f:
        repos = json.load(f)
    classified = classify_repositories(repos)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Área de Domínio', 'Tipo de Projeto', 'Subdomínio',
            'Linguagem', 'Repositório', 'Descrição', 'URL'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in classified:
            writer.writerow(row)
    print(f"Classificação concluída: {len(classified)} registros gravados em {output_path}")


if __name__ == '__main__':
    main()