# T10 - Python checkpoint project
UFAZ M1 Advanced Data Structures and Algorithms. Javidan Hajizada and Saleh Shahverdiyev.

Active project: t10_python/. Three simple baselines share enqueue, dequeue and is_empty; empty dequeue raises IndexError. Shifting and circular arrays start at capacity 4 and double without shrinking. The C and archived Python versions have been removed from the working tree. All 37 files were verified against Git history at commit `67559fc98fa604b45f59644d9a5b29a4b4a9213e` before removal and remain recoverable there.

Python is our intended implementation language; explicit approval from Professor Pavel is still unconfirmed.

Run from repository root with standard-library Python 3:

```powershell
python -m t10_python.demo
python -m unittest discover -s t10_python/tests -v
python -m t10_python.demo --dataset data/raw/ssumlinks.txt
```

On this computer the Windows python app alias does not work. An ignored portable CPython 3.13.1 runtime is available; replace python above with:

```powershell
./.local-tools/python/python.exe -m t10_python.demo
./.local-tools/python/python.exe -m unittest discover -s t10_python/tests -v
```

No WSL or third-party packages required. The portable runtime is local only, not a repository dependency.

Read demo.py, graph.py, bfs.py, queues.py, then dataset.py. BFS defaults to returning distances; with_stats=True additionally returns traversal and queue work diagnostics. Input must be valid adjacency lists with integer IDs 0..n-1. The dataset loader validates its input separately.

The demo checks hand answers on path, star, tree and grid. Optional real data stays ignored because redistribution permission is unconfirmed. Twelve tests cover FIFO against deque, empty behavior, wrapped growth, exact counts, independent repeated-relaxation shortest paths, seeded directed graphs and loader validation. The optional real-data test skips explicitly if the file is absent.

Work counters measure executed reference moves, completed growth events and occupancy, not elapsed time or bytes. Definitions and the unapproved experiment plan are in [EXPERIMENT_PROTOCOL.md](docs/EXPERIMENT_PROTOCOL.md).

Checkpoint materials: [six slides](docs/CHECKPOINT_SLIDES.md), [five-minute script](docs/CHECKPOINT_SCRIPT.md), [15 questions](docs/PAVEL_QUESTIONS.md). Real-data provenance and acquisition: [dataset record](docs/DATASET_DECISION.md). Incremental queue: [design only](docs/INCREMENTAL_DESIGN.md).

Final requirements remain: fourth queue and proof, approved frozen protocol, controlled timing and memory harness, four-queue experiments and rigorous statistical analysis. No final benchmarks have run. See PROJECT_OBJECTIVES.md for the full research scope; its broader workloads and multi-source features are objectives, not implemented checkpoint features.
