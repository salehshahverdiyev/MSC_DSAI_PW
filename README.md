# T10: simplified Python learning prototype

UFAZ Advanced Data Structures and Algorithms — Javidan Hajizada and Saleh Shahverdiyev.

> In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?

The main project in **t10_python/** is intentionally a small learning prototype:
**two queues**, one BFS, and path/star examples. It is not the complete assignment.

From the repository root with Python 3:

```sh
python -m t10_python.demo
python -m unittest discover -s t10_python/tests -v
```

Use `python3` on Linux/WSL if `python` is unavailable. On this Windows PC:

```powershell
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m t10_python.demo
wsl -d Ubuntu --cd /mnt/c/Users/javid/MSC_DSAI_PW -- python3 -m unittest discover -s t10_python/tests -v
```

## Read just three implementation files

- [demo.py](t10_python/demo.py): defines path/star adjacency lists, runs both queues and checks distances.
- [bfs.py](t10_python/bfs.py): one straightforward BFS using the chosen queue.
- [queues.py](t10_python/queues.py): shifting-array and circular-doubling queues.

Essential tests are in t10_python/tests/test_basic.py. No extra graph class,
observers, per-operation logging or benchmark framework is part of the active code.

## Preserved versions

```text
MSC_DSAI_PW/
├── t10_python/                 active two-queue learning prototype
├── archive/full_python_m1/     previous three-queue Python implementation/tests/docs
├── c_version/                  unchanged C reference
├── docs/DATASET_DECISION.md    shared real-world data plan
├── data/README.md
└── PROJECT_OBJECTIVES.md
```

The [full Python M1 archive](archive/full_python_m1/README.md) retains the linked
queue, graph class, generators, traces, research plan and independent randomized
correctness tests. It is reference material, not a second active implementation.
Run its tests with:

```sh
python -m unittest discover -s archive/full_python_m1/tests -v
```

The [C reference](c_version/README.md) remains independently runnable with
`make -C c_version test demo walkthrough` in a POSIX shell.

## Still required for the final assignment

The full T10 task requires **four queues**: shifting array, linked list, circular
doubling, and circular incremental resizing. Linked-list code is preserved in
the archive; incremental resizing and its FIFO/progress/work-bound proof remain
unfinished. The active prototype implements only the first and third designs.

Verified real-world graph loading, broader workloads, controlled paired timing,
individual-operation latency, memory including unused/temporary storage,
repetitions/distributions, fixed environment/seeds/caps, protocol freeze and final
defence work remain outside this prototype. No performance results exist.
See [shared objectives](PROJECT_OBJECTIVES.md), the [dataset decision](docs/DATASET_DECISION.md)
and the [archived DRAFT experiment plan](archive/full_python_m1/EXPERIMENT_PLAN.md).
