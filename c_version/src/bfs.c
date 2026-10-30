#include "bfs.h"
QueueStatus bfs(const Graph *g, int source, QueueKind kind, int *dist,
                size_t length, BfsStats *stats)
{
    return bfs_observed(g, source, kind, dist, length, stats, NULL, NULL);
}

/* Same BFS for demo, tests and walkthrough; only the observer is optional. */
QueueStatus bfs_observed(const Graph *graph, int source, QueueKind kind, int *dist,
                         size_t length, BfsStats *stats,
                         BfsObserver observer, void *context)
{
    size_t vertex_count = graph_vertex_count(graph);
    Queue *queue = NULL;
    QueueStatus status;
    if (!graph || !dist || !stats || source < 0 ||
        (size_t)source >= vertex_count || length < vertex_count)
        return QUEUE_INVALID_ARGUMENT;
    status = queue_create(kind, &queue);
    if (status != QUEUE_OK) return status;

    /* -1 means undiscovered. Mark on enqueue so a cycle cannot enqueue twice. */
    *stats = (BfsStats){0};
    for (size_t i = 0; i < vertex_count; ++i) dist[i] = -1;
    status = queue_enqueue(queue, source);
    if (status != QUEUE_OK) goto done;
    dist[source] = 0;
    stats->enqueue_count = 1;
    stats->frontier_peak = 1;
    if (observer) observer(BFS_ENQUEUE, source, 0, queue_size(queue), context);

    /* FIFO processes vertices in nondecreasing distance from the source. */
    while (!queue_is_empty(queue)) {
        int current;
        size_t neighbor_count;
        const int *neighbors;
        status = queue_dequeue(queue, &current);
        if (status != QUEUE_OK) goto done;
        ++stats->dequeue_count;
        ++stats->visited;
        if (observer)
            observer(BFS_DEQUEUE, current, dist[current], queue_size(queue), context);

        neighbors = graph_neighbors(graph, current, &neighbor_count);
        for (size_t i = 0; i < neighbor_count; ++i) {
            int neighbor = neighbors[i];
            if (dist[neighbor] != -1) continue;
            status = queue_enqueue(queue, neighbor);
            if (status != QUEUE_OK) goto done;
            dist[neighbor] = dist[current] + 1;
            ++stats->enqueue_count;
            if (queue_size(queue) > stats->frontier_peak)
                stats->frontier_peak = queue_size(queue);
            if (observer)
                observer(BFS_ENQUEUE, neighbor, dist[neighbor], queue_size(queue), context);
        }
    }
done:
    /* One cleanup path for success and allocation/queue-operation failure. */
    queue_destroy(queue);
    return status;
}
