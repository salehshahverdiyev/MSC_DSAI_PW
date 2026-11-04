"""Small correctness and algorithmic-work demonstration; no timing."""
import argparse
from .queues import BASELINE_QUEUES
from .bfs import bfs
from .graph import path_graph, star_graph, tree_graph, grid_graph


def examples():
    return [
        ("Path", path_graph(6), [0, 1, 2, 3, 4, 5]),
        ("Star", star_graph(6), [0, 1, 1, 1, 1, 1]),
        ("Binary tree", tree_graph(7), [0, 1, 1, 2, 2, 2, 2]),
        ("Grid 2x3", grid_graph(2, 3), [0, 1, 2, 1, 2, 3]),
    ]


def compare(name, graph, expected, compact=False):
    print("\n" + name + " (source 0)")
    for queue_class in BASELINE_QUEUES:
        distances, stats = bfs(graph, 0, queue_class, with_stats=True)
        if distances != expected:
            raise RuntimeError("BFS result mismatch")
        print(queue_class.__name__, "PASS")
        if not compact:
            print("  distances:", distances, "visited:", stats["visited"])
        else:
            print("  reachable:", len(stats["visited"]), "/", len(graph))
        print("  enqueues={enqueues} dequeues={dequeues} peak={peak} "
              "shifted={shifted} copied={copied} resizes={resizes} "
              "capacities={capacity_history}".format(**stats))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", help="optional local ssumlinks.txt")
    args = parser.parse_args()
    print("T10: exact work counters, NOT timing benchmarks")
    for name, graph, expected in examples():
        compare(name, graph, expected)
    if args.dataset:
        from .dataset import load_worm
        graph, summary = load_worm(args.dataset)
        print(summary)
        compare("C. elegans", graph, bfs(graph, 0, BASELINE_QUEUES[0]), compact=True)


if __name__ == "__main__":
    main()
