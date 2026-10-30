def bfs(graph, start, queue_class):
    if start < 0 or start >= len(graph):
        raise ValueError("start vertex is outside the graph")
    distances = [-1] * len(graph)
    distances[start] = 0
    queue = queue_class()
    queue.enqueue(start)

    while not queue.is_empty():
        vertex = queue.dequeue()
        for neighbor in graph[vertex]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[vertex] + 1
                queue.enqueue(neighbor)

    return distances
