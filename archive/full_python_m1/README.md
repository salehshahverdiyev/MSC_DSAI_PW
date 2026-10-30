# Archived full Python M1

Javidan Hajizada and Saleh Shahverdiyev — UFAZ Advanced Data Structures and
Algorithms. This is the archived three-queue implementation. The previous C project
is preserved separately in [c_version/](../../c_version/README.md) for reference.
Course-level Python approval has not been recorded. Python 3, standard library
only; verified with WSL Python 3.12.3.

Research question:

> In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?

## Run from the repository root

In Linux/WSL, use `python3` (or `python` if it names Python 3):

```sh
python3 -m compileall -q t10_python
python3 -m unittest discover -s archive/full_python_m1/tests -v
python3 -m archive.full_python_m1.demo
```

On this Windows machine there is no usable native Python installation, so these
exact PowerShell commands run the installed Ubuntu interpreter:

```powershell
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m compileall -q t10_python
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m unittest discover -s archive/full_python_m1/tests -v
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m archive.full_python_m1.demo
```

For Windows with Python 3 already installed, from the repository root:

```powershell
python -m unittest discover -s archive/full_python_m1/tests -v
python -m archive.full_python_m1.demo
```

The native Windows commands are instructions for an installed interpreter; only
WSL execution was verified here. No installation or third-party package needed
in the tested WSL environment. There is no separate build or Makefile for Python.

## Read the code in this order

1. [queues.py](queues.py): three plain classes implementing the same methods.
2. [graph.py](graph.py): a list of outgoing-neighbor lists inside a small Graph.
3. [bfs.py](bfs.py): one BFS, queue selected by its class, simple trace flag.
4. [sample_graphs.py](sample_graphs.py): six-vertex examples and hand answers.
5. [demo.py](demo.py): run every baseline, check answers, then trace the star.

[generators.py](generators.py) builds deterministic path, star, tree and grid
graphs. Tests use unittest, deque as a FIFO oracle only, and independent repeated
edge relaxation as a distance oracle. There is no inheritance, external graph
library, queue adapter, observer framework or automatic queue fallback.

## Queue contract and visible storage

`ShiftingArrayQueue`, `LinkedListQueue`, and `CircularArrayQueue` support:
`enqueue(value)`, `dequeue()`, `peek()`, `is_empty()`, `len(queue)`.
Empty dequeue/peek raise `IndexError("queue is empty")` without changing state.
Queues hold references, so `None` and other Python objects are valid values;
BFS itself enqueues integer vertex IDs. Do not modify queue fields directly.

The arrays start with four `[None]` slots (positive initial capacity is optionally
selectable), double only on full, explicitly copy references in loops and never
shrink. Shifting removal explicitly shifts every remaining reference. Ring
removal advances `front` modulo capacity and clears the vacated slot. No list
append/pop growth implements either queue. Linked nodes use head/tail/size;
removing the final node clears both ends. No manual free/destroy is required.

`to_list()` creates a logical FIFO snapshot for learning/tests, not performance
measurement. `storage_info()` returns current `size`, logical `capacity`,
`unused_slots`, and number of live linked `nodes`. For linked lists, capacity
and unused slots are `None` (N/A); arrays report nodes=0. These are counts, **not
total memory bytes or timings**. Removed array slots are reset to None so they
do not retain obsolete payload references. Python allocation exceptions propagate;
exhaustive low-memory recovery/fault-injection equivalence to C is not claimed.

| Queue | Enqueue algorithmic work | Dequeue work |
| --- | --- | --- |
| Shifting array | O(1) ordinary; O(q) growth; amortized O(1) | O(q) |
| Linked list | O(1) reference updates plus node allocation | O(1) reference updates |
| Doubling ring | O(1) ordinary; O(q) growth; amortized O(1) | O(1) |
| Incremental ring | **NOT YET IMPLEMENTED**; bound unproven | Not implemented |

