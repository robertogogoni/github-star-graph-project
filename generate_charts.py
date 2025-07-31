"""Generate summary charts from the refined CSV.

This script reads the CSV produced by `classify_repos.py` (e.g.
`starred_repos_refined.csv`) and generates bar charts for the
distribution of repositories by domain, project type and language.

Usage:
    python generate_charts.py starred_repos_refined.csv output_dir

The charts will be saved as PNG files in the specified output
directory. If the directory does not exist it will be created.

Requires:
    pandas
    matplotlib
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_bar_chart(series, title, xlabel, ylabel, filepath):
    """Generate and save a horizontal bar chart."""
    counts = series.value_counts().sort_values(ascending=True)
    plt.figure(figsize=(10, max(4, len(counts) * 0.3)))
    counts.plot(kind="barh")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filepath)
    plt.close()


def main(csv_path: str, output_dir: str) -> None:
    if not os.path.isfile(csv_path):
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    # Domain distribution
    generate_bar_chart(
        df["Domain"],
        title="Distribution of Starred Repositories by Domain",
        xlabel="Number of Repositories",
        ylabel="Domain",
        filepath=os.path.join(output_dir, "domain_distribution.png"),
    )
    # Project Type distribution
    generate_bar_chart(
        df["Project Type"],
        title="Distribution by Project Type",
        xlabel="Number of Repositories",
        ylabel="Project Type",
        filepath=os.path.join(output_dir, "project_type_distribution.png"),
    )
    # Language distribution
    generate_bar_chart(
        df["Language"],
        title="Distribution by Programming Language",
        xlabel="Number of Repositories",
        ylabel="Language",
        filepath=os.path.join(output_dir, "language_distribution.png"),
    )
    print(f"Charts saved in {output_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_charts.py <refined_csv> <output_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])