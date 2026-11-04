"""Load the directed positive-weight projection of NADINE summed links."""
from pathlib import Path
import hashlib
import math


def load_worm(filename, vertex_count=279):
    # 279 comes from the source matrix page, including any isolated vertices.
    raw = Path(filename).read_bytes()
    graph = [[] for _ in range(vertex_count)]
    seen = set()
    rows = 0
    duplicates = 0
    nonpositive = 0
    identifiers = set()
    for number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("//"):
            continue
        fields = line.split()
        try:
            if len(fields) != 3:
                raise ValueError("expected three columns")
            target, source = int(fields[0]), int(fields[1])
            weight = float(fields[2])
            if not (1 <= source <= vertex_count and 1 <= target <= vertex_count):
                raise ValueError("ID outside declared vertex range")
            if not math.isfinite(weight):
                raise ValueError("nonfinite weight")
        except ValueError as error:
            raise ValueError(f"line {number}: {error}") from error
        rows += 1
        identifiers.update((source, target))
        if weight <= 0:
            nonpositive += 1
            continue
        edge = (source - 1, target - 1)
        if edge in seen:
            duplicates += 1
            continue
        seen.add(edge)
        graph[edge[0]].append(edge[1])
    if rows == 0:
        raise ValueError("dataset contains no connection rows")
    return graph, {"vertices": vertex_count, "observed_ids": len(identifiers),
                   "rows": rows, "edges": len(seen), "duplicates": duplicates,
                   "nonpositive": nonpositive,
                   "self_loops": sum(a == b for a, b in seen),
                   "sha256": hashlib.sha256(raw).hexdigest()}
