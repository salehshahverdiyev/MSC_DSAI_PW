"""Build synthetic graphs and load C. elegans as plain adjacency lists."""
from pathlib import Path
import hashlib
import math



def path_graph(n):
    """n vertices connected in a line; n must be a nonnegative integer."""
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    graph = [[] for _ in range(n)]
    for vertex in range(1, n):
        graph[vertex - 1].append(vertex)
        graph[vertex].append(vertex - 1)
    return graph


def star_graph(n):
    """n vertices, center 0 joined to every leaf."""
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    graph = [[] for _ in range(n)]
    for leaf in range(1, n):
        graph[0].append(leaf)
        graph[leaf].append(0)
    return graph


def tree_graph(n):
    """Binary tree in level order: parent of child is (child - 1) // 2."""
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    graph = [[] for _ in range(n)]
    for child in range(1, n):
        parent = (child - 1) // 2
        graph[parent].append(child)
        graph[child].append(parent)
    return graph


def grid_graph(rows, columns):
    """Rectangular grid; vertex ID is row * columns + column."""
    if type(rows) is not int or type(columns) is not int or rows < 1 or columns < 1:
        raise ValueError("rows and columns must be positive integers")
    graph = [[] for _ in range(rows * columns)]
    for row in range(rows):
        for column in range(columns):
            vertex = row * columns + column
            if column + 1 < columns:
                right = vertex + 1
                graph[vertex].append(right)
                graph[right].append(vertex)
            if row + 1 < rows:
                below = vertex + columns
                graph[vertex].append(below)
                graph[below].append(vertex)
    return graph


def load_worm(filename, vertex_count=279):
    """Read i j weight as directed j -> i; retain positive edges for hop BFS."""
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


def load_brainlinks(filename, edge_limit=100):
    """Load a bounded, compact sample from a two-column directed edge list.

    The returned graph contains only vertices occurring in the first
    ``edge_limit`` unique edges.  ``summary["labels"]`` maps compact vertex
    indexes back to the IDs in the source file.
    """
    if type(edge_limit) is not int or edge_limit < 1:
        raise ValueError("edge_limit must be a positive integer")

    edges = []
    seen = set()
    rows = 0
    duplicates = 0
    with Path(filename).open(encoding="ascii") as stream:
        for number, line in enumerate(stream, 1):
            if len(edges) >= edge_limit:
                break
            if not line.strip():
                continue
            fields = line.split()
            if len(fields) != 2:
                raise ValueError(f"line {number}: expected two columns")
            try:
                source, target = (int(value) for value in fields)
            except ValueError as error:
                raise ValueError(f"line {number}: vertex IDs must be integers") from error
            if source < 0 or target < 0:
                raise ValueError(f"line {number}: vertex IDs must be nonnegative")
            rows += 1
            edge = (source, target)
            if edge in seen:
                duplicates += 1
                continue
            seen.add(edge)
            edges.append(edge)

    if not edges:
        raise ValueError("dataset contains no connection rows")

    labels = sorted({vertex for edge in edges for vertex in edge})
    indexes = {label: index for index, label in enumerate(labels)}
    graph = [[] for _ in labels]
    for source, target in edges:
        graph[indexes[source]].append(indexes[target])
    return graph, {"vertices": len(labels), "edges": len(edges),
                   "rows": rows, "duplicates": duplicates, "labels": labels}
