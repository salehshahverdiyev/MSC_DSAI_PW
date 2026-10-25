#include "bfs.h"
#include "samples.h"
#include <assert.h>
#include <stdint.h>
#include <stdio.h>

/* Independent oracle: repeated edge relaxation, no queue or BFS scheduling. */
static void reference(const Graph *g, int source, int *dist)
{
    size_t n = graph_vertex_count(g);
    for (size_t v = 0; v < n; ++v) dist[v] = -1;
    dist[source] = 0;
    for (size_t pass = 0; pass < n; ++pass) {
        for (size_t u = 0; u < n; ++u) {
            size_t count;
            const int *adj = graph_neighbors(g, (int)u, &count);
            if (dist[u] < 0) continue;
            for (size_t e = 0; e < count; ++e) {
                int v = adj[e];
                if (dist[v] == -1 || dist[v] > dist[u]+1) dist[v] = dist[u]+1;
            }
        }
    }
}
static void check(const Graph *g, int source, const int *hand)
{
    int expected[32], actual[32];
    size_t n = graph_vertex_count(g), reached = 0;
    assert(n <= 32);
    reference(g, source, expected);
    for (size_t i = 0; i < n; ++i) {
        if (hand) assert(expected[i] == hand[i]);
        if (expected[i] >= 0) ++reached;
    }
    for (int k = 0; k < 3; ++k) {
        BfsStats stats;
        assert(bfs(g, source, (QueueKind)k, actual, n, &stats) == QUEUE_OK);
        for (size_t i = 0; i < n; ++i) assert(actual[i] == expected[i]);
        assert(stats.visited == reached && stats.enqueue_count == reached);
        assert(stats.dequeue_count == reached && stats.frontier_peak >= 1);
        assert(stats.frontier_peak <= reached);
        if (hand) {
            size_t peak = hand[5] == 5 ? 1 : (hand[5] == 1 ? 5 : 2);
            assert(stats.frontier_peak == peak);
        }
    }
}
int main(void)
{
    Graph *g = NULL;
    BfsStats stats;
    int dist[32];
    size_t count = 99;
    assert(graph_create(0, false, &g) == GRAPH_INVALID_ARGUMENT && !g);
    assert(graph_create(SIZE_MAX, false, &g) == GRAPH_INVALID_ARGUMENT && !g);
    assert(graph_create(1, false, NULL) == GRAPH_INVALID_ARGUMENT);
    assert(graph_add_edge(NULL, 0, 0) == GRAPH_INVALID_ARGUMENT);
    assert(!graph_neighbors(NULL, 0, &count) && count == 0);
    assert(graph_vertex_count(NULL) == 0 && !graph_is_directed(NULL));
    graph_destroy(NULL);
    for (int s = 0; s < 3; ++s) {
        assert(sample_graph((SampleKind)s, &g) == GRAPH_OK);
        assert(graph_is_directed(g) == (s == SAMPLE_DIAMOND));
        check(g, 0, sample_distances((SampleKind)s));
        check(g, 5, NULL); /* reverse traversal / isolated source */
        graph_destroy(g);
    }
    assert(graph_create(1, false, &g) == GRAPH_OK);
    assert(graph_add_edge(g, 0, 0) == GRAPH_OK);
    check(g, 0, NULL);
    assert(graph_add_edge(g, -1, 0) == GRAPH_INVALID_ARGUMENT);
    assert(graph_add_edge(g, 0, 1) == GRAPH_INVALID_ARGUMENT);
    assert(!graph_neighbors(g, 1, &count) && count == 0);
    assert(!graph_neighbors(g, 0, NULL));
    assert(bfs(NULL, 0, QUEUE_LINKED_LIST, dist, 32, &stats) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, -1, QUEUE_LINKED_LIST, dist, 32, &stats) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, 1, QUEUE_LINKED_LIST, dist, 32, &stats) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, 0, QUEUE_LINKED_LIST, dist, 0, &stats) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, 0, QUEUE_LINKED_LIST, NULL, 32, &stats) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, 0, QUEUE_LINKED_LIST, dist, 32, NULL) == QUEUE_INVALID_ARGUMENT);
    assert(bfs(g, 0, QUEUE_CIRCULAR_INCREMENTAL, dist, 32, &stats) == QUEUE_UNSUPPORTED);
    graph_destroy(g);
    /* Independently generated directed/undirected cases; every source checked. */
    {
        uint32_t seed = 1030;
        for (int trial = 0; trial < 100; ++trial) {
            assert(graph_create(16, trial % 2 != 0, &g) == GRAPH_OK);
            for (int u = 0; u < 16; ++u) {
                for (int v = 0; v < 16; ++v) {
                    seed = seed * UINT32_C(1664525) + UINT32_C(1013904223);
                    if ((seed >> 24) < 30) assert(graph_add_edge(g, u, v) == GRAPH_OK);
                }
            }
            for (int source = 0; source < 16; ++source) check(g, source, NULL);
            graph_destroy(g);
        }
    }
    puts("BFS tests: PASS (hand examples, singleton/errors; 100 graphs x 16 sources x 3 queues vs relaxation oracle)");
    return 0;
}
