# Implementing a Queue for BFS-Based Graph Algorithms

## Project Information
- **Course**: Advanced Data Structures and Algorithms (Fall 2026) · UFAZ / M1 Data Science & AI
- **Topic**: Implementing a Queue
- **Authors**: Saleh Shahverdiyev & Javidan Hajizada
- **Primary Focus**: Comparative empirical evaluation of four FIFO Queue implementations in BFS graph traversals, focusing on average throughput, worst-case latency spikes (*cost spikes*), memory overhead per element, and the mitigation of capacity allocation bottlenecks through incremental resizing.

---

## 1. Project Overview & Research Question

### Research Question
> *In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue, and circular-array queues compare in average time, worst-case time of a single operation, and memory, and can incremental resizing remove the cost spikes caused by frontier growth?*

### Theoretical Context
Breadth-First Search (BFS) is a fundamental graph traversal algorithm that processes nodes level-by-level using a First-In, First-Out (FIFO) queue to maintain the search *frontier*. The structure of the target graph heavily influences how this frontier grows and shrinks over time:
- **Dense/Scale-free graphs**: Produce sharp, massive spikes in the queue size ($|Q|$) as high-degree hub nodes are processed.
- **Grids and Trees**: Result in predictable, linear, or bounded frontier growth.

Standard dynamic array queues double their capacity when full ($O(N)$ reallocation copy), which introduces severe **cost spikes** (latency spikes) at specific operation indices during frontier expansion. This project implements four distinct queue data structures from scratch and evaluates whether an **incremental resizing** mechanism can eliminate these spikes while maintaining an $O(1)$ worst-case time guarantee per operation without incurring prohibitive average-case overhead.

---

## 2. Complete Repository Directory Layout

```text
├── src/                        # Core C++ / Java source implementations
│   ├── queues/                 # FIFO Queue Abstract Data Type implementations
│   │   ├── Queue.hpp           # Abstract Base Class / Interface for Queue ADT
│   │   ├── ShiftingArrayQueue.hpp / .cpp      # Baseline shifting-array queue
│   │   ├── LinkedListQueue.hpp / .cpp         # Pointer-based singly linked list queue
│   │   ├── CircularArrayDoublingQueue.hpp / .cpp   # Circular array with 2x dynamic growth
│   │   └── CircularArrayIncrementalQueue.hpp / .cpp # Circular array with incremental O(1) resizing
│   ├── graphs/                 # Graph data structures and graph generators
│   │   ├── Graph.hpp / .cpp                   # Adjacency list graph representation
│   │   ├── SyntheticGenerators.hpp / .cpp     # Synthetic graph generators (Grids, Trees, Scale-Free)
│   │   └── RealGraphLoader.hpp / .cpp         # Dataset parser for real-world network graphs
│   └── algorithms/             # Graph algorithms utilizing the Queue interface
│       ├── BFS.hpp / .cpp                     # Standard Breadth-First Search implementation
│       └── MultiSourceBFS.hpp / .cpp          # Multi-source BFS for varying workload profiles
├── tests/                      # Correctness and Oracle testing framework
│   ├── HandVerifiedTests.cpp   # Unit tests on deterministic, hand-crafted small graphs
│   └── OracleTests.cpp         # Differential testing oracle against std::queue / reference implementations
├── benchmarks/                 # Experimental benchmarking harness & profilers
│   ├── TimingRigour.hpp / .cpp # High-resolution timer harness with warm-ups & median filtering
│   ├── MemoryProfiler.hpp / .cpp              # Memory footprint and unused capacity accounting
│   └── SpikeAnalyzer.hpp / .cpp               # Per-operation latency trace logger for spike detection
├── data/                       # Graph datasets
│   ├── raw/                    # Raw real-world graph data (e.g., Wikipedia link graph)
│   └── synthetic/              # Saved synthetic graph seeds and benchmark instances
├── scripts/                    # Post-processing, statistical analysis, & visualization
│   ├── process_benchmarks.py   # Aggregates timing traces, computes medians, IQR, and 99.9th percentiles
│   └── plot_results.py         # Matplotlib/Seaborn script generating latency, memory, and spike plots
├── slides/                     # Presentation deliverables
│   ├── Checkpoint_Slides.pdf   # Lessons 3–4 intermediate progress slides
│   └── Defence_Slides.pdf      # Lessons 7–8 final defence presentation slides
├── Makefile / CMakeLists.txt   # Project build automation configuration
└── README.md                   # Comprehensive project documentation
```

