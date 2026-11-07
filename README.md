# MSC DSAI Practical Work

This project investigates queue implementations used by breadth-first search
(BFS), with a focus on average work, resizing cost, memory, and worst-case
operation behavior on graphs with different structures.

The current T10 implementation compares four FIFO queues:

1. `ShiftingArrayQueue`
2. `LinkedListQueue`
3. `CircularArrayQueue`
4. `IncrementalCircularArrayQueue`

See the detailed T10 explanation in [`t10/README.md`](./t10/README.md).

## Requirements

- Python 3.10 or newer
- Standard library only

The repository includes a local virtual environment in some development
setups. If available, use:

```powershell
.\.venv\Scripts\python.exe
```

Otherwise use `python`.

## Run the demonstrations

Run the small correctness and work-counter demo:

```powershell
python -m t10.demo
```

Run the measured comparison across Path, Star, Binary tree, Grid, and a
Brainlinks sample:

```powershell
python -m t10.real_demo --dataset brainlinks.dat --edges 40
```

The measured demo reports, for every graph and queue:

- BFS correctness
- elapsed time
- peak traced Python memory
- peak queue size
- enqueue/dequeue counts
- shifted and copied elements
- resize events

It also writes one SVG visualization per graph. Choose another output
directory with `--output-dir`:

```powershell
python -m t10.real_demo `
  --dataset brainlinks.dat `
  --edges 40 `
  --output-dir bfs_visualizations
```

## Run tests

```powershell
python -m unittest discover -s t10\tests -v
```

The tests verify FIFO behavior, empty-queue errors, circular wrap-around,
incremental migration, BFS distances, graph loading, metrics, and SVG output.

## Complexity

For an adjacency-list graph with `V` vertices and `E` edges:

- Graph storage: `O(V + E)`
- BFS time: `O(V + E)`
- BFS auxiliary space: `O(V)`

Queue operation characteristics:

| Queue | Enqueue | Dequeue | Main cost |
|---|---:|---:|---|
| Shifting array | `O(1)` amortized | `O(n)` | shifts remaining elements |
| Linked list | `O(1)` | `O(1)` | node allocation |
| Circular doubling | `O(1)` amortized | `O(1)` | full copy during growth |
| Incremental circular | normally `O(1)` | normally `O(1)` | migration bookkeeping |

The measured time and memory values are empirical and depend on the machine,
Python runtime, graph size, and workload.

## Data

`brainlinks.dat` is a local two-column directed edge list. The real-data demo
loads a bounded number of unique edges and compacts their vertex IDs for
visualization. The original dataset is not redistributed by this project.

The optional C. elegans dataset instructions and expected metadata are in
[`RUN.txt`](./RUN.txt).

## Project structure

```text
MSC_DSAI_PW/
├── t10/
│   ├── bfs.py          BFS implementation
│   ├── demo.py         correctness and work-counter demo
│   ├── graph.py        graph generators and data loaders
│   ├── queues.py       four queue implementations
│   ├── real_demo.py    measured comparison and SVG generation
│   ├── README.md       detailed T10 report
│   └── tests/          deterministic test suite
├── brainlinks.dat      local real graph data
├── RUN.txt             dataset and execution notes
└── README.md           project overview
```
