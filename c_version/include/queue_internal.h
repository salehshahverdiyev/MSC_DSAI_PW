#ifndef T10_QUEUE_INTERNAL_H
#define T10_QUEUE_INTERNAL_H
#include "queue.h"
/* A list node owns its value; next links to the following node (NULL at tail). */
typedef struct Node { int value; struct Node *next; } Node;
/* The tag 'kind' selects which union member is valid; union storage is shared.
 * Arrays: size <= capacity, head is the front slot (always 0 for shifting).
 * Ring insertion slot is (head + size) % capacity; no separate tail is needed.
 * List: size == 0 iff both head and tail are NULL; tail->next is always NULL.
 * size_t is the unsigned type used for element counts and allocation sizes.
 */
struct Queue {
    QueueKind kind;
    size_t size;
    union {
        struct { int *data; size_t capacity, head; } array;
        struct { Node *head, *tail; } list;
    } storage;
};
QueueStatus shifting_enqueue(Queue *q, int value);
void shifting_dequeue(Queue *q);
QueueStatus linked_enqueue(Queue *q, int value);
void linked_dequeue(Queue *q);
QueueStatus circular_enqueue(Queue *q, int value);
void circular_dequeue(Queue *q);
#endif
