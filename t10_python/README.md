# Active Python implementation
See [root README](../README.md) for commands, status and checkpoint links.

- queues.py: explicit array and node operations, with counters next to executed work.
- graph.py: path, star, binary-tree and rectangular-grid adjacency-list generators.
- bfs.py: single adjacency-list BFS; queue class is the only implementation choice.
- demo.py: four hand-verified small graphs and optional local dataset comparison.
- dataset.py: strict directed summed-link loader, provenance hash and counts.
- tests/test_basic.py: deterministic boundary and hand-answer checks.
- tests/test_evidence.py: seeded queue oracle, independent distances, counters, loader and optional real graph checks.
- __init__.py: package marker.

Python approval from Professor Pavel is unconfirmed.

Arrays retain capacity after draining. Linked capacity is None. The normal demo is not a benchmark. Do not use work counts as time or bytes.
