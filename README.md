# Implementing a Queue for BFS-Based Graph Algorithms (C Implementation)

## Project Information
- **Course**: Advanced Data Structures and Algorithms (Fall 2026) · UFAZ / M1 Data Science & AI
- **Topic**: T10 — Implementing a Queue
- **Authors**: Saleh Shahverdiyev & Javidan Hajizada
- **Implementation Language**: C (C11 / C99 standard)
- **Primary Focus**: Comparative empirical evaluation of four FIFO Queue implementations written from scratch in C for BFS graph traversals. Focuses on average throughput, worst-case latency spikes (*cost spikes*), memory overhead per element (including pointer and buffer overhead), and the elimination of allocation bottlenecks via incremental resizing.

---

## 1. Project Overview & Research Question

### Research Question
> *In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue, and circular-array queues compare in average time, worst-case time of a single operation, and memory, and can incremental resizing remove the cost spikes caused by frontier growth?*

### Theoretical Context
Breadth-First Search (BFS) is a fundamental graph traversal algorithm that explores vertices level-by-level using a First-In, First-Out (FIFO) queue to manage the search *frontier*. The topological structure of the graph dictates the growth pattern of this frontier:
- **Dense / Scale-Free Graphs**: Feature high-degree hub vertices that cause sudden, massive expansion spikes in queue size ($|Q|$).
- **Grids and Trees**: Exhibit predictable, wave-front, or bounded frontier growth profiles.

Standard dynamic array queues double their capacity when full using `malloc`/`realloc` and copying existing elements ($O(N)$ reallocation cost). In C, this introduces severe **cost spikes** (nanosecond-level latency spikes) at specific operation indices during frontier expansion. This project implements four distinct queue data structures in pure C and evaluates whether an **incremental resizing** technique can eliminate these spikes by spreading relocation work across operations while maintaining a strict $O(1)$ worst-case time guarantee.

---

## 2. Complete Repository Directory Layout

```text
├── src/                        # Core C source implementations (.c / .h)
│   ├── queues/                 # FIFO Queue Data Structure implementations
│   │   ├── queue.h             # Common Abstract Queue Interface & Function Contracts
│   │   ├── queue_types.h       # Status enums, error codes, and shared struct definitions
│   │   ├── shifting_array_queue.h / .c      # Baseline shifting-array queue
│   │   ├── linked_list_queue.h / .c         # Pointer-based singly linked list queue
│   │   ├── circular_doubling_queue.h / .c   # Circular array with 2x dynamic growth via realloc
│   │   └── circular_incremental_queue.h / .c# Circular array with incremental O(1) resizing
│   ├── graphs/                 # Graph data structures and graph generators
│   │   ├── graph.h / .c                     # Dynamic adjacency list graph representation in C
│   │   ├── synthetic_generators.h / .c      # Synthetic graph generators (Grids, Trees, Scale-Free)
│   │   └── real_graph_loader.h / .c         # Dataset parser for real-world network edge lists
│   └── algorithms/             # Graph traversal algorithms in C
│       ├── bfs.h / .c                       # Standard Breadth-First Search implementation
│       └── multi_source_bfs.h / .c          # Multi-source BFS for varying workload profiles
├── tests/                      # Correctness and Oracle testing framework in C
│   ├── test_hand_verified.c    # Unit tests on deterministic, hand-crafted small graphs
│   └── test_oracle.c           # Differential oracle testing against reference array queue
├── benchmarks/                 # Experimental benchmarking harness & profilers in C
│   ├── timing_rigour.h / .c    # High-resolution POSIX clock_gettime() timer harness
│   ├── memory_profiler.h / .c  # Allocation tracking and byte footprint accounting
│   └── spike_analyzer.h / .c   # Per-operation nanosecond latency trace logger
├── data/                       # Graph datasets
│   ├── raw/                    # Raw real-world graph data (e.g., Wikipedia link graph)
│   └── synthetic/              # Saved synthetic graph seeds and benchmark instances
├── scripts/                    # Post-processing, statistical analysis, & visualization
│   ├── process_benchmarks.py   # Aggregates timing traces, computes medians, IQR, and 99.9th percentiles
│   └── plot_results.py         # Matplotlib/Seaborn script generating latency, memory, and spike plots
├── slides/                     # Presentation deliverables
│   ├── Checkpoint_Slides.pdf   # Lessons 3–4 intermediate progress slides
│   └── Defence_Slides.pdf      # Lessons 7–8 final defence presentation slides
├── Makefile                    # Modular C build configuration (gcc/clang C11)
└── README.md                   # Comprehensive project documentation
```

