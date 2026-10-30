from .graph import Graph


def path(vertex_count):
    graph = Graph(vertex_count)
    for vertex in range(1, vertex_count):
        graph.add_edge(vertex - 1, vertex)
    return graph


def star(vertex_count):
    graph = Graph(vertex_count)
    for vertex in range(1, vertex_count):
        graph.add_edge(0, vertex)
    return graph


def tree(vertex_count, branching=2):
    if type(branching) is not int or branching < 1:
        raise ValueError("branching must be a positive integer")
    graph = Graph(vertex_count)
    for vertex in range(1, vertex_count):
        parent = (vertex - 1) // branching
        graph.add_edge(parent, vertex)
    return graph


def grid(rows, columns):
    if type(rows) is not int or type(columns) is not int:
        raise ValueError("grid dimensions must be positive integers")
    if rows < 1 or columns < 1:
        raise ValueError("grid dimensions must be positive integers")
    graph = Graph(rows * columns)
    for row in range(rows):
        for column in range(columns):
            vertex = row * columns + column
            if column + 1 < columns:
                graph.add_edge(vertex, vertex + 1)
            if row + 1 < rows:
                graph.add_edge(vertex, vertex + columns)
    return graph
