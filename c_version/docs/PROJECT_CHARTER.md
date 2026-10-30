# T10 project charter

UFAZ, Advanced Data Structures and Algorithms, Fall 2026.
Javidan Hajizada and Saleh Shahverdiyev. C11, own implementations.

> In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?

M1 target: Friday 2026-10-30, three tested baseline queues and a reproducible BFS
prototype. The fourth queue is a design task, not a working implementation.
Final goals remain in [PROJECT_OBJECTIVES.md](../../PROJECT_OBJECTIVES.md), including
multi-source BFS, more generators and measured comparisons; those are future work.

Pre-experiment hypotheses (no performance experiments yet):

- H1: sustained large occupancy increases shifting cost. Total shifted elements
  equal the sum of (occupancy before successful dequeue minus one); a path can
  have no shifts, so quadratic BFS is not a universal prediction.
- H2: ring doubling concentrates linear copying at full capacity while giving
  amortized constant copying work per insertion across a sequence.
- H3: a correct bounded-progress incremental design could reduce copy-work
  peaks, at bookkeeping and temporary memory cost. Wall-clock benefits are open.
- H4: list nodes can cost extra bytes and locality, but allocation latency,
  throughput and actual overhead depend on the machine and allocator.

ADT: FIFO int values copied by value, opaque owned queue, create/destroy,
enqueue/dequeue/peek, size/is_empty and status-returning capacity query.
See [queue.h](../include/queue.h) for errors, NULL behavior and output semantics.
Arrays start with four slots, double on full, do not shrink. List capacity is N/A.
Allocation failures must preserve the existing logical FIFO.

Path controls narrow frontiers; star stresses sudden growth; diamond/cycle
checks repeated discovery and unreachable vertices. Later add grids and trees.
The real-world candidate and acquisition status are in the shared
[DATASET_DECISION.md](../../docs/DATASET_DECISION.md).
Correctness precedes paired measurements; protocol remains DRAFT until review.
