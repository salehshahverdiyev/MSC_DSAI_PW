#ifndef T10_BFS_H
#define T10_BFS_H
#include "graph.h"
#include "queue.h"
typedef struct { size_t visited, enqueue_count, dequeue_count, frontier_peak; } BfsStats;
/* Caller supplies dist with at least graph_vertex_count(g) slots and stats.
 * Distances: -1 unreachable; source=0. On failure output may be partial, never
 * use it as a completed traversal. Inputs/creation validated before writing.
 */
QueueStatus bfs(const Graph *g, int source, QueueKind kind, int *dist,
                size_t length, BfsStats *stats);
#endif
