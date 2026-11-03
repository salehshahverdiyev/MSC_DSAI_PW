import unittest

from t10_python.queues import ShiftingArrayQueue, CircularArrayQueue, BASELINE_QUEUES
from t10_python.bfs import bfs


class BasicTests(unittest.TestCase):
    def test_empty(self):
        for queue_class in BASELINE_QUEUES:
            queue = queue_class()
            self.assertTrue(queue.is_empty())
            with self.assertRaises(IndexError):
                queue.dequeue()

    def test_fifo_and_refill(self):
        for queue_class in BASELINE_QUEUES:
            queue = queue_class()
            for cycle in range(3):
                queue.enqueue(10)
                queue.enqueue(20)
                self.assertEqual(queue.dequeue(), 10)
                queue.enqueue(30)
                self.assertEqual(queue.dequeue(), 20)
                self.assertEqual(queue.dequeue(), 30)
                self.assertTrue(queue.is_empty())

    def test_growth(self):
        for queue_class in BASELINE_QUEUES:
            queue = queue_class()
            for value in range(100):
                queue.enqueue(value)
            if queue.capacity is not None:
                self.assertEqual(queue.capacity, 128)
            for value in range(100):
                self.assertEqual(queue.dequeue(), value)
            self.assertTrue(queue.is_empty())

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
        queue.enqueue(6)
        self.assertEqual(queue.capacity, 8)
        for value in range(2, 7):
            self.assertEqual(queue.dequeue(), value)

    def test_path_and_star(self):
        path = [[1], [0, 2], [1, 3], [2, 4], [3, 5], [4]]
        star = [[1, 2, 3, 4, 5], [0], [0], [0], [0], [0]]
        for queue_class in BASELINE_QUEUES:
            self.assertEqual(bfs(path, 0, queue_class), [0, 1, 2, 3, 4, 5])
            self.assertEqual(bfs(star, 0, queue_class), [0, 1, 1, 1, 1, 1])

    def test_unreachable_and_invalid_start(self):
        graph = [[1], [0], []]
        for queue_class in BASELINE_QUEUES:
            self.assertEqual(bfs(graph, 0, queue_class), [0, 1, -1])
            self.assertEqual(bfs(graph, 2, queue_class), [-1, -1, 0])
            with self.assertRaises(ValueError):
                bfs(graph, -1, queue_class)
            with self.assertRaises(ValueError):
                bfs(graph, 3, queue_class)


if __name__ == "__main__":
    unittest.main()
