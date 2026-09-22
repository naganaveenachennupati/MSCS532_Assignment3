# MSCS 532 - Assignment 3

## Understanding Algorithm Efficiency and Scalability

**Student:** Naga Naveena Chennupati  
**Course:** MSCS 532 - Algorithms and Data Structures  
**University:** University of the Cumberlands  

## Overview

This project examines algorithm efficiency and scalability through two topics: Randomized Quicksort and hashing with separate chaining.

For the Quicksort portion, I implemented a randomized version that selects a pivot uniformly from the current subarray and a deterministic version that always uses the first element as the pivot. I compared both algorithms on random, sorted, reverse-sorted, and repeated-element datasets.

For the hashing portion, I implemented a hash table with separate chaining, a universal-style hash function for integer keys, dynamic resizing, and support for insert, search, and delete operations.

## Project Files

- `randomized_quicksort.py` - Randomized Quicksort implementation
- `deterministic_quicksort.py` - First-pivot Deterministic Quicksort implementation
- `hash_table_chaining.py` - Hash table with separate chaining and dynamic resizing
- `test_quicksort.py` - Automated tests for both Quicksort implementations
- `test_hash_table.py` - Automated tests for the hash table
- `benchmark_quicksort.py` - Performance comparison for the two Quicksort algorithms
- `generate_graphs.py` - Generates performance graphs from the benchmark results
- `requirements.txt` - Python package requirement for graph generation
- `results/quicksort_results.csv` - Complete benchmark results
- `results/random_comparison.png` - Random-input performance graph
- `results/sorted_comparison.png` - Sorted-input performance graph
- `results/reverse_sorted_comparison.png` - Reverse-sorted performance graph
- `results/repeated_comparison.png` - Repeated-element performance graph

## Randomized Quicksort

The randomized implementation chooses the pivot uniformly at random from the current subarray. It then uses Hoare partitioning to divide the data before recursively sorting the resulting partitions.

Randomization reduces dependence on the original ordering of the input. Although the theoretical worst case remains quadratic, the expected running time is Θ(n log n).

## Deterministic Quicksort

The deterministic implementation always uses the first element of the current subarray as the pivot. The remaining partitioning logic is kept comparable to the randomized implementation so that pivot selection is the main experimental difference.

This strategy works well for many unsorted inputs, but sorted and reverse-sorted data can repeatedly create highly unbalanced partitions and lead to Θ(n²) behavior.

## Empirical Comparison

The algorithms were tested with input sizes:

- 100
- 500
- 1,000
- 2,000
- 5,000

Four input distributions were tested:

- Random
- Sorted
- Reverse Sorted
- Repeated Elements

Each timing measurement was repeated five times. The benchmark reports the average execution time and standard deviation. Input copying was performed before starting the timer so that preparation time was not counted as part of sorting.

The experiment used fixed random seeds so that datasets and randomized pivot selections could be reproduced.

### Selected Results at n = 5,000

| Dataset | Randomized Quicksort | Deterministic Quicksort |
|---|---:|---:|
| Random | 8.7365 ms | 6.4698 ms |
| Sorted | 7.6334 ms | 495.0036 ms |
| Reverse Sorted | 8.0949 ms | 530.1679 ms |
| Repeated Elements | 8.7254 ms | 6.6118 ms |

The largest difference occurred on sorted and reverse-sorted inputs. Selecting the first element as the pivot caused the deterministic implementation to produce highly unbalanced partitions, while randomized pivot selection remained much less sensitive to the original ordering.

On random and repeated-element datasets, the deterministic implementation was faster in these measurements. The randomized version incurs additional overhead from selecting and repositioning a random pivot, and the timing results show that randomization did not provide a speed advantage for these particular inputs.

## Hash Table with Chaining

The hash table uses separate chaining for collision resolution. Each table position contains a bucket that can store multiple key-value pairs.

The implementation supports:

- `insert(key, value)`
- `search(key)`
- `delete(key)`

For integer keys, the table uses an affine universal-hashing form:

`h(k) = ((a * k + b) mod p) mod m`

where `p` is a large prime, `m` is the current table capacity, and `a` and `b` are selected when the table is created.

The load factor is calculated as:

`α = n / m`

where `n` is the number of stored entries and `m` is the number of buckets.

The table automatically doubles its capacity before an insertion would cause the load factor to exceed 0.75. Existing entries are then rehashed into the new bucket array.

Under simple uniform hashing, search and delete have expected Θ(1 + α) time. An insertion that checks for an existing key also requires expected Θ(1 + α) time when resizing is not needed. A resize requires Θ(n) work because the existing entries must be rehashed, but doubling the capacity spreads that cost across many insertions. With the load factor kept bounded, search and delete remain expected constant-time operations, while insertion has expected constant-time amortized performance.

## Testing

The automated tests cover:

- empty inputs
- single-element inputs
- sorted and reverse-sorted arrays
- repeated and all-equal values
- negative values
- randomized pivots using multiple seeds
- larger Quicksort datasets
- hash-table insertion and search
- updating existing keys
- deletion of existing and missing keys
- collision handling
- load-factor calculation
- dynamic resizing
- zero and negative integer keys
- invalid constructor settings
- invalid key types
- larger insertion and deletion sequences

The complete test suite currently contains 15 automated tests.

## Running the Project

### 1. Verify Python

```bash
python --version