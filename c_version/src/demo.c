#include "bfs.h"
#include "samples.h"
#include <stdio.h>
int main(void)
{
    puts("T10 M1 correctness demo: source=0, distances by vertex ID; -1=unreachable");
    for (int s = 0; s < 3; ++s) {
        Graph *g = NULL;
        const int *expected = sample_distances((SampleKind)s);
        if (sample_graph((SampleKind)s, &g) != GRAPH_OK) return 1;
        puts(sample_name((SampleKind)s));
        for (int k = 0; k < 3; ++k) {
            int dist[6];
            BfsStats stats;
            if (bfs(g, 0, (QueueKind)k, dist, 6, &stats) != QUEUE_OK) {
                graph_destroy(g); return 1;
            }
            printf("  %-18s distances:", queue_kind_name((QueueKind)k));
            for (int i = 0; i < 6; ++i) {
                if (dist[i] != expected[i]) { graph_destroy(g); return 1; }
                printf(" %d", dist[i]);
            }
            printf(" | visited=%zu enq=%zu deq=%zu peak=%zu | hand-check PASS\n",
                stats.visited, stats.enqueue_count, stats.dequeue_count, stats.frontier_peak);
        }
        graph_destroy(g);
    }
    puts("Incremental queue: NOT IMPLEMENTED. No benchmark results collected.");
    return 0;
}
