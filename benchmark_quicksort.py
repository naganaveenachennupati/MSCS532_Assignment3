"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Empirical comparison of Randomized Quicksort and
Deterministic Quicksort using several input distributions.
"""

import csv
import random
import statistics
import time
from pathlib import Path

from deterministic_quicksort import deterministic_quicksort
from randomized_quicksort import randomized_quicksort


# Input sizes used for the empirical comparison.
INPUT_SIZES = [100, 500, 1000, 2000, 5000]

# Each timing measurement is repeated several times.
TIMING_TRIALS = 5

# Fixed seeds make the experiment reproducible.
DATASET_SEED = 532
PIVOT_SEED = 1532

RESULTS_FILE = Path("results/quicksort_results.csv")

DATASET_OFFSETS = {
    "Random": 100,
    "Sorted": 200,
    "Reverse Sorted": 300,
    "Repeated Elements": 400,
}


def create_datasets(size):
    """Create the four input distributions required for the experiment."""

    rng = random.Random(DATASET_SEED + size)

    random_data = rng.sample(
        range(size * 10),
        size
    )

    sorted_data = list(range(size))

    reverse_sorted_data = list(
        range(size, 0, -1)
    )

    # Use a smaller value range so that many elements repeat.
    repeated_value_range = max(5, size // 20)

    repeated_data = [
        rng.randrange(repeated_value_range)
        for _ in range(size)
    ]

    return {
        "Random": random_data,
        "Sorted": sorted_data,
        "Reverse Sorted": reverse_sorted_data,
        "Repeated Elements": repeated_data,
    }


def run_algorithm(
    algorithm_name,
    data,
    pivot_seed
):
    """Run one of the two Quicksort implementations."""

    if algorithm_name == "Randomized Quicksort":
        rng = random.Random(pivot_seed)
        randomized_quicksort(data, rng)
    else:
        deterministic_quicksort(data)

    return data


def measure_execution_time(
    algorithm_name,
    dataset_type,
    original_data,
    size
):
    """Measure execution time across several independent trials."""

    expected = sorted(original_data)
    times_ms = []

    for trial in range(TIMING_TRIALS):
        # Copy the data before starting the timer so that
        # list-copying time is not counted as sorting time.
        data = original_data.copy()

        pivot_seed = (
            PIVOT_SEED
            + DATASET_OFFSETS[dataset_type]
            + size
            + trial
        )

        start_time = time.perf_counter()

        result = run_algorithm(
            algorithm_name,
            data,
            pivot_seed
        )

        end_time = time.perf_counter()

        # Every timed run must still produce a correct result.
        assert result == expected

        elapsed_ms = (
            end_time - start_time
        ) * 1000

        times_ms.append(elapsed_ms)

    average_time = statistics.mean(times_ms)

    standard_deviation = (
        statistics.stdev(times_ms)
        if len(times_ms) > 1
        else 0.0
    )

    return average_time, standard_deviation


def save_results(results):
    """Write all benchmark measurements to a CSV file."""

    RESULTS_FILE.parent.mkdir(exist_ok=True)

    fieldnames = [
        "Algorithm",
        "Dataset Type",
        "Input Size",
        "Average Time (ms)",
        "Std Dev (ms)",
    ]

    with RESULTS_FILE.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)


def run_benchmarks():
    """Run the complete Quicksort performance experiment."""

    algorithms = [
        "Randomized Quicksort",
        "Deterministic Quicksort",
    ]

    results = []

    print("Starting Quicksort performance comparison...\n")

    for size in INPUT_SIZES:
        datasets = create_datasets(size)

        for dataset_type, dataset in datasets.items():
            for algorithm_name in algorithms:
                average_time, standard_deviation = (
                    measure_execution_time(
                        algorithm_name,
                        dataset_type,
                        dataset,
                        size
                    )
                )

                result_row = {
                    "Algorithm": algorithm_name,
                    "Dataset Type": dataset_type,
                    "Input Size": size,
                    "Average Time (ms)": round(
                        average_time,
                        4
                    ),
                    "Std Dev (ms)": round(
                        standard_deviation,
                        4
                    ),
                }

                results.append(result_row)

                print(
                    f"{algorithm_name:24} | "
                    f"{dataset_type:17} | "
                    f"n={size:<5} | "
                    f"Avg={average_time:10.4f} ms | "
                    f"SD={standard_deviation:9.4f} ms"
                )

        print()

    save_results(results)

    print("Benchmark completed successfully.")
    print(
        "Results saved to "
        "results/quicksort_results.csv"
    )


if __name__ == "__main__":
    run_benchmarks()