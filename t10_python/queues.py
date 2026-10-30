class ShiftingArrayQueue:
    def __init__(self):
        self.capacity = 4
        self.data = [None] * self.capacity
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            new_data = [None] * (2 * self.capacity)
            for index in range(self.size):
                new_data[index] = self.data[index]
            self.data = new_data
            self.capacity *= 2
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

    def is_empty(self):
        return self.size == 0


class CircularArrayQueue:
    def __init__(self):
        self.capacity = 4
        self.data = [None] * self.capacity
        self.front = 0
        self.size = 0

    def enqueue(self, value):
        if self.size == self.capacity:
            new_data = [None] * (2 * self.capacity)
            for index in range(self.size):
                old_index = (self.front + index) % self.capacity
                new_data[index] = self.data[old_index]
            self.data = new_data
            self.capacity *= 2
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
        return value

    def is_empty(self):
        return self.size == 0
