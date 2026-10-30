
from .bfs import bfs
from .queues import BASELINE_QUEUES, CircularArrayQueue
from .sample_graphs import examples
from .generators import star


def run_demo():
    for name, graph, expected_distances, expected_peak in examples():
        print(name)
        expected_visited = 0
        for distance in expected_distances:
            if distance >= 0:
                expected_visited += 1
        expected_counters = {"visited": expected_visited,
                             "enqueue_count": expected_visited,
                             "dequeue_count": expected_visited,
                             "frontier_peak": expected_peak}
        for queue_class in BASELINE_QUEUES:
            distances, counters = bfs(graph, 0, queue_class)
            if distances != expected_distances or counters != expected_counters:
                raise RuntimeError("BFS disagrees with the hand-worked example")
            print("  " + queue_class.name + " distances:", end="")
            for distance in distances:
                print("", distance, end="")
            print(f" | visited={counters['visited']}"
                  f" enq={counters['enqueue_count']}"
                  f" deq={counters['dequeue_count']}"
                  f" peak={counters['frontier_peak']} | hand-check PASS")
    print("Incremental queue: NOT YET IMPLEMENTED. No benchmark results collected.")


def walkthrough():
    print("\nStar walkthrough: circular-doubling, source=0; front is on the left.")
    distances, counters = bfs(star(6), 0, CircularArrayQueue, trace=True)
    print("Distances:", distances)
    print("Counters:", counters)
    print("These are actual BFS events, not performance measurements.")


if __name__ == "__main__":
    run_demo()
    walkthrough()
