"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Creates performance graphs from the Quicksort benchmark results.
"""

import csv
from pathlib import Path

import matplotlib.pyplot as plt


RESULTS_FILE = Path("results/quicksort_results.csv")
RESULTS_FOLDER = Path("results")

DATASET_TYPES = [
    "Random",
    "Sorted",
    "Reverse Sorted",
    "Repeated Elements",
]

ALGORITHMS = [
    "Randomized Quicksort",
    "Deterministic Quicksort",
]


def load_results():
    """Load benchmark measurements from the CSV file."""

    results = []

    with RESULTS_FILE.open(
        "r",
        encoding="utf-8"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            results.append(
                {
                    "Algorithm": row["Algorithm"],
                    "Dataset Type": row["Dataset Type"],
                    "Input Size": int(row["Input Size"]),
                    "Average Time (ms)": float(
                        row["Average Time (ms)"]
                    ),
                    "Std Dev (ms)": float(
                        row["Std Dev (ms)"]
                    ),
                }
            )

    return results


def create_graph(results, dataset_type, filename):
    """Create one comparison graph for a dataset distribution."""

    plt.figure(figsize=(8, 5))

    for algorithm in ALGORITHMS:
        selected = [
            row
            for row in results
            if row["Algorithm"] == algorithm
            and row["Dataset Type"] == dataset_type
        ]

        selected.sort(
            key=lambda row: row["Input Size"]
        )

        sizes = [
            row["Input Size"]
            for row in selected
        ]

        times = [
            row["Average Time (ms)"]
            for row in selected
        ]

        deviations = [
            row["Std Dev (ms)"]
            for row in selected
        ]

        plt.errorbar(
            sizes,
            times,
            yerr=deviations,
            marker="o",
            capsize=3,
            label=algorithm,
        )

    plt.title(
        f"Quicksort Performance - {dataset_type}"
    )
    plt.xlabel("Input Size")
    plt.ylabel("Average Execution Time (ms)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    output_file = RESULTS_FOLDER / filename
    plt.savefig(output_file, dpi=300)
    plt.close()


def main():
    """Generate all Quicksort comparison graphs."""

    RESULTS_FOLDER.mkdir(exist_ok=True)

    results = load_results()

    graph_files = {
        "Random": "random_comparison.png",
        "Sorted": "sorted_comparison.png",
        "Reverse Sorted": "reverse_sorted_comparison.png",
        "Repeated Elements": "repeated_comparison.png",
    }

    for dataset_type, filename in graph_files.items():
        create_graph(
            results,
            dataset_type,
            filename
        )

        print(
            f"Created: results/{filename}"
        )

    print("\nAll performance graphs created successfully.")


if __name__ == "__main__":
    main()