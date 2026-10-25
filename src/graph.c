#include "graph.h"
#include <limits.h>
#include <stdint.h>
#include <stdlib.h>
typedef struct { int *items; size_t count, capacity; } Adjacency;
struct Graph { size_t n; bool directed; Adjacency *adj; };
GraphStatus graph_create(size_t n, bool directed, Graph **out)
{
    Graph *g;
    if (!out) return GRAPH_INVALID_ARGUMENT;
    *out = NULL;
    if (!n || n > INT_MAX || n > SIZE_MAX / sizeof(Adjacency))
        return GRAPH_INVALID_ARGUMENT;
    g = malloc(sizeof(*g));
    if (!g) return GRAPH_NO_MEMORY;
    g->adj = calloc(n, sizeof(*g->adj));
    if (!g->adj) { free(g); return GRAPH_NO_MEMORY; }
    g->n = n;
    g->directed = directed;
    *out = g;
    return GRAPH_OK;
}
static GraphStatus reserve_one(Adjacency *a)
{
    size_t capacity;
    int *items;
    if (a->count < a->capacity) return GRAPH_OK;
    if (a->capacity > SIZE_MAX / sizeof(int) / 2) return GRAPH_NO_MEMORY;
    capacity = a->capacity ? a->capacity * 2 : 4;
    items = realloc(a->items, capacity * sizeof(int));
    if (!items) return GRAPH_NO_MEMORY;
    a->items = items;
    a->capacity = capacity;
    return GRAPH_OK;
}
GraphStatus graph_add_edge(Graph *g, int from, int to)
{
    bool reverse;
    if (!g || from < 0 || to < 0 || (size_t)from >= g->n || (size_t)to >= g->n)
        return GRAPH_INVALID_ARGUMENT;
    reverse = !g->directed && from != to;
    if (reserve_one(&g->adj[from]) != GRAPH_OK) return GRAPH_NO_MEMORY;
    if (reverse && reserve_one(&g->adj[to]) != GRAPH_OK) return GRAPH_NO_MEMORY;
    g->adj[from].items[g->adj[from].count++] = to;
    if (reverse) g->adj[to].items[g->adj[to].count++] = from;
    return GRAPH_OK;
}
size_t graph_vertex_count(const Graph *g) { return g ? g->n : 0; }
bool graph_is_directed(const Graph *g) { return g && g->directed; }
const int *graph_neighbors(const Graph *g, int vertex, size_t *count)
{
    if (count) *count = 0;
    if (!g || !count || vertex < 0 || (size_t)vertex >= g->n) return NULL;
    *count = g->adj[vertex].count;
    return g->adj[vertex].items;
}
void graph_destroy(Graph *g)
{
    if (!g) return;
    for (size_t i = 0; i < g->n; ++i) free(g->adj[i].items);
    free(g->adj);
    free(g);
}
