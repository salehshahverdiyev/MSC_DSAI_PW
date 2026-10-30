class Graph:
    def __init__(self, vertex_count, directed=False):
        if type(vertex_count) is not int or vertex_count < 1:
            raise ValueError("vertex count must be a positive integer")
        self.directed = directed
        self.adjacency = []
        for vertex in range(vertex_count):
            self.adjacency.append([])  # A separate list for each vertex.

    def __len__(self):
        return len(self.adjacency)

    def check_vertex(self, vertex):
        if type(vertex) is not int or vertex < 0 or vertex >= len(self):
            raise ValueError("vertex must be an integer in 0..vertex_count-1")

    def add_edge(self, source, target):
        self.check_vertex(source)
        self.check_vertex(target)
        self.adjacency[source].append(target)
        if not self.directed and source != target:
            self.adjacency[target].append(source)

    def neighbors(self, vertex):
        self.check_vertex(vertex)
        return self.adjacency[vertex]