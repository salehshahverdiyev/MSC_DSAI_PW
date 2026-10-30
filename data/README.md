# Shared graph data

No real-world graph has been downloaded or loaded. The current candidate and
future acquisition/preprocessing plan are in [DATASET_DECISION.md](../docs/DATASET_DECISION.md).
Keep future shared raw downloads under data/raw/ (ignored), recording source,
retrieval date, hash, ID mapping, preprocessing counts and reachability checks.

The previous Python generators are preserved in archive/full_python_m1/generators.py.
The active prototype uses literal path/star adjacency lists. The preserved
C data notes are in [c_version/data/README.md](../c_version/data/README.md).
