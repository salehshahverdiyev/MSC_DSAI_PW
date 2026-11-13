# T10 - Implementing a Queue

## Research question

In BFS on graphs with different structures, including a real graph, how do
queue representations compare in average time, worst-case single-operation
time, and memory? Can incremental resizing remove the cost spikes caused by
frontier growth?

## Implementations

All queues implement the same interface:

```python
queue = QueueClass()
queue.enqueue(value)
value = queue.dequeue()
queue.is_empty()
```

Calling `dequeue()` on an empty queue raises `IndexError("queue is empty")`.
Every implementation also exposes the same counters: `size`, `max_size`,
`capacity`, `shifted_elements`, `copied_elements`, `resize_events`, and
`capacity_history`.

The four required queues are:

1. **ShiftingArrayQueue** - a dynamic array whose dequeue shifts every
   remaining element left. Dequeue is `O(n)` and can create large cost spikes.
2. **LinkedListQueue** - a linked list with head and tail pointers. Both
   operations are `O(1)`, but each element requires a node allocation.
3. **CircularArrayQueue** - a ring buffer that doubles immediately when full.
   Normal operations are `O(1)` amortized; resizing copies all live elements
   in one operation.
4. **IncrementalCircularArrayQueue** - a ring buffer that doubles its backing
   storage but migrates at most one existing element per queue operation.
   Migration work is spread across operations instead of appearing as one
   full-copy spike. It uses extra bookkeeping and temporary storage during
   migration; if producers fill the new capacity before migration completes,
   the pending segment can grow and copy its live elements.

The implementations are in [queues.py](./queues.py), and BFS uses the common
`BASELINE_QUEUES` collection in [queues.py](./queues.py).

## BFS workloads

The demo compares all four queues on:

- a path, which keeps the frontier small;
- a star, which creates a wide frontier;
- a binary tree, which grows and then shrinks by levels;
- a grid, which has a moderate frontier;
- a bounded sample of the real `brainlinks.dat` graph.

Run the algorithmic work comparison from the repository root:

```powershell
python -m t10.real_demo `
  --dataset brainlinks.dat --edges 40
```

The command prints an aligned table of visited count, peak queue occupancy,
shifts, copies, and resizes for each queue. These are algorithmic work counters,
not timing benchmarks. The four synthetic shapes use ordinary 0-based labels
and are independent of Brainlinks. The actual directed Brainlinks sample keeps
its original vertex IDs in SVG labels. For a larger genuine sample, run:

```powershell
python -m t10.real_demo --dataset brainlinks.dat --edges 1000 --no-svg
```

The local file has 957,853 unique directed edges on 10,000 vertices; the default
uses just 40 unique edges. Samples are file prefixes, not random samples.
`measure_bfs` remains an illustrative whole-BFS timing/traced-memory helper;
statistical and single-operation measurements remain unfinished.

## Complexity and interpretation

For a graph with `V` vertices and `E` adjacency-list edges, BFS traversal takes
`O(V + E)` time assuming constant-time queue operations; shifting adds work.
Auxiliary space is `O(V)`, excluding the graph itself.
Adjacency-list storage is `O(V + E)`.

Queue operation bounds are:

| Queue | Enqueue | Dequeue | Growth behavior | Element storage |
|---|---:|---:|---|---:|
| Shifting array | `O(1)` amortized | `O(n)` | doubling copy | array capacity |
| Linked list | `O(1)` | `O(1)` | no resize | one node per element |
| Circular doubling | `O(1)` amortized | `O(1)` | one full copy | capacity plus unused slots |
| Incremental circular | `O(1)` normally | `O(1)` normally | one migration step/op; pending overflow can copy | old, new, and pending arrays |

`shifted_elements` and `copied_elements` expose the source of queue work
spikes. `capacity_history` and `resize_events` show when growth occurs.
The incremental implementation removes the normal full-copy resize spike, but
its pending-overflow path is visible in the copy counter and should be included
when interpreting worst-case measurements. Worst-case O(1) is not established;
allocating larger Python backing lists also costs time.
`tracemalloc` in [real_demo.py](./real_demo.py) measures peak traced Python
memory for the whole BFS run; it is not a direct per-element allocator
measurement.

## Correctness evidence

The tests check:

- identical FIFO behavior against `collections.deque`;
- empty-queue errors;
- wrapped circular buffers;
- incremental migration while enqueueing and dequeueing;
- identical BFS distances for every queue;
- resize/copy/shift counters;
- graph loader and visualization behavior.

Run them with:

```powershell
python -m unittest discover -s t10\tests -v
```
