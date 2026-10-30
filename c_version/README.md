# T10: Implementing a queue for BFS

This is the preserved C legacy/reference implementation. The primary project is
now [t10_python/](../t10_python/README.md). The original C documentation below
retains its prototype scope; commands and links reflect the new directory.

UFAZ, Advanced Data Structures and Algorithms, Fall 2026.
Javidan Hajizada and Saleh Shahverdiyev. Implementation: C11.

> In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?

This is the **M1 prototype for Friday, October 30, 2026**, an unfinished research
project. Three baseline queues, graph storage and single-source BFS work.
Incremental resizing is **NOT IMPLEMENTED**; requesting it returns
`QUEUE_UNSUPPORTED`. No benchmark results or performance conclusions exist.

| Component | Current status |
| --- | --- |
| Common FIFO API | Implemented; ownership/errors in [include/queue.h](include/queue.h) |
| Shifting array | Implemented; append/double, dequeue shifts remaining items |
| Singly linked list | Implemented; head/tail; allocation per enqueue; capacity N/A |
| Circular doubling | Implemented; wrapped FIFO copy on growth, no shrinking |
| Graph + BFS | Implemented; directed/undirected, insertion-order neighbors, distances and operation/occupancy counts |
| Correctness | Hand examples, independent FIFO/relaxation oracles, fault injection, sanitizer checks |
| Fourth queue | Preliminary [design](docs/INCREMENTAL_DESIGN.md), no proven bound yet |
| Real graph | NADINE C. elegans candidate; acquisition/loader pending |
| Measurements | Draft protocol only; timing, memory profiler and charts pending |

## Source layout

- `src/`: implementation `.c` files, with queue implementations in `src/queues/`.
- `include/`: `.h` headers, including the internal queue definitions.
- `tests/`: correctness test `.c` files.

## Build, test and demonstrate

Requires a C11 compiler and GNU Make with a POSIX shell. No external C libraries.
Verified on Ubuntu WSL2: GCC 13.3.0, GNU Make 4.3. Native Windows compiler/Make
were not available on the development PATH. From `c_version/` in Linux/WSL:

```sh
make all
make test
make demo
```

For a short learning trace, run `make walkthrough`. It uses the same BFS on the
six-vertex star with the circular-doubling queue. Each successful enqueue or
dequeue emits a real event; the display reconstructs the pending FIFO front to
back. Watch `[0]` become empty while 0 is processed, then grow to `[1,2,3,4,5]`
and drain in that order. Final distances are `0 1 1 1 1 1`, peak occupancy 5.
This is an explanation of BFS, not a benchmark. Normal `make demo` is unchanged.

From PowerShell on this machine:

```powershell
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version walkthrough
```

One-command correctness demonstration: `make test demo` (or `make demo` for just
the three graph examples), when inside `c_version/`. From the repository root
use `make -C c_version test demo walkthrough`. From **Windows PowerShell**:

```powershell
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version clean
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version all test demo
```

Default flags: `-std=c11 -O2 -Wall -Wextra -Wpedantic`. CC, CFLAGS,
CPPFLAGS and LDFLAGS may be overridden on the Make command line. For Ubuntu
without a toolchain: install `build-essential` using its package manager, then
run the commands above. No Python dependency for M1.

Additional verification on GCC/Ubuntu:

```sh
make test-failures  # GNU linker --wrap fault injection
make debug         # clean rebuild, ASan/UBSan, tests + fault injection + demo/walkthrough
make clean         # remove executables before switching back to release flags
```

Debug requires sanitizer support and a GNU-compatible linker; it leaves sanitized
binaries in build/. Default tests/demo use only standard C11.

## What the demo establishes

Source vertex is 0. Every queue is checked against these hand-worked distances:

| Graph (6 vertices) | Distance array | Visited | Peak live queue |
| --- | --- | --- | --- |
| Undirected path | `0 1 2 3 4 5` | 6 | 1 |
| Undirected star | `0 1 1 1 1 1` | 6 | 5 |
| Directed diamond/cycle, isolated vertex 5 | `0 1 1 2 3 -1` | 5 | 2 |

Path edges are 0--1--2--3--4--5. Star edges are 0--v for v=1..5.
Diamond edges: 0->1, 0->2, 1->3, 2->3, 3->0, 3->4.
-1 means unreachable. Successful enqueues/dequeues equal visited vertices.
Peak occupancy is measured after operations, not the number of vertices in an
entire BFS level. These are correctness observations, not performance results.

The queue suite checks 50,000 seeded mixed operations **per baseline** against
independent fixed storage, plus empty/error semantics, boundary int values,
multiple growths, refill cycles and a ring resize with nonzero head. BFS tests
check hand graphs and 100 deterministic directed/undirected graphs, each from
16 sources across three queues, against repeated edge relaxation. Optional fault
tests inject failed allocations in creation, growth, graph insertion and BFS.
Passing finite tests is evidence of correctness, not an exhaustive proof.

## Research materials and remaining work

- [Charter and hypotheses](docs/PROJECT_CHARTER.md)
- [Experimental protocol: DRAFT](docs/EXPERIMENT_PROTOCOL.md)
- [Shared dataset candidate and acquisition plan](../docs/DATASET_DECISION.md)
- [Incremental migration questions](docs/INCREMENTAL_DESIGN.md)
- [Friday checkpoint: six-slide outline and commands](docs/CHECKPOINT_2026-10-30.md)
- [Final project objectives](../PROJECT_OBJECTIVES.md)

Arrays start at capacity 4, double when full and never shrink. Shifting dequeue
does linear work in current occupancy; total BFS shifting depends on its queue
profile. Linked-list pointer work is constant, but allocator latency can vary.
Doubling has amortized constant insertion work and occasional linear copying.
Bounded incremental copying would not itself bound allocation or elapsed time.

M1 stops here: no incremental implementation, real-data loader, multi-source BFS,
grid/random production generators, timing harness, memory profiler, benchmark
plots or final slide deck. The protocol has not been frozen at a teacher review.
