# Slide 1 — Research question
T10 — Implementing a Queue. UFAZ M1 Advanced Data Structures and Algorithms.
Javidan Hajizada and Saleh Shahverdiyev. Checkpoint with Professor Pavel.

“In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?”

Today: correctness and exact algorithmic work. No timing conclusions.

---
# Slide 2 — Four queues and status
| Queue | Status | Important algorithmic cost |
|---|---|---|
| Shifting array | Implemented, tested | dequeue shifts size-1 references |
| Linked list | Restored from archive, tested | constant pointer operations; one node allocation per enqueue |
| Circular doubling | Implemented, tested | constant dequeue; full enqueue copies size references |
| Circular incremental | Design only; mandatory final work | aim: bounded migration per operation; proof pending |
Arrays start at four slots, double, never shrink. All expose enqueue, dequeue, is_empty; empty dequeue raises IndexError.
Doubling enqueue is amortized O(1), with O(n) individual growth work. Python allocation costs need separate treatment.

---
# Slide 3 — Graphs and BFS
One adjacency-list BFS accepts any queue class. Mark discovered before enqueue, so each reachable vertex enters once. FIFO processes vertices in nondecreasing distance. Unreachable distance is -1.

Path: distances 0,1,2,3,4,5; peak occupancy 1.
Star: distances 0,1,1,1,1,1; peak occupancy 5.
Binary tree: distances 0,1,1,2,2,2,2; peak occupancy 4.
Real data: directed C. elegans summed links, 279 vertices, 2990 unique edges. Row i j w means j -> i. Positive weights become unweighted edges. Source 0 reaches 275 vertices. These are local correctness observations.

---
# Slide 4 — Correctness and executed work
11 tests pass on portable native CPython 3.13.1. Queue oracle: collections.deque, seeded interleaving. Distance oracle: repeated edge relaxation, independent of BFS. Wrapped growth, drain/refill, None payloads and malformed data tested.

| Graph | Peak | Shifting queue shifts | Array resize copies | Array growth events |
|---|---:|---:|---:|---:|
| Path, 6 vertices | 1 | 0 | 0 | 0 |
| Star, 6 vertices | 5 | 10 | 4 | 1 |
| Tree, 7 vertices | 4 | 9 | 0 | 0 |
Copies apply to each array implementation; linked-list shifts/copies/growth are zero. Zero copies does not mean zero work or zero memory. Counts are increments inside executed loops, not elapsed times.

---
# Slide 5 — Hypotheses and proposed protocol
H1: broad frontiers increase shifting work and likely BFS time.
H2: doubling produces copy bursts despite amortized constant enqueue work.
H3: incremental migration could distribute copies but adds metadata and temporary storage.
H4: linked nodes may use more memory per live element; arrays retain unused slots.

DRAFT: identical graphs/sources/neighbor order; fixed seeds; paired repetitions; rotate queue order; 3 warm-ups and 11 measured runs proposed. Report median, IQR, paired ratios, observed maximum latency and high percentiles. Separate throughput, individual-operation diagnostics, and memory passes. Freeze settings after feasibility and approval. No final experiments run.

---
# Slide 6 — Remaining work
Prove and implement incremental migration; test interleavings and bounded progress.
Approve and freeze experimental protocol, sizes, resource limits and sources.
Build timing/memory harness; quantify instrumentation overhead and Python allocation effects.
Run four-queue synthetic and real-world experiments, preserve raw data and analyze variability.
Today’s demonstration is lightweight and reproducible; final timing, memory and statistical conclusions remain incomplete.
