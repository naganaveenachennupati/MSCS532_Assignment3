"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Randomized Quicksort implementation.
The pivot is selected uniformly at random from the current subarray.
"""

import random


def randomized_quicksort(values, rng=None):
    """Sort the list in ascending order using Randomized Quicksort."""

    if rng is None:
        rng = random

    _randomized_quicksort(values, 0, len(values) - 1, rng)

    return values


def _randomized_quicksort(values, low, high, rng):
    """Recursively sort the portion of the list from low through high."""

    while low < high:
        split_index = randomized_partition(values, low, high, rng)

        left_size = split_index - low + 1
        right_size = high - split_index

        # Recurse on the smaller side first and continue sorting
        # the larger side in the loop. This limits recursion depth.
        if left_size < right_size:
            _randomized_quicksort(
                values,
                low,
                split_index,
                rng
            )
            low = split_index + 1

        else:
            _randomized_quicksort(
                values,
                split_index + 1,
                high,
                rng
            )
            high = split_index


def randomized_partition(values, low, high, rng):
    """Choose a random pivot and partition the current subarray."""

    pivot_index = rng.randint(low, high)

    # Hoare partitioning uses the first position as the pivot,
    # so move the randomly selected value there.
    values[low], values[pivot_index] = values[pivot_index], values[low]

    return hoare_partition(values, low, high)


def hoare_partition(values, low, high):
    """Partition the subarray using Hoare's partitioning method."""

    pivot_value = values[low]

    left = low - 1
    right = high + 1

    while True:
        left += 1
        while values[left] < pivot_value:
            left += 1

        right -= 1
        while values[right] > pivot_value:
            right -= 1

        if left >= right:
            return right

        values[left], values[right] = values[right], values[left]


def main():
    sample_values = [38, 27, 43, 3, 9, 82, 10, 27]

    print("Original values:")
    print(sample_values)

    randomized_quicksort(sample_values)

    print("\nValues after Randomized Quicksort:")
    print(sample_values)


if __name__ == "__main__":
    main()