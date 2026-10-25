#ifndef T10_QUEUE_INTERNAL_H
#define T10_QUEUE_INTERNAL_H
#include "queue.h"
typedef struct Node { int value; struct Node *next; } Node;
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
