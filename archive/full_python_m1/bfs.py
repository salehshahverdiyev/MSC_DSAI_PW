def bfs(graph, source, queue_class, trace=False):
    graph.check_vertex(source)
    queue = queue_class()
    distances = [-1] * len(graph)
    distances[source] = 0
    queue.enqueue(source)
    counters = {"visited": 0, "enqueue_count": 1,
                "dequeue_count": 0, "frontier_peak": 1}
    if trace:
        print("enqueue", source, "queue =", queue.to_list())

    while not queue.is_empty():
        current = queue.dequeue()
        counters["dequeue_count"] += 1
        counters["visited"] += 1
        if trace:
            print("dequeue", current, "queue =", queue.to_list())

        for neighbor in graph.neighbors(current):
            if distances[neighbor] != -1:
                continue
            distances[neighbor] = distances[current] + 1
            queue.enqueue(neighbor)
            counters["enqueue_count"] += 1
            if len(queue) > counters["frontier_peak"]:
                counters["frontier_peak"] = len(queue)
            if trace:
                print("enqueue", neighbor, "queue =", queue.to_list())

    return distances, counters
