class ShiftingArrayQueue:
    name = "shifting-array"

    def __init__(self, initial_capacity=4):
        if type(initial_capacity) is not int or initial_capacity < 1:
            raise ValueError("initial capacity must be a positive integer")
        self.capacity = initial_capacity
        self.data = [None] * self.capacity
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            new_capacity = self.capacity * 2
            new_data = [None] * new_capacity
            for index in range(self.size):
                new_data[index] = self.data[index]
            self.data = new_data
            self.capacity = new_capacity
        self.data[self.size] = value
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.data[0]
        for index in range(1, self.size):
            self.data[index - 1] = self.data[index]
        self.size -= 1
        self.data[self.size] = None
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self.data[0]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def to_list(self):
        values = []
        for index in range(self.size):
            values.append(self.data[index])
        return values

    def storage_info(self):
        return {"size": self.size, "capacity": self.capacity,
                "unused_slots": self.capacity - self.size, "nodes": 0}


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

    def enqueue(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.head.value
        self.head = self.head.next
        self.size -= 1
        if self.size == 0:
            self.tail = None
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self.head.value

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def to_list(self):
        values = []
        node = self.head
        while node is not None:
            values.append(node.value)
            node = node.next
        return values

    def storage_info(self):
        return {"size": self.size, "capacity": None,
                "unused_slots": None, "nodes": self.size}


class CircularArrayQueue:
    name = "circular-doubling"

    def __init__(self, initial_capacity=4):
        if type(initial_capacity) is not int or initial_capacity < 1:
            raise ValueError("initial capacity must be a positive integer")
        self.capacity = initial_capacity
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            new_capacity = self.capacity * 2
            new_data = [None] * new_capacity
            # Copy logical FIFO order, even when the old buffer is wrapped.
            for index in range(self.size):
                old_index = (self.front + index) % self.capacity
                new_data[index] = self.data[old_index]
            self.data = new_data
            self.capacity = new_capacity
            self.front = 0
        back = (self.front + self.size) % self.capacity
        self.data[back] = value
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        value = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        if self.size == 0:
            self.front = 0
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self.data[self.front]

    def is_empty(self):
        return self.size == 0

    def __len__(self):
        return self.size

    def to_list(self):
        values = []
        for index in range(self.size):
            slot = (self.front + index) % self.capacity
            values.append(self.data[slot])
        return values

    def storage_info(self):
        return {"size": self.size, "capacity": self.capacity,
                "unused_slots": self.capacity - self.size, "nodes": 0}


BASELINE_QUEUES = (ShiftingArrayQueue, LinkedListQueue, CircularArrayQueue)

