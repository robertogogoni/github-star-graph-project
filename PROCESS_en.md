# Tinkering Process

This document serves as a logbook for the project, recording decisions, attempts, missteps and learnings throughout the development of a graph‑visualisation application for starred repositories.

## 1. Exporting Starred Repositories

* **Tool used:** the Python script `export_github_stars.py`.
* **Motivation:** the available GitHub connector in the runtime environment did not offer an endpoint to list stars.  We therefore used the GitHub public API with pagination (`/users/{user}/starred`) and a PAT provided by the user.
* **Result:** obtained a JSON file with ~4,465 repositories.

## 2. Initial Classification

* **Goal:** quickly categorise the repositories by primary language, theme and project type using heuristics.
* **Method:** defined keyword dictionaries to map descriptions and names to large categories (e.g. `Android`, `Web`, `DevOps`).  We also identified whether the project was a library, framework, CLI, etc.
* **Learning:** this approach provided a general view but left many projects in the “Other” category and did not capture sub‑themes.

## 3. Refinement of Categories

* **Improvements:** expanded keyword lists for domains (e.g. `Data & AI`, `Security & Crypto`) and types (library, template, dataset).  Included subdomains such as `React`, `Docker`, `Kubernetes`.
* **Result:** generated the file `starred_repos_refined.csv` with the columns `Domain`, `Project Type`, `Subdomain`, providing a more granular view.

## 4. Semantic Clustering

* **Goal:** discover natural groupings in the data without relying on predefined keyword lists.
* **Method:** used TF‑IDF for vectorisation of the descriptions and `KMeans` (20 clusters) to group the projects.  Identified dominant keywords in each cluster to label them.
* **Result:** the file `starred_repos_clusters.csv` associates each repository with a cluster and lists the most common words in the group.
* **Observations:** clusters revealed interesting communities such as design tools, API wrappers, “awesome” lists and productivity utilities.

## 5. Enrichment with Topics (to be run locally)

* **Challenge:** the API endpoint for repository topics (`/topics`) is not directly accessible in the current execution environment.  The script `fetch_repo_topics.py` was prepared to be run locally, adding the list of `topics` to each record.
* **Next steps:** once the JSON is enriched, the classification can use these labels for even more accurate categorisation.

## 6. Future Evolutions

1. **Connection Graph**: model relationships between repositories (sharing topics, dependencies or high similarity) and build a graph in Neo4j or as a JSON file for visualisation.
2. **Integration with Trending Repositories**: collect trending projects regularly and integrate them into the graph to identify connections with your current stars.
3. **Automation**: configure GitHub Actions to run the scripts periodically and keep the visualisation always up to date.

This process is iterative; new ideas and improvements should be recorded here as they are implemented.