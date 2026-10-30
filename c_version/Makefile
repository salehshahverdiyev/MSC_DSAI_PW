CC = cc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic
CPPFLAGS = -Iinclude
QUEUE_SRC = src/queue.c src/queues/shifting_array.c src/queues/linked_list.c src/queues/circular_doubling.c
GRAPH_SRC = src/graph.c src/bfs.c src/samples.c
HEADERS = $(wildcard include/*.h)

.PHONY: all test demo walkthrough clean debug test-failures
all: build/test_queues build/test_bfs build/demo build/walkthrough

build:
	mkdir -p build

build/test_queues: tests/test_queues.c $(QUEUE_SRC) $(HEADERS) | build
	$(CC) $(CPPFLAGS) $(CFLAGS) tests/test_queues.c $(QUEUE_SRC) $(LDFLAGS) -o $@

build/test_bfs: tests/test_bfs.c $(QUEUE_SRC) $(GRAPH_SRC) $(HEADERS) | build
	$(CC) $(CPPFLAGS) $(CFLAGS) tests/test_bfs.c $(QUEUE_SRC) $(GRAPH_SRC) $(LDFLAGS) -o $@

build/demo: src/demo.c $(QUEUE_SRC) $(GRAPH_SRC) $(HEADERS) | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/demo.c $(QUEUE_SRC) $(GRAPH_SRC) $(LDFLAGS) -o $@

test: build/test_queues build/test_bfs
	./build/test_queues
	./build/test_bfs

demo: build/demo
	./build/demo

build/walkthrough: src/walkthrough.c $(QUEUE_SRC) $(GRAPH_SRC) $(HEADERS) | build
	$(CC) $(CPPFLAGS) $(CFLAGS) src/walkthrough.c $(QUEUE_SRC) $(GRAPH_SRC) $(LDFLAGS) -o $@

walkthrough: build/walkthrough
	./build/walkthrough

# Optional fault injection requires a GNU-compatible linker (Ubuntu/WSL).
build/test_alloc: tests/test_alloc.c $(QUEUE_SRC) $(GRAPH_SRC) $(HEADERS) | build
	$(CC) $(CPPFLAGS) $(CFLAGS) tests/test_alloc.c $(QUEUE_SRC) $(GRAPH_SRC) $(LDFLAGS) -Wl,--wrap=malloc,--wrap=calloc,--wrap=realloc -o $@

test-failures: build/test_alloc
	./build/test_alloc

clean:
	rm -f build/test_queues build/test_bfs build/demo build/walkthrough build/test_alloc

debug:
	$(MAKE) clean
	$(MAKE) CFLAGS='-std=c11 -O0 -g -Wall -Wextra -Wpedantic -fsanitize=address,undefined -fno-omit-frame-pointer' test test-failures demo walkthrough
