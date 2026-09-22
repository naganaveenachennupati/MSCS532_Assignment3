"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Tests for the Randomized Quicksort and Deterministic Quicksort implementations.
"""

import random
import unittest

from deterministic_quicksort import deterministic_quicksort
from randomized_quicksort import randomized_quicksort


class TestQuicksortAlgorithms(unittest.TestCase):
    """Test both Quicksort implementations on different input conditions."""

    def setUp(self):
        self.test_cases = {
            "empty": [],
            "single element": [10],
            "two elements": [5, 2],
            "already sorted": [1, 2, 3, 4, 5],
            "reverse sorted": [5, 4, 3, 2, 1],
            "repeated values": [4, 2, 4, 1, 2, 4, 2],
            "all equal": [7, 7, 7, 7, 7],
            "negative values": [-3, 7, 0, -1, 5],
            "mixed values": [38, 27, 43, 3, 9, 82, 10, 27],
        }

    def test_deterministic_quicksort(self):
        """Verify Deterministic Quicksort on all standard test cases."""

        for name, values in self.test_cases.items():
            with self.subTest(case=name):
                data = values.copy()
                result = deterministic_quicksort(data)

                self.assertEqual(result, sorted(values))
                self.assertIs(result, data)

    def test_randomized_quicksort(self):
        """Verify Randomized Quicksort on all standard test cases."""

        rng = random.Random(532)

        for name, values in self.test_cases.items():
            with self.subTest(case=name):
                data = values.copy()
                result = randomized_quicksort(data, rng)

                self.assertEqual(result, sorted(values))
                self.assertIs(result, data)

    def test_randomized_quicksort_with_multiple_seeds(self):
        """Verify that different random pivot choices still sort correctly."""

        values = [12, 4, 18, 7, 3, 15, 9, 1, 11, 6]

        for seed in range(10):
            with self.subTest(seed=seed):
                data = values.copy()
                rng = random.Random(seed)

                randomized_quicksort(data, rng)

                self.assertEqual(data, sorted(values))

    def test_larger_inputs(self):
        """Verify both algorithms on larger datasets."""

        rng = random.Random(532)
        random_values = rng.sample(range(10000), 1000)

        datasets = [
            list(range(1000)),
            list(range(1000, 0, -1)),
            random_values,
            [value % 20 for value in range(1000)],
        ]

        for values in datasets:
            expected = sorted(values)

            deterministic_data = values.copy()
            deterministic_quicksort(deterministic_data)
            self.assertEqual(deterministic_data, expected)

            randomized_data = values.copy()
            randomized_quicksort(
                randomized_data,
                random.Random(532)
            )
            self.assertEqual(randomized_data, expected)


if __name__ == "__main__":
    unittest.main()