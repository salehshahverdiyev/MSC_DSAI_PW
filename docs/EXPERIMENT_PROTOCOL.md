# Python experiment protocol v0.1 — DRAFT, NOT FROZEN
No final timing or memory experiments have been run. Correctness demos and work counts are not timing pilots.

## Hypotheses recorded before timing
H1: increasing frontier occupancy increases shifting work and likely runtime.
H2: doubling has amortized O(1) enqueue copy work but O(n) growth operations.
H3: incremental migration can spread copying, with extra bookkeeping and temporary memory; wall-clock spikes may persist from allocation.
H4: linked-node overhead may exceed array cost per live element, while arrays retain unused capacity. Measure rather than assume a winner.

## Paired design
Use identical stored path, star, tree, grid and seeded random adjacency lists for each queue. Candidate synthetic sizes: 100, 1000, 5000 vertices; feasibility pilot may reduce them. Seeds: 20261103, 20261104, 20261105. Include directed C. elegans with raw hash in DATASET_DECISION.md. Proposed sources: vertex 0 and maximum outdegree vertex, ties by smallest ID; report separately. Pin graph hashes, source IDs and neighbor ordering before timing. Validate distances first. Include all four queues only once incremental passes its gates.

## Timing
Propose 3 warm-ups and 11 paired measured repetitions per graph/source; deterministic rotating order, same inputs each pair. Exclude loading, generation, correctness comparisons and printing. Use perf_counter_ns; record clock resolution and measurement overhead. Time total BFS separately from individual enqueue/dequeue operations. Single-operation timestamps need a separate diagnostic pass and overhead calibration; batched timings cannot establish a maximum single operation. Counters are currently always enabled; first quantify their overhead with a reviewed counter-disabled equivalent before freezing the timing implementation. Preserve instrumented and uninstrumented code hashes. Never infer elapsed time from work counters.

Report median, Q1/Q3 with statistics.quantiles(method='inclusive'), IQR, all raw samples and paired runtime ratios. For operation diagnostics report observed maximum and p95/p99 with a frozen nearest-rank rule, never a mathematical worst-case latency guarantee. Use independent seeded graph instances for structure-level inference; repetitions of one instance are not independent graphs. Proposed uncertainty analysis: paired bootstrap over independent graph instances, fixed seed and resample count finalized before freeze. Avoid broad statistical claims from one small real graph.

## Memory and resources
Run memory diagnostics separately using standard-library tracemalloc; create graph before tracing and retain it across comparisons. Record baseline, incremental peak, retained bytes, interpreter version and limitations: traced Python allocations are not whole-process RSS or complete allocator overhead. For structural accounting include queue object, node dictionaries/links, unused array slots and simultaneous old/new buffers; count shared payload objects only once under an explicit policy. Capacity is not bytes. Reset tracing per case; define payload ownership and GC policy before freeze.

Proposed caps: one worker, 5 seconds per case, 256 MiB process budget, 5000 synthetic vertices. These limits are NOT currently enforced. Future harness must use subprocess timeouts and validate a Windows memory-enforcement mechanism before freeze, or reduce sizes and adopt an explicit measured-memory abort policy with its overshoot limitation. Log timeout, OOM and aborted cases; never silently remove them or report them as completed timings. No heavy dependencies or final runs now.

## Exact current counters
- shifted_elements: reference assignments inside the shifting dequeue loop; excludes clearing the last slot.
- copied_elements: live reference assignments from old to new buffer inside growth loops; excludes normal enqueue, None initialization and interpreter internals.
- resize_events: successful completed array capacity increases.
- max_size / BFS peak: largest live size after a successful enqueue, including source; not necessarily whole-level width.
- capacity_history: initial reserved slot count followed by each completed doubled capacity; linked queue has [] and capacity None. Neither is a memory measurement.
- BFS enqueues/dequeues: successful calls, including initial source enqueue; visited lists vertices in dequeue order. Empty failures are excluded.
All counters accumulate per fresh queue instance. No shrinking. Counter integer arithmetic and history storage add overhead.

## Freeze procedure
Run a lightweight feasibility pilot only after labeling it PILOT. Finalize sizes, seeds, hashes, sources, repetitions, queue ordering, GC policy, timing boundaries, memory accounting, overhead controls, percentile/bootstrap rules and enforced limits. Obtain team/professor approval; record approval, date, protocol version and source hash. Preserve the frozen protocol and raw observations. Any change requires a dated amendment and separate results or reruns. Do not run final experiments while this document is DRAFT.
