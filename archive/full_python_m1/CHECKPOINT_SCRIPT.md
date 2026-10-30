Archived reference script; the active two-queue prototype is in t10_python/.

# Five-minute oral script — primary Python implementation

This is a suggested talk, not a claim that Python or a protocol freeze has been
approved. Adapt the language to what you actually understand and verified.

## 0:00–0:45 — Question and honest status

“Our project asks how four FIFO queue designs behave inside BFS on different
graph structures, including a real network. We care about average operation
time, slow individual operations and memory, especially when a growing frontier
forces storage to resize. Python is now our main project, with three working
baseline queues. Our C prototype is preserved in c_version/ as a reference.
We still need confirmation that Python
is permitted for the final experiments.”

## 0:45–1:30 — Graph, BFS and FIFO

“A graph has vertices and edges. BFS starts at a source and discovers vertices
in layers of increasing number of edges from that source. A FIFO queue stores
discovered vertices that are waiting. First in, first out keeps that layer order.
We use adjacency lists, so we inspect just the current vertex's neighbors. We
keep one BFS and change only its queue class.”

## 1:30–2:20 — Three working queues, fourth still required

“The shifting array keeps its front at index zero. On removal an explicit loop
moves all remaining references left, so large occupancy means more work.
The linked list appends at a tail node and removes the head with constant
reference updates, although allocation/interpreter costs still affect timing.
The circular array wraps indices using modulo. When full it creates twice the
capacity and copies logical FIFO order. Ordinary operations are constant work,
but a growth operation is linear; amortized means a bound across a sequence.
The fourth queue should migrate incrementally, but is not implemented yet.”

## 2:20–3:20 — Live demonstration

From the repository root in WSL:

```sh
python3 -m unittest discover -s archive/full_python_m1/tests -v
python3 -m archive.full_python_m1.demo
```

Exact PowerShell demo command on the development PC:

```powershell
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m archive.full_python_m1.demo
```

“Here the three queues agree on the hand-worked distances. The path has peak
queue size one; the star has five pending leaves after the center is processed.
The directed diamond tests shared discoveries and a cycle; isolated vertex five
keeps distance minus one. Now the actual star walkthrough shows each enqueue
and dequeue. The leaves leave in discovery order. Its distances are zero then
five ones. These counters are correctness observations, not timing results.”

## 3:20–4:10 — Correctness and planned measurements

“The queue tests use deque only as an independent test reference. We run 50,000
seeded operations per baseline, including wrap and resize. BFS tests compare
against hand examples and repeated edge relaxation, without our queues: 100
graphs, 16 sources and three queues. Tests are evidence, not an exhaustive proof.
Later we will use identical graph/source/order inputs, warm-up and repeated
paired runs, report medians and distributions, and record timeouts and memory
limits. Batch averages and the slowest individual observations are different
measurements. Interpreter, garbage collector and allocator effects need reporting.”

## 4:10–5:00 — Memory, migration and remaining work

“Python lists contain references and node objects have overhead. Capacity and
unused slots matter, but do not by themselves measure total bytes. We plan
defined structural accounting and separate allocation diagnostics. Our current
real-graph candidate is the NADINE C. elegans neural network, not yet loaded.
Incremental resizing must preserve FIFO across old/new buffers and finish before
space runs out. In Python even creating or releasing a large list may be linear,
so spreading copies alone is not the required full constant-work proof. We need
to resolve the storage model before claiming that bound. No benchmark results
exist yet and the protocol is DRAFT. We want feedback on language permission,
the candidate dataset and the experimental model before finalizing the study.”

