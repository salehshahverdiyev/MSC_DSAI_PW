#include "queue_internal.h"
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
QueueStatus shifting_enqueue(Queue *q, int value)
{
    if (q->size == q->storage.array.capacity) {
        size_t capacity = q->storage.array.capacity;
        int *data;
        if (capacity > SIZE_MAX / sizeof(int) / 2) return QUEUE_NO_MEMORY;
        data = realloc(q->storage.array.data, 2 * capacity * sizeof(int));
        if (!data) return QUEUE_NO_MEMORY;
        q->storage.array.data = data;
        q->storage.array.capacity = 2 * capacity;
    }
    q->storage.array.data[q->size++] = value;
    return QUEUE_OK;
}
void shifting_dequeue(Queue *q)
{
    --q->size;
    memmove(q->storage.array.data, q->storage.array.data + 1,
            q->size * sizeof(int));
}
