#!/usr/bin/env python3
"""
cluster_repos.py
=================

Script para agrupar repositórios estrelados com base em suas
descrições usando TF‑IDF e KMeans. O objetivo é descobrir padrões
semânticos que não dependem de listas pré‑definidas de palavras‑chave.

Uso:

    python cluster_repos.py input.json output.csv

O resultado será um CSV com as colunas `Cluster`, `Cluster_terms`,
`Repositório`, `Descrição`, `Linguagem` e `URL`. Cada linha pertence
a um cluster e `Cluster_terms` contém as cinco palavras mais
representativas desse grupo.

Dependências: scikit‑learn, pandas.
"""

import sys
import json
import csv
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def load_texts(repos: List[dict]) -> List[str]:
    texts = []
    for repo in repos:
        name = repo.get('name') or ''
        desc = repo.get('description') or ''
        texts.append((name + ' ' + desc).lower())
    return texts


def perform_clustering(texts: List[str], n_clusters: int = 20):
    vectorizer = TfidfVectorizer(max_df=0.8, min_df=2, stop_words='english')
    X = vectorizer.fit_transform(texts)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    terms = vectorizer.get_feature_names_out()
    # Top terms for each cluster
    top_terms = {}
    for i in range(n_clusters):
        center = kmeans.cluster_centers_[i]
        top_indices = center.argsort()[-10:][::-1]
        top_terms[i] = [terms[idx] for idx in top_indices]
    return labels, top_terms


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python cluster_repos.py <input.json> <output.csv>")
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    with open(input_path, 'r', encoding='utf-8') as f:
        repos = json.load(f)
    texts = load_texts(repos)
    labels, top_terms = perform_clustering(texts)
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Cluster', 'Cluster_terms', 'Repositório', 'Descrição', 'Linguagem', 'URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo, label in zip(repos, labels):
            writer.writerow({
                'Cluster': label,
                'Cluster_terms': ', '.join(top_terms[label][:5]),
                'Repositório': repo.get('full_name'),
                'Descrição': repo.get('description') or '',
                'Linguagem': repo.get('language') or 'Unknown',
                'URL': repo.get('html_url'),
            })
    print(f"Clustering concluído: {len(repos)} registros gravados em {output_path}")


if __name__ == '__main__':
    main()