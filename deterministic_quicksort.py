"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Deterministic Quicksort implementation.
The first element of each subarray is used as the pivot.
"""


def deterministic_quicksort(values):
    """Sort the list in ascending order using Deterministic Quicksort."""

    _deterministic_quicksort(values, 0, len(values) - 1)

    return values


def _deterministic_quicksort(values, low, high):
    """Sort the portion of the list from low through high."""

    while low < high:
        split_index = hoare_partition(values, low, high)

        left_size = split_index - low + 1
        right_size = high - split_index

        # Recurse on the smaller side first and continue sorting
        # the larger side in the loop to limit recursion depth.
        if left_size < right_size:
            _deterministic_quicksort(
                values,
                low,
                split_index
            )
            low = split_index + 1

        else:
            _deterministic_quicksort(
                values,
                split_index + 1,
                high
            )
            high = split_index


def hoare_partition(values, low, high):
    """Partition the subarray using its first element as the pivot."""

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

    deterministic_quicksort(sample_values)

    print("\nValues after Deterministic Quicksort:")
    print(sample_values)


if __name__ == "__main__":
    main()