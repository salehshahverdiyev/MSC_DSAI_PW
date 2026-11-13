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

Run the work-counter comparison across four synthetic shapes and a genuine
Brainlinks directed edge sample:

```powershell
python -m t10.real_demo --dataset brainlinks.dat --edges 40
python -m t10.real_demo --dataset brainlinks.dat --edges 1000 --no-svg
```

For each graph, an aligned table lists all four queues, correctness, visited
count, peak queue occupancy, shifted/copied elements, and resize events.
These are algorithmic work counters, not timing benchmarks. The small default
also writes SVGs; use `--output-dir bfs_visualizations` to choose the directory
or `--no-svg` to skip files for larger samples. Synthetic shapes are independent
40-vertex graphs, not real networks with substituted labels.

## Run tests

```powershell
python -m unittest discover -s t10\tests -v
```

The tests verify FIFO behavior, empty-queue errors, circular wrap-around,
incremental migration, BFS distances, graph loading, metrics, and SVG output.

## Complexity

For an adjacency-list graph with `V` vertices and `E` edges:

- Graph storage: `O(V + E)`
- BFS traversal time: `O(V + E)` assuming constant-time queue operations;
  the shifting queue adds its shifting work
- BFS auxiliary space: `O(V)`

Queue operation characteristics:

| Queue | Enqueue | Dequeue | Main cost |
|---|---:|---:|---|
| Shifting array | `O(1)` amortized | `O(n)` | shifts remaining elements |
| Linked list | `O(1)` | `O(1)` | node allocation |
| Circular doubling | `O(1)` amortized | `O(1)` | full copy during growth |
| Incremental circular | normally `O(1)` | normally `O(1)` | migration bookkeeping |

The retained `measure_bfs` helper provides illustrative whole-run time and
traced memory; the checkpoint CLI displays work counters. Worst-case O(1) for
the incremental queue is not established because pending-buffer growth can
copy all pending elements in one operation.

## Data

`brainlinks.dat` is a local two-column directed edge list. The real-data demo
loads a bounded number of unique edges and compacts their vertex IDs for
visualization. The checked-in local file contains 1,960,108 rows, 957,853
unique directed edges, and 10,000 vertices. The default uses 40 unique edges;
`--edges 1000` selects a larger genuine prefix sample, not a random sample.
External provenance and redistribution permission have not been verified.

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
│   ├── real_demo.py    work comparison and SVG generation
│   ├── README.md       detailed T10 report
│   └── tests/          deterministic test suite
├── brainlinks.dat      local real graph data
├── RUN.txt             dataset and execution notes
└── README.md           project overview
```
