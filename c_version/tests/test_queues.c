#include "queue.h"
#include "queue_internal.h"
#include <assert.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>

static void take(Queue *q, int expected)
{
    int value = 0;
    assert(queue_peek(q, &value) == QUEUE_OK && value == expected);
    assert(queue_dequeue(q, &value) == QUEUE_OK && value == expected);
}
static void check_kind(QueueKind kind)
{
    Queue *q = NULL;
    int value = 77;
    size_t capacity = 99;
    assert(queue_create(kind, &q) == QUEUE_OK);
    assert(queue_is_empty(q) && queue_size(q) == 0);
    assert(queue_peek(q, &value) == QUEUE_EMPTY && value == 77);
    assert(queue_dequeue(q, &value) == QUEUE_EMPTY && value == 77);
    assert(queue_peek(q, NULL) == QUEUE_INVALID_ARGUMENT);
    assert(queue_dequeue(q, NULL) == QUEUE_INVALID_ARGUMENT);
    assert(queue_capacity(q, NULL) == QUEUE_INVALID_ARGUMENT);
    if (kind == QUEUE_LINKED_LIST)
        assert(queue_capacity(q, &capacity) == QUEUE_UNSUPPORTED && capacity == 99);
    else assert(queue_capacity(q, &capacity) == QUEUE_OK && capacity == 4);
    assert(queue_enqueue(q, INT_MIN) == QUEUE_OK); take(q, INT_MIN);
    assert(queue_enqueue(q, INT_MAX) == QUEUE_OK); take(q, INT_MAX);
    /* Fill capacity 4, advance head, wrap, then force growth with head != 0. */
    for (int i = 0; i < 4; ++i) assert(queue_enqueue(q, i) == QUEUE_OK);
    take(q, 0); take(q, 1);
    assert(queue_enqueue(q, 4) == QUEUE_OK);
    assert(queue_enqueue(q, 5) == QUEUE_OK);
    if (kind == QUEUE_CIRCULAR_DOUBLING) assert(q->storage.array.head == 2);
    assert(queue_enqueue(q, 6) == QUEUE_OK);
    for (int i = 2; i <= 6; ++i) take(q, i);
    for (int round = 0; round < 20; ++round) {
        for (int i = 0; i < 1000; ++i) assert(queue_enqueue(q, i) == QUEUE_OK);
        for (int i = 0; i < 1000; ++i) take(q, i);
        assert(queue_is_empty(q));
        if (kind == QUEUE_LINKED_LIST)
            assert(!q->storage.list.head && !q->storage.list.tail);
    }
    /* Independent fixed storage oracle; deterministic mixed-operation trace. */
    {
        int oracle[50000];
        size_t front = 0, back = 0;
        uint32_t seed = 20261030;
        for (int step = 0; step < 50000; ++step) {
            seed = seed * UINT32_C(1664525) + UINT32_C(1013904223);
            if (front == back || (seed & 256)) {
                int item = (int)(seed % 100000);
                oracle[back++] = item;
                assert(queue_enqueue(q, item) == QUEUE_OK);
            } else take(q, oracle[front++]);
            assert(queue_size(q) == back - front);
            assert(queue_is_empty(q) == (back == front));
            if (front < back) {
                assert(queue_peek(q, &value) == QUEUE_OK);
                assert(value == oracle[front]);
            }
        }
        while (front < back) take(q, oracle[front++]);
    }
    assert(queue_enqueue(q, 42) == QUEUE_OK); /* destroy a nonempty queue */
    queue_destroy(q);
}
int main(void)
{
    Queue *q = NULL;
    int value = 1;
    size_t capacity = 3;
    assert(queue_create(QUEUE_CIRCULAR_INCREMENTAL, &q) == QUEUE_UNSUPPORTED && !q);
    assert(queue_create((QueueKind)99, &q) == QUEUE_INVALID_ARGUMENT && !q);
    assert(queue_create(QUEUE_LINKED_LIST, NULL) == QUEUE_INVALID_ARGUMENT);
    assert(queue_enqueue(NULL, 1) == QUEUE_INVALID_ARGUMENT);
    assert(queue_dequeue(NULL, &value) == QUEUE_INVALID_ARGUMENT && value == 1);
    assert(queue_peek(NULL, &value) == QUEUE_INVALID_ARGUMENT);
    assert(queue_capacity(NULL, &capacity) == QUEUE_INVALID_ARGUMENT && capacity == 3);
    assert(queue_size(NULL) == 0 && queue_is_empty(NULL));
    queue_destroy(NULL);
    for (int k = 0; k < 3; ++k) check_kind((QueueKind)k);
    puts("queue tests: PASS (3 baselines; 50000 seeded steps each; wrapped resize/refill)");
    return 0;
}
