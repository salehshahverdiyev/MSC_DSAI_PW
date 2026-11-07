class QueueInterface:
    """Shared FIFO contract and instrumentation for every queue."""

    def __init__(self):
        self.size = 0
        self.capacity = None
        self.shifted_elements = 0
        self.copied_elements = 0
        self.resize_events = 0
        self.max_size = 0
        self.capacity_history = []

    def enqueue(self, value):
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError

    def is_empty(self):
        return self.size == 0

    def _record_enqueue(self):
        self.size += 1
        self.max_size = max(self.max_size, self.size)


class ShiftingArrayQueue(QueueInterface):
    def __init__(self):
        super().__init__()
        self.capacity = 4
        self.data = [None] * self.capacity
        self.capacity_history = [self.capacity]

    def enqueue(self, value):
        if self.size == self.capacity:
            new_data = [None] * (2 * self.capacity)
            for index in range(self.size):
                new_data[index] = self.data[index]
                self.copied_elements += 1
            self.data = new_data
            self.capacity *= 2
            self.resize_events += 1
            self.capacity_history.append(self.capacity)
        self.data[self.size] = value
        self._record_enqueue()

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.data[0]
        for index in range(1, self.size):
            self.data[index - 1] = self.data[index]
            self.shifted_elements += 1
        self.size -= 1
        self.data[self.size] = None
        return value

class CircularArrayQueue(QueueInterface):
    def __init__(self):
        super().__init__()
        self.capacity = 4
        self.data = [None] * self.capacity
        self.front = 0
        self.capacity_history = [self.capacity]

    def enqueue(self, value):
        if self.size == self.capacity:
            new_data = [None] * (2 * self.capacity)
            for index in range(self.size):
                old_index = (self.front + index) % self.capacity
                new_data[index] = self.data[old_index]
                self.copied_elements += 1
            self.data = new_data
            self.capacity *= 2
            self.resize_events += 1
            self.capacity_history.append(self.capacity)
            self.front = 0
        back = (self.front + self.size) % self.capacity
        self.data[back] = value
        self._record_enqueue()

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedListQueue(QueueInterface):
    name = "linked-list"

    def __init__(self):
        super().__init__()
        self.head = None
        self.tail = None

    def enqueue(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self._record_enqueue()

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        if self.size == 0:
            self.tail = None
        return value

class IncrementalCircularArrayQueue(QueueInterface):
    """Circular queue that migrates one element per operation while growing."""

    def __init__(self):
        super().__init__()
        self.capacity = 4
        self.data = [None] * self.capacity
        self.front = 0
        self.capacity_history = [self.capacity]
        self._old_data = None
        self._old_front = 0
        self._old_unmigrated = 0
        self._new_data = None
        self._new_front = 0
        self._migrated = 0
        self._pending_data = None
        self._pending_front = 0
        self._pending_size = 0

    def _begin_resize(self):
        self._old_data = self.data
        self._old_front = self.front
        self._old_unmigrated = self.size
        self._new_data = [None] * (2 * self.capacity)
        self._new_front = 0
        self._migrated = 0
        self._pending_data = [None] * (2 * self.capacity)
        self._pending_front = 0
        self._pending_size = 0
        self.capacity *= 2
        self.resize_events += 1
        self.capacity_history.append(self.capacity)

    def _append_migrated(self, value):
        index = (self._new_front + self._migrated) % self.capacity
        self._new_data[index] = value

    def _ensure_pending_capacity(self):
        if self._pending_size == len(self._pending_data):
            expanded = [None] * (2 * len(self._pending_data))
            for index in range(self._pending_size):
                old_index = (self._pending_front + index) % len(self._pending_data)
                expanded[index] = self._pending_data[old_index]
            self._pending_data = expanded
            self._pending_front = 0
            self.capacity = max(self.capacity, len(expanded))
            self.resize_events += 1
            self.capacity_history.append(self.capacity)
            self.copied_elements += self._pending_size

    def _append_pending(self, value):
        self._ensure_pending_capacity()
        index = (self._pending_front + self._pending_size) % self.capacity
        self._pending_data[index] = value
        self._pending_size += 1

    def _migrate_one(self):
        if self._old_data is None or self._old_unmigrated == 0:
            return
        value = self._old_data[self._old_front]
        self._old_data[self._old_front] = None
        self._old_front = (self._old_front + 1) % len(self._old_data)
        self._old_unmigrated -= 1
        self._append_migrated(value)
        self._migrated += 1
        self.copied_elements += 1

    def _finish_resize(self):
        if self._old_data is None or self._old_unmigrated or self._migrated:
            return
        if self._pending_data is not None:
            self.data = self._pending_data
            self.front = self._pending_front
        else:
            self.data = self._new_data
            self.front = self._new_front
        self._old_data = None
        self._new_data = None
        self._migrated = 0
        self._pending_data = None
        self._pending_size = 0

    def enqueue(self, value):
        if self._old_data is None and self.size == self.capacity:
            self._begin_resize()
        elif self._old_data is not None and self.size >= self.capacity:
            self._ensure_pending_capacity()
        if self._old_data is not None:
            self._migrate_one()
            self._append_pending(value)
        elif self._migrated:
            self._append_pending(value)
        else:
            index = (self.front + self.size) % self.capacity
            self.data[index] = value
        self._record_enqueue()
        self._finish_resize()

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        if self._old_data is not None:
            self._migrate_one()
            if self._migrated:
                value = self._new_data[self._new_front]
                self._new_data[self._new_front] = None
                self._new_front = (self._new_front + 1) % self.capacity
                self._migrated -= 1
            elif self._old_unmigrated:
                value = self._old_data[self._old_front]
                self._old_data[self._old_front] = None
                self._old_front = (self._old_front + 1) % len(self._old_data)
                self._old_unmigrated -= 1
            else:
                value = self._pending_data[self._pending_front]
                self._pending_data[self._pending_front] = None
                self._pending_front = (
                    self._pending_front + 1
                ) % self.capacity
                self._pending_size -= 1
        else:
            value = self.data[self.front]
            self.data[self.front] = None
            self.front = (self.front + 1) % self.capacity
        self.size -= 1
        self._finish_resize()
        return value


BASELINE_QUEUES = (
    ShiftingArrayQueue,
    LinkedListQueue,
    CircularArrayQueue,
    IncrementalCircularArrayQueue,
)
