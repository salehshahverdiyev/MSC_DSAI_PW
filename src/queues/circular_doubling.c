#include "queue_internal.h"
#include <stdint.h>
#include <stdlib.h>
QueueStatus circular_enqueue(Queue *q, int value)
{
    size_t capacity = q->storage.array.capacity;
    if (q->size == capacity) {
        int *data;
        if (capacity > SIZE_MAX / sizeof(int) / 2) return QUEUE_NO_MEMORY;
        data = malloc(2 * capacity * sizeof(int));
        if (!data) return QUEUE_NO_MEMORY;
        /* Unroll in logical FIFO order, including a wrapped old head. */
        for (size_t i = 0; i < q->size; ++i)
            data[i] = q->storage.array.data[(q->storage.array.head + i) % capacity];
        free(q->storage.array.data);
        q->storage.array.data = data;
        q->storage.array.head = 0;
        q->storage.array.capacity = capacity *= 2;
    }
    q->storage.array.data[(q->storage.array.head + q->size) % capacity] = value;
    ++q->size;
    return QUEUE_OK;
}
void circular_dequeue(Queue *q)
{
    q->storage.array.head = (q->storage.array.head + 1) % q->storage.array.capacity;
    if (--q->size == 0) q->storage.array.head = 0;
}