---

## 3. Detailed Explanation of Folders and Files

### 3.1. `src/queues/` — Queue Data Structure Implementations (C Architecture)
This module contains the four custom FIFO queue implementations written in standard C (C11). To maintain polymorphic modularity without C++ class inheritance, a unified function interface and status error code system is used.

- **`queue_types.h` (Shared Types & Error Enums)**
  - **Purpose**: Defines common return status codes, boolean flags (`<stdbool.h>`), and typedefs used across all queue modules.
  - **Key Enum**:
    ```c
    typedef enum {
        QUEUE_SUCCESS = 0,
        QUEUE_ERR_EMPTY,
        QUEUE_ERR_NOMEM,
        QUEUE_ERR_INVALID_ARG
    } queue_status_t;
    ```

- **`queue.h` (Queue Abstract Interface)**
  - **Purpose**: Defines the unified C functional contract for queue operations using generic struct wrappers or function pointers.
  - **Core Function Signatures**:
    - `queue_status_t queue_enqueue(Queue *q, int value);`: Pushes a vertex ID onto the back of the queue.
    - `queue_status_t queue_dequeue(Queue *q, int *out_value);`: Pops the front vertex ID into `out_value`.
    - `queue_status_t queue_peek(const Queue *q, int *out_value);`: Inspects the front element without removal.
    - `bool queue_is_empty(const Queue *q);`: Returns `true` if element count is 0.
    - `size_t queue_size(const Queue *q);`: Returns current active element count.
    - `size_t queue_capacity(const Queue *q);`: Returns allocated memory capacity in elements.
    - `void queue_destroy(Queue *q);`: Frees all heap-allocated buffers and queue metadata.

- **`shifting_array_queue.h / .c` (Baseline Shifting Array)**
  - **Structure**:
    ```c
    typedef struct {
        int *data;
        size_t size;
        size_t capacity;
    } ShiftingArrayQueue;
    ```
  - **Mechanism**:
    - `enqueue()` appends to `data[size]` in $O(1)$ time (reallocating if necessary).
    - `dequeue()` extracts `data[0]` and shifts remaining $N-1$ elements left by one position using `memmove(data, data + 1, (size - 1) * sizeof(int))` in $O(N)$ time.
  - **Role in Study**: Acts as an unoptimized baseline to demonstrate the performance cost of continuous memory shifting during heavy BFS enqueue/dequeue cycles.

- **`linked_list_queue.h / .c` (Pointer-Based Linked List)**
  - **Structure**:
    ```c
    typedef struct Node {
        int data;
        struct Node *next;
    } Node;

    typedef struct {
        Node *head;
        Node *tail;
        size_t size;
    } LinkedListQueue;
    ```
  - **Mechanism**:
    - `enqueue()` allocates a new `Node` via `malloc(sizeof(Node))` and updates `tail->next`.
    - `dequeue()` removes `head`, saves `data`, updates `head = head->next`, and calls `free(old_head)`.
  - **Trade-offs**: Both operations execute in strict $O(1)$ time without array reallocations, eliminating cost spikes. However, it incurs significant memory overhead ($2\times - 3\times$ bytes per element for 64-bit pointers) and suffers from CPU cache misses due to heap node fragmentation.

- **`circular_doubling_queue.h / .c` (Circular Array with $2\times$ Dynamic Doubling)**
  - **Structure**:
    ```c
    typedef struct {
        int *buffer;
        size_t head;
        size_t tail;
        size_t size;
        size_t capacity;
    } CircularDoublingQueue;
    ```
  - **Mechanism**:
    - Ring buffer using index wrap-around: `tail = (tail + 1) % capacity`.
    - When `size == capacity`, allocates a new buffer of size $2 \times \text{capacity}$ via `malloc()`, copies unrolled elements in logical order (`[0 ... size-1]`), resets `head = 0`, `tail = size`, and `free()`s the old buffer.
  - **Role in Study**: Represents standard dynamic array reallocation. Serves as the primary source of **cost spikes** (latency spikes) during dynamic buffer growth under BFS frontier expansion.

