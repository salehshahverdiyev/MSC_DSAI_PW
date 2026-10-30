#include "bfs.h"
#include "samples.h"
#include <stdio.h>

typedef struct { int pending[6]; size_t size; bool valid; } QueueDisplay;

static void show_event(BfsEvent event, int vertex, int distance,
                       size_t actual_size, void *context)
{
    QueueDisplay *display = context;
    if (!display->valid) return;
    if (event == BFS_ENQUEUE) {
        if (display->size == 6) { display->valid = false; return; }
        display->pending[display->size] = vertex;
        ++display->size;
    } else {
        if (display->size == 0 || display->pending[0] != vertex) {
            display->valid = false;
            return;
        }
        --display->size;
        for (size_t i = 0; i < display->size; ++i)
            display->pending[i] = display->pending[i + 1];
    }
    if (display->size != actual_size) { display->valid = false; return; }
    printf("  %-7s %d (distance=%d) queue=[",
           event == BFS_ENQUEUE ? "enqueue" : "process", vertex, distance);
    for (size_t i = 0; i < display->size; ++i)
        printf("%s%d", i ? "," : "", display->pending[i]);
    puts("]");
}

int main(void)
{
    Graph *graph = NULL;
    int distances[6];
    BfsStats stats;
    QueueDisplay display = {{0}, 0, true};
    if (sample_graph(SAMPLE_STAR, &graph) != GRAPH_OK) return 1;
    puts("BFS walkthrough: undirected star, source=0, queue=circular-doubling");
    puts("Queue shown front to back; events come from the actual BFS.");
    QueueStatus status = bfs_observed(graph, 0, QUEUE_CIRCULAR_DOUBLING,
                                      distances, 6, &stats, show_event, &display);
    graph_destroy(graph);
    if (status != QUEUE_OK || !display.valid || display.size != 0) return 1;
    printf("Distances:");
    for (int i = 0; i < 6; ++i) {
        if (distances[i] != sample_distances(SAMPLE_STAR)[i]) return 1;
        printf(" %d", distances[i]);
    }
    printf("\nvisited=%zu enq=%zu deq=%zu peak=%zu\n", stats.visited,
           stats.enqueue_count, stats.dequeue_count, stats.frontier_peak);
    puts("FIFO: vertices 1..5 leave in discovery order. This is not a benchmark.");
    return 0;
}
