#ifndef T10_QUEUE_H
#define T10_QUEUE_H
#include <stdbool.h>
#include <stddef.h>

typedef enum {
    QUEUE_OK, QUEUE_EMPTY, QUEUE_NO_MEMORY, QUEUE_INVALID_ARGUMENT,
    QUEUE_UNSUPPORTED
} QueueStatus;
typedef enum {
    QUEUE_SHIFTING_ARRAY, QUEUE_LINKED_LIST, QUEUE_CIRCULAR_DOUBLING,
    QUEUE_CIRCULAR_INCREMENTAL
} QueueKind;
typedef struct Queue Queue;

/* Owns copied int values. Caller owns *out on success; destroy exactly once.
 * Create clears *out on failure. Failed enqueue leaves FIFO unchanged.
 * Failed peek/dequeue/capacity leaves output unchanged. NULL arguments are
 * INVALID_ARGUMENT; destroy(NULL) is safe; size(NULL)=0, is_empty(NULL)=true.
 * Capacity is reserved slots for arrays; linked list returns UNSUPPORTED (N/A).
 * Array capacity starts at 4, doubles on full, never shrinks. Overflow -> NO_MEMORY.
 */
QueueStatus queue_create(QueueKind kind, Queue **out);
QueueStatus queue_enqueue(Queue *q, int value);
QueueStatus queue_dequeue(Queue *q, int *out);
QueueStatus queue_peek(const Queue *q, int *out);
QueueStatus queue_capacity(const Queue *q, size_t *out);
size_t queue_size(const Queue *q);
bool queue_is_empty(const Queue *q);
void queue_destroy(Queue *q);
const char *queue_kind_name(QueueKind kind);
#endif