Here q is live occupancy. Costs assume fixed-size reference/index work;
interpreter, allocator, garbage collection and list initialization affect actual
elapsed time. Shifting's total removal work depends on occupancy, not universally
V² for every BFS. See [EXPERIMENT_PLAN.md](EXPERIMENT_PLAN.md) for precise caveats.

## Graphs, BFS and expected output

A vertex is an ID 0..n-1; an edge connects vertices. `adjacency[v]` is the list
of outgoing neighbors of v. Undirected addition stores both directions except
self-loops once; directed addition stores only the supplied direction. Neighbor
order is insertion order; duplicate edges are allowed. Construct graphs through
add_edge, then treat them as read-only while BFS runs. Empty graphs and invalid
IDs/dimensions raise ValueError. Initial Graph adjacency lists are independent.

`bfs(graph, source, queue_class, trace=False)` returns `(distances, counters)`.
Distances are indexed by vertex ID, source=0 distance, and -1 is unreachable.
Mark vertices on discovery, enqueue once, process FIFO; no duplicated BFS logic.
`visited` counts successful dequeues, `enqueue_count` includes the initial source,
`dequeue_count` counts successful removals, `frontier_peak` is maximum pending
occupancy after operations (not generally whole-level width).

| Six-vertex graph, source 0 | Distances for all three queues | visited/enq/deq | peak |
| --- | --- | --- | --- |
| Undirected path | `0 1 2 3 4 5` | 6/6/6 | 1 |
| Undirected star | `0 1 1 1 1 1` | 6/6/6 | 5 |
| Directed diamond/cycle + isolated 5 | `0 1 1 2 3 -1` | 5/5/5 | 2 |

Diamond edges: 0->1,0->2,1->3,2->3,3->0,3->4. All nine demo rows were parsed and
compared against the actual C demo; distances and counters match. The final star
walkthrough prints actual enqueue/dequeue events and queue contents front-to-back:
[0], then [] after removing 0, then the five leaves grow to [1,2,3,4,5] and drain
in FIFO order. `trace=True` calls to_list/print inside the same BFS; disable it
for all future timing. The walkthrough is not a benchmark.

## Correctness evidence and remaining work

18 unittest methods pass: empty/FIFO/interleaving/refill/reference values,
multiple doublings, nonzero-front wrapped growth, small capacities, storage
counts, graph/generator validation, hand distances, actual trace parity, plus
50,000 seeded steps per queue and 100 graphs x 16 sources x three queues checked
against repeated relaxation. Seeds: queues 20261030, test graphs 1030. Finite
tests are evidence, not a proof for all inputs. Tests use unittest checks rather
than bare assert; failures exit nonzero. Tests in the original C tree are intact.

Final requirements remain: fourth queue with justified FIFO/progress/capacity
invariants and a valid work bound, real-data ingestion, paired controlled timing,
average operation costs, individual-operation distributions/slowest observations,
memory including unused capacity and temporary buffers, documented seeds/
environment/caps, repetitions/medians/spread, protocol freeze and final defence.
No benchmark harness/results or memory-byte measurements exist in this phase.

The existing [dataset decision](../../docs/DATASET_DECISION.md) proposes NADINE
C. elegans (source-reported 279 neurons); no raw dataset is present or loaded,
and local edge count/reachability are unknown. This phase did not download it.
The [Python experiment plan](EXPERIMENT_PLAN.md) is DRAFT and does not revise or
freeze the [C reference protocol](../../c_version/docs/EXPERIMENT_PROTOCOL.md).
The active learning prototype is in ../../t10_python/; record outstanding language
and experimental-model decisions with Pavel.

Use the [five-minute presentation script](CHECKPOINT_SCRIPT.md) for a truthful
checkpoint talk. From the repository root, run the C reference independently
with `make -C c_version test demo walkthrough`. C and Python timings must never be pooled as though
they measured interchangeable runtimes.

