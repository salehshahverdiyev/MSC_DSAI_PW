from .queues import ShiftingArrayQueue, CircularArrayQueue
from .bfs import bfs

def main():
    path = [[1], [0, 2], [1, 3], [2, 4], [3, 5], [4]]
    star = [[1, 2, 3, 4, 5], [0], [0], [0], [0], [0]]

    examples = [
        ("Path", path, [0, 1, 2, 3, 4, 5]),
        ("Star", star, [0, 1, 1, 1, 1, 1]),
    ]
    print("T10 learning subset: source vertex = 0")
    for name, graph, expected in examples:
        print(name)
        for queue_class in (ShiftingArrayQueue, CircularArrayQueue):
            distances = bfs(graph, 0, queue_class)
            if distances != expected:
                raise RuntimeError("BFS distances do not match the hand answer")
            print(" ", queue_class.__name__, distances, "PASS")
    print("Both queues match the hand answers.")


if __name__ == "__main__":
    main()
