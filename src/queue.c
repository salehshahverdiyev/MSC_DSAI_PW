#include "queue_internal.h"
#include <stdint.h>
#include <stdlib.h>

QueueStatus queue_create(QueueKind kind, Queue **out)
{
    Queue *q;
    if (!out) return QUEUE_INVALID_ARGUMENT;
    *out = NULL;
    if (kind == QUEUE_CIRCULAR_INCREMENTAL) return QUEUE_UNSUPPORTED;
    if (kind < QUEUE_SHIFTING_ARRAY || kind > QUEUE_CIRCULAR_DOUBLING)
        return QUEUE_INVALID_ARGUMENT;
    /* calloc initializes an empty queue; backing storage is owned separately. */
    q = calloc(1, sizeof(*q));
    if (!q) return QUEUE_NO_MEMORY;
    q->kind = kind;
    if (kind != QUEUE_LINKED_LIST) {
        q->storage.array.data = malloc(4 * sizeof(int));
        if (!q->storage.array.data) { free(q); return QUEUE_NO_MEMORY; }
        q->storage.array.capacity = 4;
    }
    *out = q;
    return QUEUE_OK;
}
QueueStatus queue_enqueue(Queue *q, int value)
{
    if (!q) return QUEUE_INVALID_ARGUMENT;
    if (q->size == SIZE_MAX) return QUEUE_NO_MEMORY;
    /* One public interface, three independent storage implementations. */
    switch (q->kind) {
    case QUEUE_SHIFTING_ARRAY: return shifting_enqueue(q, value);
    case QUEUE_LINKED_LIST: return linked_enqueue(q, value);
    case QUEUE_CIRCULAR_DOUBLING: return circular_enqueue(q, value);
    default: return QUEUE_UNSUPPORTED;
    }
}
QueueStatus queue_peek(const Queue *q, int *out)
{
    if (!q || !out) return QUEUE_INVALID_ARGUMENT;
    if (!q->size) return QUEUE_EMPTY;
    if (q->kind == QUEUE_LINKED_LIST) {
        *out = q->storage.list.head->value;
    } else {
        *out = q->storage.array.data[q->storage.array.head];
    }
    return QUEUE_OK;
}
QueueStatus queue_dequeue(Queue *q, int *out)
{
    /* Read/validate first; only a successful read may remove the front item. */
    QueueStatus status = queue_peek(q, out);
    if (status != QUEUE_OK) return status;
    switch (q->kind) {
    case QUEUE_SHIFTING_ARRAY: shifting_dequeue(q); break;
    case QUEUE_LINKED_LIST: linked_dequeue(q); break;
    case QUEUE_CIRCULAR_DOUBLING: circular_dequeue(q); break;
    default: return QUEUE_UNSUPPORTED;
    }
    return QUEUE_OK;
}
size_t queue_size(const Queue *q) { return q ? q->size : 0; }
bool queue_is_empty(const Queue *q) { return queue_size(q) == 0; }
QueueStatus queue_capacity(const Queue *q, size_t *out)
{
    if (!q || !out) return QUEUE_INVALID_ARGUMENT;
    if (q->kind == QUEUE_LINKED_LIST) return QUEUE_UNSUPPORTED;
    *out = q->storage.array.capacity;
    return QUEUE_OK;
}
void queue_destroy(Queue *q)
{
    if (!q) return;
    /* Free owned elements/backing storage before freeing the queue wrapper. */
    if (q->kind == QUEUE_LINKED_LIST) {
        while (q->size) linked_dequeue(q);
    } else free(q->storage.array.data);
    free(q);
}
const char *queue_kind_name(QueueKind kind)
{
    switch (kind) {
    case QUEUE_SHIFTING_ARRAY: return "shifting-array";
    case QUEUE_LINKED_LIST: return "linked-list";
    case QUEUE_CIRCULAR_DOUBLING: return "circular-doubling";
    case QUEUE_CIRCULAR_INCREMENTAL: return "incremental (NOT IMPLEMENTED)";
    default: return "invalid";
    }
}
