#include "queue_internal.h"
#include <stdlib.h>
QueueStatus linked_enqueue(Queue *q, int value)
{
    Node *node = malloc(sizeof(*node));
    if (!node) return QUEUE_NO_MEMORY;
    node->value = value;
    node->next = NULL;
    if (q->storage.list.tail) q->storage.list.tail->next = node;
    else q->storage.list.head = node;
    q->storage.list.tail = node;
    ++q->size;
    return QUEUE_OK;
}
void linked_dequeue(Queue *q)
{
    Node *node = q->storage.list.head;
    q->storage.list.head = node->next;
    if (--q->size == 0) q->storage.list.tail = NULL;
    free(node);
}
