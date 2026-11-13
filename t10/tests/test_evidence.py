import random
import tempfile
import unittest
from collections import deque
from pathlib import Path
from t10.queues import (BASELINE_QUEUES, CircularArrayQueue,
                        IncrementalCircularArrayQueue, LinkedListQueue,
                        ShiftingArrayQueue)
from t10.bfs import bfs
from t10.demo import examples
from t10.graph import load_worm
from t10.graph import load_brainlinks
from t10.graph import path_graph, star_graph, tree_graph, grid_graph
from t10.real_demo import measure_bfs, synthetic_shapes, write_svg


def reference_distances(graph, start):
    # Repeated edge relaxation, independent of FIFO and BFS implementation.
    distances = [-1] * len(graph)
    distances[start] = 0
    for _ in range(len(graph) - 1):
        previous = distances[:]
        for vertex, neighbors in enumerate(graph):
            if previous[vertex] < 0:
                continue
            for neighbor in neighbors:
                candidate = previous[vertex] + 1
                if distances[neighbor] < 0 or candidate < distances[neighbor]:
                    distances[neighbor] = candidate
        if previous == distances:
            break
    return distances


class EvidenceTests(unittest.TestCase):
    def test_differential_fifo(self):
        for cls in BASELINE_QUEUES:
            rng = random.Random(20261103)
            queue, reference = cls(), deque()
            for _ in range(1500):
                if rng.random() < 0.58:
                    value = rng.choice([None, -2, 0, 7])
                    queue.enqueue(value)
                    reference.append(value)
                elif reference:
                    self.assertEqual(queue.dequeue(), reference.popleft())
                else:
                    with self.assertRaisesRegex(IndexError, "queue is empty"):
                        queue.dequeue()
                self.assertEqual(queue.size, len(reference))
                self.assertEqual(queue.is_empty(), not reference)
            while reference:
                self.assertEqual(queue.dequeue(), reference.popleft())
            if cls is LinkedListQueue:
                self.assertIsNone(queue.head)
                self.assertIsNone(queue.tail)

    def test_exact_work(self):
        for cls in BASELINE_QUEUES:
            q = cls()
            for value in range(9):
                q.enqueue(value)
            for value in range(9):
                self.assertEqual(q.dequeue(), value)
            self.assertEqual(q.max_size, 9)
            self.assertEqual(q.shifted_elements, 36 if cls is ShiftingArrayQueue else 0)
            expected_copies = (
                0 if cls is LinkedListQueue
                else 4 if cls is IncrementalCircularArrayQueue
                else 12
            )
            expected_resizes = 0 if cls is LinkedListQueue else (
                1 if cls is IncrementalCircularArrayQueue else 2
            )
            expected_history = (
                [] if cls is LinkedListQueue
                else [4, 8] if cls is IncrementalCircularArrayQueue
                else [4, 8, 16]
            )
            self.assertEqual(q.copied_elements, expected_copies)
            self.assertEqual(q.resize_events, expected_resizes)
            self.assertEqual(q.capacity_history, expected_history)
            before = (q.shifted_elements, q.copied_elements, q.resize_events)
            with self.assertRaises(IndexError):
                q.dequeue()
            self.assertEqual(before, (q.shifted_elements, q.copied_elements, q.resize_events))

    def test_bfs_reference(self):
        rng = random.Random(20261103)
        graphs = [g for _, g, _ in examples()]
        graphs += [[[j for j in range(15) if rng.random() < .15] for i in range(15)] for _ in range(10)]
        for graph in graphs:
            for source in range(len(graph)):
                expected = reference_distances(graph, source)
                for cls in BASELINE_QUEUES:
                    distances, stats = bfs(graph, source, cls, True)
                    self.assertEqual(distances, expected)
                    reachable = sum(d >= 0 for d in expected)
                    self.assertEqual(stats["enqueues"], reachable)
                    self.assertEqual(stats["dequeues"], reachable)
                    self.assertEqual(len(set(stats["visited"])), reachable)

    def test_graph_generators(self):
        self.assertEqual(path_graph(4), [[1], [0, 2], [1, 3], [2]])
        self.assertEqual(star_graph(4), [[1, 2, 3], [0], [0], [0]])
        self.assertEqual(tree_graph(5), [[1, 2], [0, 3, 4], [0], [1], [1]])
        self.assertEqual(grid_graph(2, 2), [[1, 2], [0, 3], [0, 3], [1, 2]])
        self.assertEqual(grid_graph(1, 1), [[]])
        for generator in (path_graph, star_graph, tree_graph):
            self.assertEqual(generator(0), [])
            self.assertEqual(generator(1), [[]])
            for invalid in (-1, 1.5, True):
                with self.assertRaises(ValueError):
                    generator(invalid)
        for dimensions in ((0, 2), (2, -1), (1.5, 2)):
            with self.assertRaises(ValueError):
                grid_graph(*dimensions)

    def test_loader(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "links.txt"
            path.write_text("// j points to i\n2 1 3\n2 1 2\n3 2 1\n3 3 1\n1 3 0\n")
            graph, stats = load_worm(path, 4)
            self.assertEqual(graph, [[1], [2], [2], []])
            self.assertEqual(stats["duplicates"], 1)
            self.assertEqual(stats["nonpositive"], 1)
            for empty in ("", "// comments only\n"):
                path.write_text(empty)
                with self.assertRaisesRegex(ValueError, "no connection rows"):
                    load_worm(path, 4)
            for bad in ("<html>error</html>", "1 2", "0 1 2", "1 2 nan", "x 2 1"):
                path.write_text(bad)
                with self.assertRaisesRegex(ValueError, "line 1"):
                    load_worm(path, 4)

    def test_brainlinks_loader_compacts_sample(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "brainlinks.dat"
            path.write_text("10 20\n10 20\n20 30\n")
            graph, stats = load_brainlinks(path, 2)
            self.assertEqual(graph, [[1], [2], []])
            self.assertEqual(stats["labels"], [10, 20, 30])
            self.assertEqual(stats["duplicates"], 1)

    def test_real_demo_metrics_and_svg(self):
        graph = [[1], [2], []]
        distances, stats = measure_bfs(graph, CircularArrayQueue)
        self.assertEqual(distances, [0, 1, 2])
        self.assertGreaterEqual(stats["time_seconds"], 0)
        self.assertGreater(stats["peak_bytes"], 0)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "graph.svg"
            write_svg(graph, distances, [10, 20, 30], output)
            content = output.read_text(encoding="utf-8")
            self.assertIn("<svg", content)
            self.assertIn("BFS graph", content)

    def test_synthetic_shapes_are_independent_of_sample(self):
        shapes = synthetic_shapes()
        self.assertEqual([name for name, _ in shapes],
                         ["Synthetic Path", "Synthetic Star",
                          "Synthetic Binary tree", "Synthetic Grid 5x8"])
        for _, graph in shapes:
            self.assertEqual(len(graph), 40)

    @unittest.skipUnless(Path("data/raw/ssumlinks.txt").exists(), "optional raw dataset absent")
    def test_real_graph(self):
        graph, stats = load_worm("data/raw/ssumlinks.txt")
        for source in (0, max(range(len(graph)), key=lambda v: len(graph[v]))):
            expected = reference_distances(graph, source)
            for cls in BASELINE_QUEUES:
                self.assertEqual(bfs(graph, source, cls), expected)
