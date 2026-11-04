# Project Objectives

## Project Context

This project investigates how different FIFO queue implementations affect the
performance of Breadth-First Search (BFS) graph traversals. The study is
intended to use Python, subject to explicit approval from Professor Pavel.
The historical C and archived Python versions are recoverable from Git commit
`67559fc98fa604b45f59644d9a5b29a4b4a9213e`; they are absent from the active tree. It evaluates queue behavior across synthetic
graphs with different structures and real-world network data.

## Main Objective

To implement and experimentally compare four FIFO queue data structures used
by BFS, determining how their designs affect:

- Average execution time and throughput.
- Worst-case latency of individual queue operations.
- Latency spikes caused by dynamic memory growth.
- Memory overhead per active queue element.
- Overall BFS performance across different graph topologies.

## Specific Objectives

1. **Implement multiple queue designs**
   - Build a shifting-array queue as a simple baseline.
   - Build a linked-list queue with constant-time insertion and removal.
   - Build a circular array queue with conventional capacity doubling.
   - Build a circular array queue with incremental resizing and gradual
     element migration.

2. **Provide a common and reliable interface**
   - Keep the shared Python enqueue, dequeue and is_empty interface, with
     size and capacity fields (capacity is None for linked nodes).
   - Raise IndexError consistently on empty removal; Python manages storage.
   - Preserve FIFO behavior for every queue, including empty-queue and
     wrap-around cases.

3. **Use the queues in BFS workloads**
   - Parameterize standard BFS over the common queue interface.
   - Support multi-source BFS to produce sustained, high-throughput workloads.
   - Record traversal results and frontier sizes so queue behavior can be
     related to graph structure.

4. **Evaluate behavior on varied graph structures**
   - Test predictable frontier growth using grid and tree graphs.
   - Test sudden frontier expansion using scale-free graphs with high-degree
     hubs.
   - Include random graph models as a general baseline.
   - Include at least one real-world graph dataset to assess practical
     performance.

5. **Measure average and worst-case performance**
   - Measure total BFS runtime and average queue throughput.
   - Capture per-operation enqueue and dequeue latency.
   - Identify maximum and high-percentile operation costs.
   - Correlate latency spikes with queue capacity growth and buffer
     relocation.

6. **Analyze memory efficiency**
   - Measure active element storage, unused capacity, pointer overhead, and
     allocation metadata where applicable.
   - Compare memory overhead per queue element among array-based and
     linked-list designs.
   - Examine the additional temporary memory used during incremental
     migration.

7. **Investigate incremental resizing**
   - Determine whether gradual migration can remove the large latency spikes
     associated with copying a full queue buffer at once.
   - Verify that migration work is distributed across ordinary queue
     operations.
   - Evaluate the trade-off between smoother worst-case latency and any
     additional average runtime or memory cost.

8. **Establish correctness before benchmarking**
   - Validate queue operations with hand-verified unit tests.
   - Test boundary conditions such as empty queues, refill cycles, capacity
     expansion, and circular wrap-around.
   - Use differential testing against a reference queue and confirm that all
     implementations produce identical BFS distance results.

9. **Ensure experimental rigor and reproducibility**
   - Record Python interpreter version and runtime settings, fixed random seeds, and documented
     graph instances.
   - Separate graph construction and other setup work from timed regions.
   - Perform warm-up runs and repeated timed runs.
   - Report robust summary statistics, including medians, interquartile
     ranges, and high-percentile latency.
   - Generate consistent tables and visualizations from recorded benchmark
     results.

## Expected Outcome

The project should establish the practical trade-offs among the four queue
designs and determine whether incremental resizing is an effective way to
maintain strict constant-time queue operations while avoiding the cost spikes
of conventional dynamic array growth. The final results should explain which
queue is most suitable for different BFS workload and graph-structure
profiles, considering both performance and memory use.
