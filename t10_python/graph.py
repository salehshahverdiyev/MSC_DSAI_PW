"""Synthetic undirected graphs as ordinary adjacency lists, with IDs 0..n-1."""


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
