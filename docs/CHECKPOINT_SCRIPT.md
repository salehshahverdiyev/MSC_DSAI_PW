# Five-minute speaking script
Suggested split: Javidan slides 1–3, Saleh slides 4–6. Both should rehearse all code.

## 0:00–0:45 — Slide 1
Our project studies how the queue inside BFS changes cost when graph structure changes. We compare a shifting array, a linked list, circular doubling and eventually incremental resizing. Our research question includes average time, the worst single operation, and memory. Today we present three working baselines, correctness evidence and a draft experiment plan. We have not measured final performance. Our temporary computer is modest, so the checkpoint uses small graphs and standard-library Python.

## 0:45–1:35 — Slide 2
Each queue has enqueue, dequeue and is_empty. Removing from an empty queue raises the same IndexError. The shifting queue stores the first item at index zero and moves all remaining items left on removal. The linked queue keeps head and tail pointers. When removing its last node, it also clears tail. The circular queue advances a front index instead of shifting. When full, it doubles and copies items in logical FIFO order. Doubling is amortized constant work per enqueue, but one growth operation copies every live item. Incremental resizing remains design work, and we do not claim its guarantee yet.

## 1:35–2:25 — Slide 3
The same BFS accepts a queue class, creates it and enqueues the source. Distances start at minus one. When we discover a neighbor, we assign its distance before enqueueing. This prevents duplicate insertion even when several edges reach it. FIFO ensures that a shorter layer is processed first. A path keeps only one pending vertex; a star creates a broad frontier immediately. Our small tree gives another frontier pattern. The real neural graph is directed: the file says column j points to column i. We ignore positive weight magnitude because this BFS measures edge counts, not weighted shortest paths.

## 2:25–3:20 — Slide 4
Our tests compare queue results with Python deque, but the production code does not use deque. We also verify BFS using repeated edge relaxation, a separate method. Tests cover empty queues, repeated growth, wrap-around, interleavings and malformed dataset rows. All eleven tests pass. The counters increase next to actual assignments. On our six-vertex path there are no shifts or resize copies. The star causes ten shifts in the shifting queue and four copies in each array queue. These are exact algorithmic counts. They do not measure time, allocator work or bytes. All queues return the same distances.

## 3:20–4:15 — Slide 5
Our hypotheses are written before timing. We expect broad frontiers to penalize shifting, doubling to create copy spikes, and incremental migration to trade smoother copying for complexity and memory. We propose paired comparisons on identical graph instances, sources and adjacency order. We will use warm-ups, repeated runs and balanced queue order. We will report median and variability, preserving failures and timeouts. Throughput, operation latency and memory need separate measurements because instrumentation affects the program. We will finalize sizes and resource caps in a small feasibility pilot, then obtain approval and freeze the protocol before final experiments.

## 4:15–5:00 — Slide 6
The main unfinished implementation is incremental resizing. The idea is to keep old and new buffers temporarily, place new items after older logical items, and migrate only bounded work on each operation. We must prove ownership, FIFO order and that migration finishes before another growth is required. Even then, allocating a Python list initializes many slots, so bounded copying alone cannot prove constant wall-clock latency. Next we will complete that proof and implementation, freeze the protocol, and collect timing and memory data on synthetic and real graphs. Today we can defend the three baselines and their correctness evidence.
