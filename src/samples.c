#include "samples.h"
GraphStatus sample_graph(SampleKind kind, Graph **out)
{
    GraphStatus status;
    Graph *g = NULL;
    /* Diamond has two routes to 3, a cycle back to 0, and isolated vertex 5. */
    const int edges[][2] = {{0,1},{0,2},{1,3},{2,3},{3,0},{3,4}};
    if (!out) return GRAPH_INVALID_ARGUMENT;
    *out = NULL;
    if (kind < SAMPLE_PATH || kind > SAMPLE_DIAMOND) return GRAPH_INVALID_ARGUMENT;
    status = graph_create(6, kind == SAMPLE_DIAMOND, &g);
    if (status != GRAPH_OK) return status;
    if (kind == SAMPLE_DIAMOND) {
        for (size_t i = 0; i < sizeof(edges)/sizeof(edges[0]); ++i) {
            status = graph_add_edge(g, edges[i][0], edges[i][1]);
            if (status != GRAPH_OK) goto fail;
        }
    } else {
        for (int v = 1; v < 6; ++v) {
            int parent = 0; /* Star: every leaf connects to the center. */
            if (kind == SAMPLE_PATH) parent = v - 1;
            status = graph_add_edge(g, parent, v);
            if (status != GRAPH_OK) goto fail;
        }
    }
    *out = g;
    return GRAPH_OK;
fail:
    graph_destroy(g);
    return status;
}
const int *sample_distances(SampleKind kind)
{
    static const int expected[][6] = {{0,1,2,3,4,5},{0,1,1,1,1,1},{0,1,1,2,3,-1}};
    return kind >= SAMPLE_PATH && kind <= SAMPLE_DIAMOND ? expected[kind] : NULL;
}
const char *sample_name(SampleKind kind)
{
    switch (kind) {
    case SAMPLE_PATH: return "path (undirected)";
    case SAMPLE_STAR: return "star (undirected)";
    case SAMPLE_DIAMOND: return "diamond/cycle + isolated vertex (directed)";
    default: return "invalid";
    }
}
