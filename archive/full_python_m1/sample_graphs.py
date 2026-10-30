from .graph import Graph
from .generators import path, star


def diamond():
    graph = Graph(6, directed=True)
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 0), (3, 4)]
    for source, target in edges:
        graph.add_edge(source, target)
    # Vertex 5 exists but has no incident edges.
    return graph


def examples():
    # Each tuple: display name, graph, expected distances, expected queue peak.
    return [
        ("path", path(6), [0, 1, 2, 3, 4, 5], 1),
        ("star", star(6), [0, 1, 1, 1, 1, 1], 5),
        ("diamond", diamond(), [0, 1, 1, 2, 3, -1], 2),
    ]
