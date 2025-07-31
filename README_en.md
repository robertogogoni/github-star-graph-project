# GitHub Star Graph

This project provides a complete guide to transform your list of starred repositories into **interactive visualizations** and **actionable insights**.  The idea is to start small—by extracting and classifying your favourite repositories—and gradually evolve towards a sophisticated solution that includes intelligent enrichment, similarity graphs, integration with trending repositories and automated updates.  Everything is documented so you can follow the reasoning, choices and results along the way.

## Goals

The repository has these main goals:

* **Centralize scripts and tools** for collecting, enriching and classifying your starred repositories and also querying trending projects.
* **Record the tinkering process**: every step, hypothesis and adjustment is described in `docs/PROCESS.md` so that other people (and you in the future) can understand how decisions were made.
* **Enable incremental evolution**: you can add new features (e.g. topic collection, semantic clustering, graph modelling) without losing context, because the project is organised into well‑defined modules and steps.
* **Encourage best practices**: the README follows recommended conventions, clearly explains how to use the scripts and warns about security concerns such as token usage.

## Minimum Viable Version (MVP)

The starting point is to obtain basic data about the repositories you starred and classify them by language, domain and type.  This provides an overview of your technical profile and helps plan the later visualisation.  At this stage you only need an access token with public read permission (`public_repo`).

The main scripts are:

1. `scripts/export_github_stars.py` – Exports all repositories you have starred.  It reads your personal access token (PAT) from the `GITHUB_TOKEN` environment variable and writes a file `starred_repos.json` containing basic details about each repository.
2. `scripts/classify_repos.py` – Takes the exported JSON and generates a CSV file with columns `Domain`, `Project Type`, `Subdomain`, `Language`, `Repository`, `Description` and `URL`.  The classification uses extended keyword lists to map each repository to technical and business categories.

### Running the MVP

1. **Create an isolated Python environment (optional)**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install the dependencies** listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set the `GITHUB_TOKEN` environment variable** with your PAT (example for fish shell):

   ```fish
   set -x GITHUB_TOKEN "your_token"
   ```

4. **Run the export script** to download all repositories you starred:

   ```bash
   python scripts/export_github_stars.py
   ```

5. **Classify the repositories** using extended keyword lists to identify domain, type and subdomain:

   ```bash
   python scripts/classify_repos.py starred_repos.json starred_repos_refined.csv
   ```

6. **Analyse the results**: open the generated CSV in a spreadsheet (Excel, LibreOffice or Google Sheets) and explore the `Domain`, `Project Type`, `Subdomain`, `Language` columns, etc.

## Planned Evolution

With the MVP in place, you can advance in incremental steps.  Some suggestions:

1. **Enrich with topics** – The script `scripts/fetch_repo_topics.py` queries the GitHub API to obtain tags assigned by maintainers.  These metadata help refine categories and identify relationships between projects.
2. **Apply semantic clustering** – `scripts/cluster_repos.py` uses TF‑IDF and KMeans to group similar descriptions.  This reveals hidden patterns and lays a foundation for proximity‑based visualisations.
3. **Model the graph** – Convert repositories, topics and similarity relations into a graph (JSON or CSV).  This structure can be imported into a graph database (Neo4j) or consumed by visualisation libraries such as D3.js or Cytoscape.js.
4. **Integrate with trending** – Add a module to collect trending repositories and connect them to your starred repositories by language, topics or shared dependencies.
5. **Automate and publish** – Configure GitHub Actions to run these scripts daily or weekly.  Use GitHub Pages or another service to host the updated interactive visualisation.
6. **Apply advanced AI** – Explore embeddings with `sentence-transformers` or AI APIs to compute contextual similarity, recommendations and automatic summarisations.

## Repository Structure

* `scripts/` – Contains the Python scripts used in the collection, enrichment, classification and clustering steps.
* `docs/` – Documentation files, including the tinkering process (`PROCESS.md`).
* `requirements.txt` – List of Python dependencies.
* `.github/workflows/` – (Optional) Contains automation configurations via GitHub Actions for continuous updates.

## Requirements

* **Python 3.8 or higher** – The scripts use features from recent Python versions.
* **Internet access** – Needed for GitHub API calls and, eventually, to download trending files or dependencies.
* **Personal Access Token (PAT)** – The token should have the minimum public repository read scope (`public_repo`).  Never commit your key into the repository; keep it in an environment variable.

## Contributing

This project encourages an experimental mindset ("tinkering").  Suggestions for collaboration:

* **Thematic branches** – Create specific branches for each improvement (e.g. `feature/clustering`, `feature/trending`, `ci/automation`).  This keeps the history organised.
* **Clear commit messages** – Explain why each change was made.  This helps reconstruct the reasoning.
* **Update the documentation** – Whenever you experiment with something new, record in `docs/PROCESS.md` what was done, what worked and what can be improved.
* **Take care of security** – Never expose tokens or credentials.  Use environment variables and `.env` files ignored by git.