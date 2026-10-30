import random
import unittest
from collections import deque  # Independent test oracle, never production storage.

from archive.full_python_m1.queues import (
    BASELINE_QUEUES, ShiftingArrayQueue, LinkedListQueue, CircularArrayQueue,
)


class QueueTests(unittest.TestCase):
    def test_empty_operations(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                self.assertTrue(queue.is_empty())
                self.assertEqual(len(queue), 0)
                with self.assertRaisesRegex(IndexError, "queue is empty"):
                    queue.dequeue()
                with self.assertRaisesRegex(IndexError, "queue is empty"):
                    queue.peek()
                self.assertEqual(queue.to_list(), [])

    def test_fifo_and_peek(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                for value in [10, 20, 30]:
                    queue.enqueue(value)
                self.assertEqual(queue.peek(), 10)
                self.assertEqual(len(queue), 3)
                for value in [10, 20, 30]:
                    self.assertEqual(queue.dequeue(), value)
                self.assertTrue(queue.is_empty())

    def test_interleaving_and_refill(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                for cycle in range(20):
                    queue.enqueue(1)
                    queue.enqueue(2)
                    self.assertEqual(queue.dequeue(), 1)
                    queue.enqueue(3)
                    self.assertEqual(queue.dequeue(), 2)
                    self.assertEqual(queue.dequeue(), 3)
                    self.assertTrue(queue.is_empty())

    def test_none_and_reference_values(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                value = ["one shared object"]
                queue.enqueue(None)
                queue.enqueue(value)
                self.assertIsNone(queue.dequeue())
                self.assertIs(queue.peek(), value)
                self.assertIs(queue.dequeue(), value)

    def test_multiple_doublings(self):
        for queue_class in [ShiftingArrayQueue, CircularArrayQueue]:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                for value in range(1000):
                    queue.enqueue(value)
                self.assertEqual(queue.capacity, 1024)
                self.assertEqual(len(queue.data), queue.capacity)
                for value in range(1000):
                    self.assertEqual(queue.dequeue(), value)
                self.assertEqual(queue.capacity, 1024)  # No shrink.
                self.assertEqual(queue.data, [None] * 1024)

    def test_wrapped_resize(self):
        queue = CircularArrayQueue()
        for value in range(4):
            queue.enqueue(value)
        self.assertEqual(queue.dequeue(), 0)
        self.assertEqual(queue.dequeue(), 1)
        queue.enqueue(4)
        queue.enqueue(5)
        self.assertEqual(queue.front, 2)
        self.assertEqual(queue.data, [4, 5, 2, 3])
        queue.enqueue(6)  # Full AND wrapped: the important resize regression.
        self.assertEqual(queue.capacity, 8)
        self.assertEqual(queue.front, 0)
        self.assertEqual(queue.to_list(), [2, 3, 4, 5, 6])
        for value in [2, 3, 4, 5, 6]:
            self.assertEqual(queue.dequeue(), value)

    def test_small_capacities_and_repeated_wrap(self):
        for capacity in [1, 2, 3, 4, 7]:
            with self.subTest(capacity=capacity):
                queue = CircularArrayQueue(capacity)
                reference = deque()
                for value in range(capacity):
                    queue.enqueue(value)
                    reference.append(value)
                for value in range(100):
                    self.assertEqual(queue.dequeue(), reference.popleft())
                    queue.enqueue(value)
                    reference.append(value)
                    self.assertEqual(queue.to_list(), list(reference))
                queue.enqueue(999)  # Grow at each tested physical head offset.
                reference.append(999)
                self.assertEqual(queue.to_list(), list(reference))

    def test_storage_information(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                queue = queue_class()
                queue.enqueue(5)
                queue.enqueue(6)
                info = queue.storage_info()
                self.assertEqual(info["size"], 2)
                if queue_class is LinkedListQueue:
                    self.assertIsNone(info["capacity"])
                    self.assertIsNone(info["unused_slots"])
                    self.assertEqual(info["nodes"], 2)
                    self.assertIsNone(queue.tail.next)
                else:
                    self.assertEqual(info["capacity"], 4)
                    self.assertEqual(info["unused_slots"], 2)
                    self.assertEqual(info["nodes"], 0)
                queue.dequeue()
                queue.dequeue()
                if queue_class is LinkedListQueue:
                    self.assertIsNone(queue.head)
                    self.assertIsNone(queue.tail)
                    self.assertEqual(queue.storage_info()["nodes"], 0)

    def test_invalid_array_capacity(self):
        for queue_class in [ShiftingArrayQueue, CircularArrayQueue]:
            for capacity in [0, -1, 1.5, True]:
                with self.subTest(queue=queue_class.name, capacity=capacity):
                    with self.assertRaises(ValueError):
                        queue_class(capacity)

    def test_seeded_random_operations(self):
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                random_source = random.Random(20261030)
                queue = queue_class()
                reference = deque()
                for step in range(50000):
                    if not reference or random_source.random() < 0.5:
                        value = random_source.randrange(-10000, 10001)
                        queue.enqueue(value)
                        reference.append(value)
                    else:
                        self.assertEqual(queue.dequeue(), reference.popleft())
                    self.assertEqual(len(queue), len(reference))
                    self.assertEqual(queue.is_empty(), len(reference) == 0)
                    if reference:
                        self.assertEqual(queue.peek(), reference[0])
                    if step % 250 == 0:
                        self.assertEqual(queue.to_list(), list(reference))
                while reference:
                    self.assertEqual(queue.dequeue(), reference.popleft())
                self.assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
