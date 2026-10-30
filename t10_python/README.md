# Main Python learning prototype

Only two queues, one BFS and two small graphs are active here. This is a learning
prototype, not the completed four-queue T10 assignment.

From the repository root (use python3 in WSL if necessary):

```sh
python -m t10_python.demo
python -m unittest discover -s t10_python/tests -v
```

Read `demo.py` first: each graph is simply a list of neighbor lists. It selects
one queue class, calls the same `bfs` function and checks a hand-worked answer.
`bfs.py` assigns distances on discovery and processes pending vertices FIFO.
`queues.py` contains explicit shifting and circular-doubling implementations.
Both expose enqueue, dequeue and is_empty; empty removal raises IndexError.
Arrays start at capacity 4, double when full, and do not shrink. Ring removal
advances front modulo capacity; shifting removal moves every remaining entry.

Expected distances with both queues, starting at vertex 0:

- Path: `[0, 1, 2, 3, 4, 5]`
- Star: `[0, 1, 1, 1, 1, 1]`

Essential tests cover empty/FIFO/refill, multiple growths, wrapped growth, hand
BFS distances, unreachable vertices and invalid starting ranges. The BFS assumes
valid adjacency lists and integer IDs; it is not a general graph-input validator.

The complete previous Python implementation is preserved in
[archive/full_python_m1/](../archive/full_python_m1/README.md). It includes the
linked queue and more extensive tests/generators. The final assignment also
requires incremental resizing/proof, real-world data and controlled timing,
latency/memory experiments. None is claimed by this simplified active version.
The C reference in c_version/ remains separate and untouched.
