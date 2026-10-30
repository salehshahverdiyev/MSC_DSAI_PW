import contextlib
import io
import random
import unittest

from archive.full_python_m1.bfs import bfs
from archive.full_python_m1.graph import Graph
from archive.full_python_m1.generators import path, star, tree, grid
from archive.full_python_m1.queues import BASELINE_QUEUES
from archive.full_python_m1.sample_graphs import examples, diamond


def reference_distances(graph, source):
    """Repeated edge relaxation: no queue and no production BFS scheduling."""
    distances = [-1] * len(graph)
    distances[source] = 0
    for pass_number in range(len(graph)):
        for vertex in range(len(graph)):
            if distances[vertex] == -1:
                continue
            for neighbor in graph.adjacency[vertex]:
                candidate = distances[vertex] + 1
                if distances[neighbor] == -1 or candidate < distances[neighbor]:
                    distances[neighbor] = candidate
    return distances


class BfsTests(unittest.TestCase):
    def check_graph(self, graph, source, expected, expected_peak=None):
        self.assertEqual(reference_distances(graph, source), expected)
        reachable = 0
        for distance in expected:
            if distance >= 0:
                reachable += 1
        first_counters = None
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name, source=source):
                distances, counters = bfs(graph, source, queue_class)
                self.assertEqual(distances, expected)
                self.assertEqual(counters["visited"], reachable)
                self.assertEqual(counters["enqueue_count"], reachable)
                self.assertEqual(counters["dequeue_count"], reachable)
                self.assertGreaterEqual(counters["frontier_peak"], 1)
                self.assertLessEqual(counters["frontier_peak"], reachable)
                if expected_peak is not None:
                    self.assertEqual(counters["frontier_peak"], expected_peak)
                if first_counters is None:
                    first_counters = counters
                self.assertEqual(counters, first_counters)

    def test_hand_worked_samples(self):
        for name, graph, distances, peak in examples():
            with self.subTest(graph=name):
                self.check_graph(graph, 0, distances, peak)

    def test_reverse_and_isolated_sources(self):
        self.check_graph(path(6), 5, [5, 4, 3, 2, 1, 0], 1)
        self.check_graph(star(6), 5, [1, 2, 2, 2, 2, 0], 4)
        self.check_graph(diamond(), 5, [-1, -1, -1, -1, -1, 0], 1)

    def test_singleton_self_loops_and_duplicates(self):
        graph = Graph(1)
        graph.add_edge(0, 0)
        graph.add_edge(0, 0)
        self.assertEqual(graph.neighbors(0), [0, 0])
        self.check_graph(graph, 0, [0], 1)
        graph = Graph(4, directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(0, 1)
        graph.add_edge(1, 0)
        self.check_graph(graph, 0, [0, 1, -1, -1], 1)

    def test_directed_and_undirected_storage(self):
        graph = Graph(3)
        graph.add_edge(0, 2)
        graph.add_edge(0, 1)
        self.assertEqual(graph.adjacency, [[2, 1], [0], [0]])
        graph = Graph(3, directed=True)
        graph.add_edge(0, 2)
        self.assertEqual(graph.adjacency, [[2], [], []])

    def test_tree_and_grid_generators(self):
        self.check_graph(tree(7), 0, [0, 1, 1, 2, 2, 2, 2], 4)
        self.check_graph(tree(6, branching=1), 0, [0, 1, 2, 3, 4, 5], 1)
        self.check_graph(grid(2, 3), 0, [0, 1, 2, 1, 2, 3])
        for generator in [path, star, tree]:
            self.check_graph(generator(1), 0, [0], 1)
        self.check_graph(grid(1, 1), 0, [0], 1)
        graph = grid(3, 4)
        adjacency_entries = 0
        for neighbors in graph.adjacency:
            adjacency_entries += len(neighbors)
        self.assertEqual(adjacency_entries, 2 * (3 * 3 + 2 * 4))

    def test_invalid_inputs(self):
        for count in [0, -1, 2.5, True]:
            with self.assertRaises(ValueError):
                Graph(count)
        graph = Graph(2)
        for vertex in [-1, 2, 1.5, True]:
            with self.assertRaises(ValueError):
                graph.add_edge(0, vertex)
            with self.assertRaises(ValueError):
                graph.neighbors(vertex)
            for queue_class in BASELINE_QUEUES:
                with self.assertRaises(ValueError):
                    bfs(graph, vertex, queue_class)
        for branching in [0, -1, 1.5]:
            with self.assertRaises(ValueError):
                tree(7, branching)
        for rows, columns in [(0, 3), (3, -1), (1.5, 3)]:
            with self.assertRaises(ValueError):
                grid(rows, columns)

    def test_actual_star_trace(self):
        expected_lines = [
            "enqueue 0 queue = [0]", "dequeue 0 queue = []",
            "enqueue 1 queue = [1]", "enqueue 2 queue = [1, 2]",
            "enqueue 3 queue = [1, 2, 3]", "enqueue 4 queue = [1, 2, 3, 4]",
            "enqueue 5 queue = [1, 2, 3, 4, 5]",
            "dequeue 1 queue = [2, 3, 4, 5]", "dequeue 2 queue = [3, 4, 5]",
            "dequeue 3 queue = [4, 5]", "dequeue 4 queue = [5]",
            "dequeue 5 queue = []",
        ]
        for queue_class in BASELINE_QUEUES:
            with self.subTest(queue=queue_class.name):
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    observed = bfs(star(6), 0, queue_class, trace=True)
                self.assertEqual(output.getvalue().splitlines(), expected_lines)
                self.assertEqual(observed, bfs(star(6), 0, queue_class))

    def test_seeded_random_graphs(self):
        random_source = random.Random(1030)
        for trial in range(100):
            graph = Graph(16, directed=trial % 2 == 1)
            for source in range(16):
                for target in range(16):
                    if random_source.random() < 0.12:
                        graph.add_edge(source, target)
            for source in range(16):
                expected = reference_distances(graph, source)
                self.check_graph(graph, source, expected)


if __name__ == "__main__":
    unittest.main()
