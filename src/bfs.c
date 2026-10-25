#include "bfs.h"
QueueStatus bfs(const Graph *g, int source, QueueKind kind, int *dist,
                size_t length, BfsStats *stats)
{
    size_t n = graph_vertex_count(g);
    Queue *q = NULL;
    QueueStatus status;
    if (!g || !dist || !stats || source < 0 || (size_t)source >= n || length < n)
        return QUEUE_INVALID_ARGUMENT;
    status = queue_create(kind, &q);
    if (status != QUEUE_OK) return status;
    *stats = (BfsStats){0};
    for (size_t i = 0; i < n; ++i) dist[i] = -1;
    status = queue_enqueue(q, source);
    if (status != QUEUE_OK) goto done;
    dist[source] = 0;
    stats->enqueue_count = stats->frontier_peak = 1;
    while (!queue_is_empty(q)) {
        int u;
        size_t count;
        const int *neighbors;
        status = queue_dequeue(q, &u);
        if (status != QUEUE_OK) goto done;
        ++stats->dequeue_count;
        ++stats->visited;
        neighbors = graph_neighbors(g, u, &count);
        for (size_t i = 0; i < count; ++i) {
            int v = neighbors[i];
            if (dist[v] != -1) continue;
            status = queue_enqueue(q, v);
            if (status != QUEUE_OK) goto done;
            dist[v] = dist[u] + 1;
            ++stats->enqueue_count;
            if (queue_size(q) > stats->frontier_peak)
                stats->frontier_peak = queue_size(q);
        }
    }
done:
    queue_destroy(q);
    return status;
}
