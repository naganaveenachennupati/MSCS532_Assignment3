"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Automated tests for the hash table with separate chaining.
"""

import unittest

from hash_table_chaining import ChainedHashTable


class TestChainedHashTable(unittest.TestCase):
    """Test hash table operations, collisions, and resizing."""

    def test_insert_and_search(self):
        """Verify that inserted values can be retrieved."""

        table = ChainedHashTable()

        table.insert(10, "A")
        table.insert(20, "B")
        table.insert(30, "C")

        self.assertEqual(table.search(10), "A")
        self.assertEqual(table.search(20), "B")
        self.assertEqual(table.search(30), "C")
        self.assertEqual(table.size, 3)
        self.assertEqual(len(table), 3)

    def test_update_existing_key(self):
        """Updating a key should replace its value without increasing size."""

        table = ChainedHashTable()

        table.insert(10, "Old")
        table.insert(10, "New")

        self.assertEqual(table.search(10), "New")
        self.assertEqual(table.size, 1)

    def test_delete_existing_and_missing_keys(self):
        """Verify deletion behavior for existing and missing keys."""

        table = ChainedHashTable()

        table.insert(10, "A")
        table.insert(20, "B")

        self.assertTrue(table.delete(10))
        self.assertIsNone(table.search(10))
        self.assertEqual(table.size, 1)

        self.assertFalse(table.delete(999))
        self.assertEqual(table.size, 1)

    def test_empty_table(self):
        """Search and delete should work safely on an empty table."""

        table = ChainedHashTable()

        self.assertIsNone(table.search(10))
        self.assertFalse(table.delete(10))
        self.assertEqual(table.size, 0)
        self.assertEqual(table.load_factor, 0)

    def test_zero_and_negative_keys(self):
        """Verify that zero and negative integer keys are supported."""

        table = ChainedHashTable()

        table.insert(0, "zero")
        table.insert(-25, "negative")

        self.assertEqual(table.search(0), "zero")
        self.assertEqual(table.search(-25), "negative")

    def test_collision_handling(self):
        """Verify that two colliding keys remain accessible in one chain."""

        table = ChainedHashTable(
            initial_capacity=8,
            max_load_factor=0.99
        )

        seen_buckets = {}
        first_key = None
        second_key = None

        # Find two keys that map to the same bucket.
        for key in range(100):
            bucket_index = table._hash(key)

            if bucket_index in seen_buckets:
                first_key = seen_buckets[bucket_index]
                second_key = key
                break

            seen_buckets[bucket_index] = key

        self.assertIsNotNone(first_key)
        self.assertIsNotNone(second_key)
        self.assertEqual(
            table._hash(first_key),
            table._hash(second_key)
        )

        table.insert(first_key, "first")
        table.insert(second_key, "second")

        self.assertEqual(table.search(first_key), "first")
        self.assertEqual(table.search(second_key), "second")
        self.assertEqual(table.size, 2)

    def test_dynamic_resizing(self):
        """Verify resizing preserves all stored key-value pairs."""

        table = ChainedHashTable(initial_capacity=4)

        original_capacity = table.capacity

        for key in range(100):
            table.insert(key, key * 10)

        self.assertGreater(table.capacity, original_capacity)
        self.assertEqual(table.size, 100)
        self.assertLessEqual(
            table.load_factor,
            table._max_load_factor
        )

        for key in range(100):
            self.assertEqual(table.search(key), key * 10)

    def test_load_factor(self):
        """Verify that the reported load factor is n divided by m."""

        table = ChainedHashTable(initial_capacity=8)

        table.insert(10, "A")
        table.insert(20, "B")
        table.insert(30, "C")

        self.assertAlmostEqual(table.load_factor, 3 / 8)

    def test_invalid_constructor_values(self):
        """Verify invalid table settings are rejected."""

        with self.assertRaises(ValueError):
            ChainedHashTable(initial_capacity=0)

        with self.assertRaises(ValueError):
            ChainedHashTable(initial_capacity=-5)

        with self.assertRaises(ValueError):
            ChainedHashTable(max_load_factor=0)

        with self.assertRaises(ValueError):
            ChainedHashTable(max_load_factor=1)

        with self.assertRaises(ValueError):
            ChainedHashTable(max_load_factor=1.5)

    def test_invalid_key_types(self):
        """Verify non-integer keys are rejected."""

        table = ChainedHashTable()

        with self.assertRaises(TypeError):
            table.insert("abc", 123)

        with self.assertRaises(TypeError):
            table.search("abc")

        with self.assertRaises(TypeError):
            table.delete("abc")

    def test_many_insertions_and_deletions(self):
        """Verify consistency across a larger sequence of operations."""

        table = ChainedHashTable(initial_capacity=4)

        for key in range(500):
            table.insert(key, key + 1000)

        self.assertEqual(table.size, 500)

        for key in range(0, 500, 2):
            self.assertTrue(table.delete(key))

        self.assertEqual(table.size, 250)

        for key in range(500):
            if key % 2 == 0:
                self.assertIsNone(table.search(key))
            else:
                self.assertEqual(
                    table.search(key),
                    key + 1000
                )


if __name__ == "__main__":
    unittest.main()