- **`circular_incremental_queue.h / .c` (Circular Array with Incremental $O(1)$ Resizing)**
  - **Structure**:
    ```c
    typedef struct {
        int *old_buffer;
        int *new_buffer;
        size_t old_head;
        size_t new_tail;
        size_t size;
        size_t old_capacity;
        size_t new_capacity;
        size_t migration_head;
        size_t elements_migrated;
        bool is_migrating;
    } CircularIncrementalQueue;
    ```
  - **Mechanism**:
    - Maintains two buffer pointers during active migration: `old_buffer` and `new_buffer`.
    - When `size == old_capacity`, allocates `new_buffer` ($2 \times \text{old_capacity}$) without copying all elements at once, setting `is_migrating = true`.
    - On every subsequent `enqueue()` or `dequeue()` call, moves $k$ (e.g., $k=2$) elements from `old_buffer` to `new_buffer` alongside the main operation.
    - Once all elements are moved, `free(old_buffer)` is called and `is_migrating` becomes `false`.
  - **Research Importance**: Guarantees a strict $O(1)$ worst-case time per operation, eliminating dynamic allocation latency spikes at the cost of managing dual buffer pointers and step-by-step migration logic.

---

### 3.2. `src/graphs/` — Graph Data Structures & Generators in C
Provides lightweight, cache-efficient graph representations and utilities to generate synthetic graph topologies or parse real-world networks in C.

- **`graph.h / .c` (Dynamic Adjacency List Graph)**
  - **Structure**:
    ```c
    typedef struct {
        int *neighbors;
        size_t count;
        size_t capacity;
    } AdjList;

    typedef struct {
        int num_vertices;
        size_t num_edges;
        AdjList *adj; // Array of Adjacency Lists
    } Graph;
    ```
  - **Key Capabilities**: Contiguous, cache-friendly array storage allowing fast neighbor iteration during the inner BFS loop (`for (size_t i = 0; i < graph->adj[u].count; i++)`). Includes `graph_create()`, `graph_add_edge()`, and `graph_destroy()`.

- **`synthetic_generators.h / .c` (Synthetic Graph Generators)**
  - **Purpose**: Generates synthetic graph instances using `rand_r()` or PCG pseudo-random generators to trigger specific BFS frontier growth profiles:
    - **Grid Graphs (2D/3D Mesh)**: Creates wave-front propagation with steady, bounded queue sizes.
    - **Balanced & Unbalanced Trees**: Generates exponential frontier growth (balanced) or narrow linear queue sizes (path graph).
    - **Scale-Free Graphs (Barabási–Albert Model)**: Features high-degree hub nodes that cause massive, sudden spikes in queue size ($|Q|$).
    - **Erdős–Rényi Random Graphs ($G(n, p)$)**: Serves as a baseline random connectivity model.

- **`real_graph_loader.h / .c` (Real-World Dataset Parser)**
  - **Purpose**: Fast edge-list file parser (`fopen`, `fgets`, `strtok_r`) for real-world networks (e.g., Wikipedia link graph, Twitter follower network).
  - **Functionality**: Remaps node IDs to 0-indexed contiguous integers, removes self-loops/duplicate edges, and outputs an initialized `Graph` struct.

---

### 3.3. `src/algorithms/` — Graph Algorithms in C
- **`bfs.h / .c` (Breadth-First Search Engine)**
  - **Purpose**: High-performance BFS implementation parameterized over the `Queue` C interface.
  - **Execution Details**:
    - Allocates distance array `int *dist` (initialized to -1) and visited tracking.
    - Collects traversal completion runtime, level-by-level frontier size ($|Q|$ at distance level $d$), and optional per-operation nanosecond execution timestamps for cost spike correlation.

- **`multi_source_bfs.h / .c` (Multi-Source Workload Variant)**
  - **Purpose**: Runs multi-source BFS searches to test queue performance under sustained high-throughput workloads with multiple simultaneous expanding frontiers.

---

### 3.4. `tests/` — Correctness & Oracle Suite in C
Per the course specification (*Part A4: Correctness first*), benchmarking is strictly prohibited until correctness is proven.

- **`test_hand_verified.c` (Deterministic Unit Tests)**
  - **Purpose**: Validates all 4 C queue implementations on small, hand-crafted graphs (e.g., 5-node star graph, 10-node line graph, 3x3 grid) with manually computed shortest-path distances and vertex visit orders.
  - **Edge Case Coverage**: Enqueue/dequeue wrap-around index boundary conditions, empty queue error return codes, queue expansion during single-element frontiers, and queue emptying/re-filling cycles.

- **`test_oracle.c` (Differential Oracle Testing)**
  - **Purpose**: Runs automated differential testing over 10,000+ random synthetic graphs.
  - **Mechanism**: Runs BFS simultaneously using `ShiftingArrayQueue`, `LinkedListQueue`, `CircularDoublingQueue`, `CircularIncrementalQueue`, and a simple, unresized large static array reference queue. Asserts that output distance arrays `dist[]` match 100% across all implementations.

---

