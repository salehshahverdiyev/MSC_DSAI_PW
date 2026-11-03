class ShiftingArrayQueue:
    def __init__(self):
        self.capacity = 4
        self.data = [None] * self.capacity
        self.size = 0
        self.shifted_elements = 0
        self.copied_elements = 0
        self.resize_events = 0
        self.max_size = 0
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
        self.size += 1
        self.max_size = max(self.max_size, self.size)

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

    def is_empty(self):
        return self.size == 0


class CircularArrayQueue:
    def __init__(self):
        self.capacity = 4
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0
        self.shifted_elements = 0
        self.copied_elements = 0
        self.resize_events = 0
        self.max_size = 0
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
        self.size += 1
        self.max_size = max(self.max_size, self.size)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return value

    def is_empty(self):
        return self.size == 0


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedListQueue:
    name = "linked-list"

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.capacity = None
        self.shifted_elements = 0
        self.copied_elements = 0
        self.resize_events = 0
        self.max_size = 0
        self.capacity_history = []

    def enqueue(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1
        self.max_size = max(self.max_size, self.size)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        if self.size == 0:
            self.tail = None
        return value

    def is_empty(self):
        return self.size == 0

BASELINE_QUEUES = (ShiftingArrayQueue, LinkedListQueue, CircularArrayQueue)