---

## 3. Detailed Explanation of Folders and Files

### 3.1. `src/queues/` — Queue Data Structure Implementations
This folder contains the core queue implementations being evaluated. All queues implement a uniform interface to ensure fair and decoupled benchmarking within the BFS algorithm.

- **`Queue.hpp` (Queue Abstract Interface)**
  - **Purpose**: Defines the pure virtual contract (ADT) that all four queue variants must implement.
  - **Key Methods**:
    - `virtual void enqueue(const T& value) = 0;`: Inserts an element at the back of the queue.
    - `virtual T dequeue() = 0;`: Removes and returns the element at the front of the queue.
    - `virtual const T& peek() const = 0;`: Returns the front element without removal.
    - `virtual bool isEmpty() const = 0;`: Returns `true` if the queue contains 0 elements.
    - `virtual size_t size() const = 0;`: Returns the current number of elements in the queue.
    - `virtual size_t capacity() const = 0;`: Returns the total allocated memory capacity (buffer size).
  - **Specification Contract**: Defines explicit behavior for edge cases (e.g., throwing `std::underflow_error` when dequeuing from an empty queue).

- **`ShiftingArrayQueue.hpp / .cpp` (Baseline Shifting Array)**
  - **Purpose**: Implements a simple array-backed queue where the front element is always stored at index `0`.
  - **Mechanism**:
    - `enqueue()` appends to index `size` in $O(1)$ time.
    - `dequeue()` removes the element at index `0` and shifts all remaining $N-1$ elements left by one position in $O(N)$ time.
  - **Role in Study**: Acts as an unoptimized baseline to demonstrate the performance cost of naive memory shifting during heavy BFS enqueue/dequeue cycles.

- **`LinkedListQueue.hpp / .cpp` (Pointer-Based Linked List)**
  - **Purpose**: Implements a dynamic, pointer-based singly linked list with `head` and `tail` pointers.
  - **Mechanism**:
    - Each element is stored in a dynamically allocated `Node` containing `T data` and `Node* next`.
    - Both `enqueue()` and `dequeue()` operate in strict $O(1)$ worst-case time without array reallocations.
  - **Trade-offs**: Incurs high memory overhead per element (pointer storage) and poor CPU cache locality due to heap fragmentation during frequent node allocations/deallocations.

- **`CircularArrayDoublingQueue.hpp / .cpp` (Circular Array with $2\times$ Dynamic Doubling)**
  - **Purpose**: Implements a ring buffer using head/tail index wrap-around (`(index + 1) % capacity`).
  - **Mechanism**:
    - When `size == capacity`, allocates a new array of size $2 \times \text{capacity}$, copies existing elements in logical order, resets `head = 0` and `tail = size`, and frees the old array.
  - **Role in Study**: Represents the standard library strategy (e.g., C++ `std::vector` / Java `ArrayList`). Serves as the primary source of **cost spikes** during dynamic reallocation when the BFS frontier expands.

- **`CircularArrayIncrementalQueue.hpp / .cpp` (Circular Array with Incremental Resizing)**
  - **Purpose**: Implements a worst-case $O(1)$ time circular array queue that eliminates allocation cost spikes during resizing.
  - **Mechanism**:
    - Maintains two buffers during migration: `old_buffer` and `new_buffer`.
    - When capacity is reached, allocates a larger buffer without copying all elements at once.
    - On every subsequent `enqueue()` or `dequeue()` call, moves $k$ (e.g., $k=2$) elements from `old_buffer` to `new_buffer` alongside the regular operation.
    - Once migration completes, `old_buffer` is deallocated and `new_buffer` becomes primary.
  - **Research Importance**: Guarantees bounded worst-case per-operation execution time at the cost of managing dual pointers and incremental copying logic.

---

### 3.2. `src/graphs/` — Graph Data Structures & Generators
This module provides graph representations and utilities to generate synthetic graph families or load real-world networks.

- **`Graph.hpp / .cpp` (Adjacency List Graph)**
  - **Purpose**: Compact, cache-friendly graph representation storing vertices and directed/undirected edges using adjacency lists (`std::vector<std::vector<int>>`).
  - **Key Capabilities**: Fast neighbor iteration required during the BFS inner loop (`for (int neighbor : adj[u])`).