### 3.5. `benchmarks/` — Benchmarking & Profiling Harness in C
Ensures strict experimental rigour (*Part A4: Timing rigour, Defined counters, Resource limits*).

- **`timing_rigour.h / .c` (High-Resolution POSIX Timer Harness)**
  - **Purpose**: Measures execution times using POSIX `clock_gettime(CLOCK_MONOTONIC, &ts)` to eliminate OS scheduling noise and cold-cache artifacts.
  - **Protocol**:
    1. Pre-allocates graph and distance memory outside timed regions.
    2. Executes $N_{\text{warmup}}$ (e.g., 5) untimed warm-up runs.
    3. Runs $N_{\text{timed}}$ (e.g., 31) timed iterations.
    4. Computes median runtimes and Interquartile Ranges (IQR).

- **`memory_profiler.h / .c` (Memory Footprint Accounting in C)**
  - **Purpose**: Tracks exact dynamic memory allocation per queue struct using custom `malloc`/`free` wrappers or struct instrumentation.
  - **Calculations**:
    $$\text{Memory Overhead} = \frac{\text{Total Heap Bytes Allocated by Queue}}{\text{Current Queue Size } |Q|}$$
  - **Accounting**: Measures active element bytes, node pointer overhead (`sizeof(Node)` in `LinkedListQueue`), and unused allocated buffer capacity (`CircularDoublingQueue`).

- **`spike_analyzer.h / .c` (Per-Operation Latency Trace Logger)**
  - **Purpose**: Pre-allocates a nanosecond timestamp array (`uint64_t *latency_trace`) to log individual `enqueue()` and `dequeue()` durations without I/O overhead.
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
Requires a C11 compatible C compiler (`gcc` or `clang`), `make`, and Python 3.8+ (for visualization scripts).

```bash
# Clean previous builds and compile all targets (tests, benchmarks, main driver)
make clean && make all

# Compiler flags used in Makefile:
# gcc -std=c11 -O3 -Wall -Wextra -Wpedantic -D_POSIX_C_SOURCE=200809L -Iinclude -lm
```

### 4.2. Running Correctness Tests
Before running benchmarks, verify that all 4 C queue implementations pass the unit tests and differential oracle:

```bash
# Run hand-verified unit tests and differential oracle
./bin/test_runner
```

### 4.3. Executing Benchmark Suite
Run the automated benchmarking framework across synthetic and real-world graphs:

```bash
# Run full benchmark suite (outputs raw logs to benchmarks/results.csv)
./bin/benchmark_runner --graph-dir data/raw/ --runs 31 --warmup 5
```

### 4.4. Generating Visualizations
Generate comparison plots and summary tables from the benchmark logs:

```bash
python3 scripts/process_benchmarks.py --input benchmarks/results.csv --output benchmarks/summary.csv
python3 scripts/plot_results.py --input benchmarks/summary.csv --out-dir slides/plots/
```

---

## 5. Experimental Protocol & Research Methodology

1. **Hypotheses First**:
   - $H_1$: `ShiftingArrayQueue` will exhibit $O(N^2)$ overall BFS runtime due to $O(N)$ dequeuing shifts (`memmove`).
   - $H_2$: `CircularDoublingQueue` will yield high average throughput but suffer severe $O(|Q|)$ latency cost spikes when crossing capacity thresholds ($2^k$) during `realloc` / buffer copying.
   - $H_3$: `CircularIncrementalQueue` will completely eliminate cost spikes, maintaining strict $O(1)$ worst-case operation bounds at a minor ($<15\%$) average runtime overhead due to incremental migration bookkeeping.
   - $H_4$: `LinkedListQueue` will eliminate allocation spikes but consume $2\times - 3\times$ more memory per element due to 64-bit node pointer overhead and `malloc` metadata.

2. **Frozen Protocol**: Once validated at the Lessons 3–4 checkpoint, compiler flags (`-O3`), random seeds, graph instances, and timing parameters are frozen to prevent bias.

---

## 6. Project Milestones & Deliverables

| Milestone | Lessons | Key Deliverables & Activities |
| :--- | :---: | :--- |
| **Project Charter** | 1–2 | Formulate research question, hypotheses, C queue interface, and choose real-life graph dataset. |
| **Checkpoint** | 3–4 | Implement 4 C queues, graph representations, BFS, and correctness oracles. Deliver `Checkpoint_Slides.pdf`. |
| **Data Collection** | 5–6 | Execute pilot benchmarks, collect POSIX timing and memory traces, perform statistical analysis. |
| **Final Defence** | 7–8 | Deliver `Defence_Slides.pdf`, C source code, reproducible benchmarks, and defend results individually. |
