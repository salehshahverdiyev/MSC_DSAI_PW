#ifndef T10_BFS_H
#define T10_BFS_H
#include "graph.h"
#include "queue.h"
typedef struct { size_t visited, enqueue_count, dequeue_count, frontier_peak; } BfsStats;
/* Caller supplies dist with at least graph_vertex_count(g) slots and stats.
 * Distances: -1 unreachable; dist[source]=0. On failure output may be partial, never
 * use it as a completed traversal. Inputs/creation validated before writing.
 */
QueueStatus bfs(const Graph *g, int source, QueueKind kind, int *dist,
                size_t length, BfsStats *stats);

/* Optional teaching observer, called synchronously AFTER each successful queue
 * operation and its distance/counter update. It receives values, not ownership.
 * context belongs to the caller and must remain valid until BFS returns.
 * Observer must not mutate/free the graph, distance array or stats, or reenter
 * BFS using those objects. NULL observer disables events; context may be NULL.
 * Failed BFS can emit a partial trace. This is diagnostic, not timed mode.
 */
typedef enum { BFS_ENQUEUE, BFS_DEQUEUE } BfsEvent;
typedef void (*BfsObserver)(BfsEvent event, int vertex, int distance,
                            size_t queue_size, void *context);
QueueStatus bfs_observed(const Graph *g, int source, QueueKind kind, int *dist,
                         size_t length, BfsStats *stats,
                         BfsObserver observer, void *context);
#endif