- **`SyntheticGenerators.hpp / .cpp` (Controlled Synthetic Graph Generators)**
  - **Purpose**: Generates synthetic graph topologies designed to trigger specific BFS frontier growth profiles:
    - **Grid Graphs (2D/3D Mesh)**: Creates wave-front propagation with steady, bounded queue sizes.
    - **Balanced & Unbalanced Trees**: Generates exponential frontier growth (balanced) or narrow linear queue sizes (unbalanced/path graph).
    - **Scale-Free Graphs (Barabási–Albert Model)**: Features high-degree hub nodes that cause massive, sudden spikes in queue size ($|Q|$).
    - **Erdős–Rényi Random Graphs ($G(n, p)$)**: Serves as a baseline random connectivity model.

- **`RealGraphLoader.hpp / .cpp` (Real-World Graph Dataset Parser)**
  - **Purpose**: Parses external real-world network edge lists (e.g., Wikipedia link network, Twitter follower graph).
  - **Functionality**: Handles node ID remapping (0-indexed contiguous integers), removes self-loops/duplicate edges, and outputs a clean `Graph` object.

---

### 3.3. `src/algorithms/` — Graph Algorithms
- **`BFS.hpp / .cpp` (Breadth-First Search Engine)**
  - **Purpose**: Templated or interface-driven BFS implementation accepting any class implementing `Queue`.
  - **Metrics Captured**:
    - Traversal completion time.
    - Level-by-level frontier size ($|Q|$ at distance level $d$).
    - Full sequence of queue operations mapped to time stamps for cost spike correlation.

- **`MultiSourceBFS.hpp / .cpp` (Multi-Source Workload Variant)**
  - **Purpose**: Runs multi-source BFS searches to test queue performance under sustained high-throughput workloads with multiple simultaneous expanding frontiers.

---

### 3.4. `tests/` — Correctness & Oracle Suite
Per the course specification (*Part A4: Correctness first*), benchmarking is strictly prohibited until correctness is proven.

- **`HandVerifiedTests.cpp` (Deterministic Unit Tests)**
  - **Purpose**: Validates all 4 queue implementations on small, hand-crafted graphs (e.g., 5-node star graph, 10-node line graph, 3x3 grid) with manually computed shortest-path distances and vertex visit orders.
  - **Edge Case Coverage**: Enqueue/dequeue wrap-around boundary conditions, empty queue exceptions, queue expansion during single-element frontiers, and queue emptying/re-filling cycles.

- **`OracleTests.cpp` (Differential Oracle Testing)**
  - **Purpose**: Runs automated differential testing over 10,000+ random synthetic graphs.
  - **Mechanism**: Runs BFS simultaneously using `ShiftingArrayQueue`, `LinkedListQueue`, `CircularArrayDoublingQueue`, `CircularArrayIncrementalQueue`, and a reference standard library queue (`std::queue`). Asserts that distance arrays `dist[]` and traversal orders match 100% across all implementations.

---

### 3.5. `benchmarks/` — Benchmarking & Profiling Harness
Ensures strict experimental rigour (*Part A4: Timing rigour, Defined counters, Resource limits*).

- **`TimingRigour.hpp / .cpp` (High-Resolution Timer Harness)**
  - **Purpose**: Measures execution times while eliminating OS scheduling noise and cold-cache artifacts.
  - **Protocol**:
    1. Pre-allocates graph memory outside the timed region.
    2. Executes $N_{\text{warmup}}$ (e.g., 5) untimed warm-up runs.
    3. Runs $N_{\text{timed}}$ (e.g., 31) timed iterations.
    4. Reports median runtimes and Interquartile Ranges (IQR).

- **`MemoryProfiler.hpp / .cpp` (Memory Footprint Accounting)**
  - **Purpose**: Measures exact memory footprint per queue element across operations.
  - **Calculations**:
    $$\text{Memory Overhead} = \frac{\text{Total Bytes Allocated by Queue}}{\text{Current Queue Size } |Q|}$$
  - **Accounting**: Tracks active element bytes, node pointer overhead (`LinkedListQueue`), and unused allocated buffer capacity (`CircularArrayDoublingQueue`).

- **`SpikeAnalyzer.hpp / .cpp` (Per-Operation Latency Trace Logger)**
  - **Purpose**: Logs high-resolution timestamps for *every individual* `enqueue()` and `dequeue()` call during a BFS run.
  - **Analysis**: Isolates the worst-case operation latency ($99.9\text{th}$ percentile and maximum cost spikes) and correlates spike occurrences with internal array reallocation events.

