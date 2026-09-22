"""
MSCS 532 - Assignment 3
Naga Naveena Chennupati

Hash table implementation using separate chaining for collision resolution.
The table uses a universal-style hash function for integer keys and
automatically resizes when the load factor becomes too high.
"""

import random


class ChainedHashTable:
    """Hash table with separate chaining and dynamic resizing."""

    # Large prime used by the universal hash function.
    PRIME = 2**61 - 1

    def __init__(
        self,
        initial_capacity=8,
        max_load_factor=0.75,
        seed=532
    ):
        """Create an empty hash table."""

        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be greater than zero")

        if not 0 < max_load_factor < 1:
            raise ValueError("max_load_factor must be between 0 and 1")

        self._capacity = initial_capacity
        self._max_load_factor = max_load_factor
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]

        # Select parameters for the universal hash function.
        rng = random.Random(seed)
        self._a = rng.randrange(1, self.PRIME)
        self._b = rng.randrange(0, self.PRIME)

    @property
    def size(self):
        """Return the number of key-value pairs stored in the table."""

        return self._size

    @property
    def capacity(self):
        """Return the current number of buckets."""

        return self._capacity

    @property
    def load_factor(self):
        """Return the current load factor, alpha = n / m."""

        return self._size / self._capacity

    def _validate_key(self, key):
        """Require integer keys for the universal hash function."""

        if not isinstance(key, int):
            raise TypeError("Hash table keys must be integers")

    def _hash(self, key):
        """Return the bucket index for an integer key."""

        normalized_key = key % self.PRIME

        return (
            (
                self._a * normalized_key
                + self._b
            )
            % self.PRIME
        ) % self._capacity

    def insert(self, key, value):
        """Insert a new key-value pair or update an existing key."""

        self._validate_key(key)

        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        # Update the value if the key already exists.
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[index] = (key, value)
                return

        # Resize before inserting a new key if the next insertion
        # would push the load factor above the chosen threshold.
        projected_load = (self._size + 1) / self._capacity

        if projected_load > self._max_load_factor:
            self._resize(self._capacity * 2)
            bucket_index = self._hash(key)
            bucket = self._buckets[bucket_index]

        bucket.append((key, value))
        self._size += 1

    def search(self, key):
        """Return the value associated with key, or None if not found."""

        self._validate_key(key)

        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        for stored_key, value in bucket:
            if stored_key == key:
                return value

        return None

    def delete(self, key):
        """Delete key from the table and return True if it was found."""

        self._validate_key(key)

        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]

        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[index]
                self._size -= 1
                return True

        return False

    def _resize(self, new_capacity):
        """Resize the table and rehash all existing key-value pairs."""

        old_buckets = self._buckets

        self._capacity = new_capacity
        self._buckets = [[] for _ in range(self._capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                new_index = self._hash(key)
                self._buckets[new_index].append((key, value))

    def __len__(self):
        """Return the number of stored key-value pairs."""

        return self._size


def main():
    table = ChainedHashTable(initial_capacity=4)

    table.insert(101, "Alice")
    table.insert(205, "Bob")
    table.insert(309, "Carol")

    print("Stored entries:", len(table))
    print("Current capacity:", table.capacity)
    print(f"Load factor: {table.load_factor:.2f}")

    print("\nSearch for key 205:")
    print(table.search(205))

    table.insert(205, "Robert")

    print("\nUpdated value for key 205:")
    print(table.search(205))

    print("\nDelete key 101:")
    print(table.delete(101))

    print("Search for deleted key 101:")
    print(table.search(101))


if __name__ == "__main__":
    main()