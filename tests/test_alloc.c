/* Optional GNU-linker fault injection; production C code has no test hooks. */
#include "bfs.h"
#include "samples.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

void *__real_malloc(size_t n);
void *__real_calloc(size_t n, size_t size);
void *__real_realloc(void *p, size_t n);
static int active;
static size_t call_index, fail_index;
static int fail_now(void) { return active && call_index++ == fail_index; }
void *__wrap_malloc(size_t n) { return fail_now() ? NULL : __real_malloc(n); }
void *__wrap_calloc(size_t n, size_t s) { return fail_now() ? NULL : __real_calloc(n,s); }
void *__wrap_realloc(void *p, size_t n) { return fail_now() ? NULL : __real_realloc(p,n); }
static void arm(size_t index) { call_index = 0; fail_index = index; active = 1; }
static void disarm(void) { active = 0; }
static void check_queue(QueueKind kind)
{
    Queue *q = NULL;
    size_t allocations = kind == QUEUE_LINKED_LIST ? 1 : 2;
    int value;
    for (size_t i = 0; i < allocations; ++i) {
        arm(i);
        assert(queue_create(kind, &q) == QUEUE_NO_MEMORY && !q);
        disarm();
    }
    assert(queue_create(kind, &q) == QUEUE_OK);
    if (kind == QUEUE_LINKED_LIST) {
        assert(queue_enqueue(q, 3) == QUEUE_OK);
        arm(0);
        assert(queue_enqueue(q, 4) == QUEUE_NO_MEMORY);
        disarm();
        assert(queue_size(q) == 1);
        assert(queue_dequeue(q, &value) == QUEUE_OK && value == 3);
    } else {
        size_t capacity;
        for (int i = 0; i < 4; ++i) assert(queue_enqueue(q, i) == QUEUE_OK);
        assert(queue_dequeue(q, &value) == QUEUE_OK && value == 0);
        assert(queue_enqueue(q, 4) == QUEUE_OK); /* ring now wrapped/full */
        arm(0);
        assert(queue_enqueue(q, 5) == QUEUE_NO_MEMORY);
        disarm();
        assert(queue_size(q) == 4);
        assert(queue_capacity(q, &capacity) == QUEUE_OK && capacity == 4);
        for (int i = 1; i <= 4; ++i)
            assert(queue_dequeue(q, &value) == QUEUE_OK && value == i);
    }
    assert(queue_enqueue(q, 9) == QUEUE_OK); /* recovery after failure */
    queue_destroy(q);
}
int main(void)
{
    Graph *g = NULL;
    size_t count;
    for (int k = 0; k < 3; ++k) check_queue((QueueKind)k);
    for (size_t i = 0; i < 2; ++i) {
        arm(i);
        assert(graph_create(2, false, &g) == GRAPH_NO_MEMORY && !g);
        disarm();
        assert(graph_create(2, false, &g) == GRAPH_OK);
        arm(i); /* fail first or reverse adjacency allocation */
        assert(graph_add_edge(g, 0, 1) == GRAPH_NO_MEMORY);
        disarm();
        (void)graph_neighbors(g, 0, &count); assert(count == 0);
        (void)graph_neighbors(g, 1, &count); assert(count == 0);
        assert(graph_add_edge(g, 0, 1) == GRAPH_OK);
        graph_destroy(g);
    }
    /* Sweep every allocation site on sample creation and BFS until success. */
    for (size_t i = 0; ; ++i) {
        GraphStatus status;
        assert(i < 100);
        arm(i); status = sample_graph(SAMPLE_STAR, &g); disarm();
        if (status == GRAPH_OK) break;
        assert(status == GRAPH_NO_MEMORY && !g);
    }
    for (int k = 0; k < 3; ++k) {
        for (size_t i = 0; ; ++i) {
            int dist[6];
            BfsStats stats;
            QueueStatus status;
            assert(i < 100);
            arm(i); status = bfs(g, 0, (QueueKind)k, dist, 6, &stats); disarm();
            if (status == QUEUE_OK) {
                assert(stats.visited == 6);
                for (int v = 0; v < 6; ++v) assert(dist[v] == (v ? 1 : 0));
                break;
            }
            assert(status == QUEUE_NO_MEMORY);
        }
    }
    graph_destroy(g);
    puts("allocation failure tests: PASS (creation, enqueue/growth, graph atomicity, sample/BFS failure sweep)");
    return 0;
}