---

### 3.6. `data/` — Graph Datasets
- **`data/raw/`**: Contains raw edge-list text files (e.g., `wiki-Vote.txt`, `twitter_combined.txt`).
- **`data/synthetic/`**: Contains fixed random seeds and serialized synthetic benchmark graphs to ensure 100% reproducibility across environments.

---

### 3.7. `scripts/` — Post-Processing & Visualization
- **`process_benchmarks.py`**: Aggregates JSON/CSV benchmark output logs, calculates summary statistics (median, std dev, 95th/99.9th percentiles), and outputs formatted Markdown/LaTeX tables.
- **`plot_results.py`**: Generates publication-quality charts using `matplotlib` and `seaborn`:
  1. **Average Runtime vs. Graph Size**: Compares overall BFS throughput across graph topologies.
  2. **Latency Timeline & Cost Spikes**: Plots operation latency over operation index, highlighting capacity reallocation spikes vs. incremental smooth latencies.
  3. **Memory Footprint per Element**: Plots memory overhead as queue capacity fluctuates during BFS expansion.

---

### 3.8. `slides/` — Presentation Deliverables
- **`Checkpoint_Slides.pdf`**: Presentation deck delivered for Lessons 3–4 oral checkpoint (covering ADT design, correctness oracle proofs, and frozen experimental protocol).
- **`Defence_Slides.pdf`**: Final defence presentation deck delivered for Lessons 7–8 (presenting empirical results, cost spike analysis, memory trade-offs, and research conclusions).

---

## 4. How to Build, Test, and Run Benchmarks

### 4.1. Prerequisites & Compilation
Requires a C++17 compatible compiler (`g++` or `clang++`) and Python 3.8+ (for visualization scripts).

```bash
# Build the entire project (tests, benchmarks, and main executable)
make clean && make all

# Alternatively using CMake:
mkdir -p build && cd build
cmake ..
make -j4
```

### 4.2. Running Correctness Tests
Before running benchmarks, verify that all 4 queue implementations pass the unit tests and differential oracle:

```bash
# Run hand-verified unit tests and differential oracle
./bin/run_tests
```

### 4.3. Executing Benchmark Suite
Run the automated benchmarking framework across synthetic and real-world graphs:

```bash
# Run full benchmark suite (outputs raw logs to benchmarks/results.json)
./bin/run_benchmarks --graph-dir data/raw/ --runs 31 --warmup 5
```

### 4.4. Generating Visualizations
Generate comparison plots and summary tables from the benchmark logs:

```bash
python3 scripts/process_benchmarks.py --input benchmarks/results.json --output benchmarks/summary.csv
python3 scripts/plot_results.py --input benchmarks/summary.csv --out-dir slides/plots/
```

---

## 5. Experimental Protocol & Research Methodology

1. **Hypotheses First**:
   - $H_1$: `ShiftingArrayQueue` will exhibit $O(N^2)$ overall BFS runtime due to $O(N)$ dequeuing shifts.
   - $H_2$: `CircularArrayDoublingQueue` will yield high average throughput but suffer severe $O(|Q|)$ latency cost spikes when crossing capacity thresholds ($2^k$).
   - $H_3$: `CircularArrayIncrementalQueue` will completely eliminate cost spikes, maintaining strict $O(1)$ worst-case operation bounds at a minor ($<15\%$) average runtime overhead due to incremental migration bookkeeping.
   - $H_4$: `LinkedListQueue` will eliminate allocation spikes but consume $2\times - 3\times$ more memory per element due to node pointer overhead.

2. **Frozen Protocol**: Once validated at the Lessons 3–4 checkpoint, compiler flags (`-O3`), random seeds, graph instances, and timing parameters are frozen to prevent bias.

---

## 6. Project Milestones & Deliverables

| Milestone | Lessons | Key Deliverables & Activities |
| :--- | :---: | :--- |
| **Project Charter** | 1–2 | Formulate research question, hypotheses, ADT contract, and choose real-life graph dataset. |
| **Checkpoint** | 3–4 | Implement 4 queues, graph representations, BFS, and correctness oracles. Deliver `Checkpoint_Slides.pdf`. |
| **Data Collection** | 5–6 | Execute pilot benchmarks, collect timing and memory traces, perform statistical analysis. |
| **Final Defence** | 7–8 | Deliver `Defence_Slides.pdf`, source code, reproducible benchmarks, and defend results individually. |
