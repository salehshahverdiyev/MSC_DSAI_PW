def bfs(graph, start, queue_class, with_stats=False):
    if start < 0 or start >= len(graph):
        raise ValueError("start vertex is outside the graph")
    distances = [-1] * len(graph)
    distances[start] = 0
    queue = queue_class()
    queue.enqueue(start)

    visited = []
    enqueues = 1
    dequeues = 0
    while not queue.is_empty():
        vertex = queue.dequeue()
        visited.append(vertex)
        dequeues += 1
        for neighbor in graph[vertex]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[vertex] + 1
                queue.enqueue(neighbor)
                enqueues += 1

    if with_stats:
        return distances, {"visited": visited, "enqueues": enqueues,
                           "dequeues": dequeues, "peak": queue.max_size,
                           "shifted": queue.shifted_elements,
                           "copied": queue.copied_elements,
                           "resizes": queue.resize_events,
                           "capacity_history": queue.capacity_history}
    return distances
