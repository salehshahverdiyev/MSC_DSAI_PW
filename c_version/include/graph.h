#ifndef T10_GRAPH_H
#define T10_GRAPH_H
#include <stdbool.h>
#include <stddef.h>
typedef enum { GRAPH_OK, GRAPH_INVALID_ARGUMENT, GRAPH_NO_MEMORY } GraphStatus;
typedef struct Graph Graph;
/* Owns adjacency arrays; n in [1, INT_MAX]. Neighbors keep insertion order.
 * Duplicate edges allowed; undirected self-loop stored once. Failed add leaves
 * edges unchanged (reserved capacity may grow). Output cleared on create failure.
 */
GraphStatus graph_create(size_t n, bool directed, Graph **out);
GraphStatus graph_add_edge(Graph *g, int from, int to);
size_t graph_vertex_count(const Graph *g);
bool graph_is_directed(const Graph *g);
/* Borrowed neighbor storage, valid until graph mutation/destruction.
 * NULL/invalid inputs return NULL and set *count=0 if count is non-NULL. */
const int *graph_neighbors(const Graph *g, int vertex, size_t *count);
void graph_destroy(Graph *g);
#endif
