# Experimental protocol v0.1
protocol_status: DRAFT

No performance data collected. Freeze date: none. Numerical timing settings,
source manifest and resource caps require a feasibility pilot and student/teacher
review before freezing at the actual intermediate checkpoint. This is a concrete
draft, not a claim of readiness to collect final data today. Record freeze date,
version, every finalized setting and later amendments here.

Use the charter's H1-H4. Compare identical stored graphs, insertion-order
neighbors, source IDs and FIFO traces across queue kinds. Synthetic conditions:
path, star/branching tree and grid at increasing sizes (sizes TBD after pilot).
Real candidate: NADINE C. elegans; directed unweighted projection, source rule
below. Fix generator seeds and all graph hashes in a manifest before timing.
M1 queue-test seed is 20261030, not an experimental graph seed.

Source rule proposed: smallest mapped ID plus a fixed high-outdegree vertex
(ties by original ID); report each separately and reachable counts, including
unreachable vertices. Finalize this rule before observing comparative timings.
Do not silently make a directed graph undirected to improve reachability.

Correctness gate: tests and independent reference distances must pass for each
implementation. M1 covers only three baselines. Prepare/loading/verification
outside timing. Run untimed warm-ups; proposed pilot 3 warm-ups and 11 measured
runs per case, 5 seconds/run and 256 MiB requested-memory cap. These are provisional,
not implemented or enforced by the M1 program. Pilot must validate timeout and
memory enforcement, then fix counts/caps, compiler flags and seeds before freeze.
Rotate queue order deterministically; record per-run raw observations, median
and IQR (Q1/Q3 method to be fixed), failures/timeouts/OOM without removing them.

Throughput path excludes per-operation timestamps and diagnostic logs.
Diagnostic path records copies, allocation events, occupancy and sampled latency
separately. Calibrate clock resolution and empty measurement overhead; batch
operations or sample where single operations are below timer resolution.
Batch averages cannot identify a single-operation maximum. Monotonic clocks do
not remove scheduling/allocator/cache noise. Report observed maxima, not a
worst-case wall-clock guarantee or exact nanoseconds.

Counter definitions:

| Counter | Definition / M1 status |
| --- | --- |
| enqueue_count / dequeue_count | successful operations, including source enqueue; implemented in BFS |
| visited | successful dequeues; implemented |
| frontier_peak | maximum live queue occupancy after any successful operation, including source; implemented; not whole-level width |
| copies_per_operation | moved int elements due to shifts/migration/resize, excludes normal insertion; future |
| resize_event | one successful capacity increase, not failed allocation; future |
| reserved_queue_bytes | requested backing buffers/nodes, including unused array slots and both migration buffers; future |
| live_queue_bytes | logical size times sizeof(int); future |
| peak_queue_bytes | maximum simultaneous requested bytes including queue metadata and transient growth buffers; future |
| time_ns | elapsed measured interval converted to ns, accuracy reported separately; future |

Memory/element = current requested queue bytes (metadata plus reserved storage)
/ live elements; N/A when zero. Report sizeof(Node) including padding separately
from hidden allocator metadata (not portably exact). Record initial capacity,
no-shrink policy and temporary old+new allocations.

Future row schema: protocol version, graph hash/family/n/m/direction, source,
kind, seed, run/order, warmup flag, status/timeout/cap, elapsed time, operation
counts, peak occupancy, copy/resize counters, requested memory, compiler/version/
flags, OS, CPU, timer resolution/overhead and timestamp. Record environment noise
and variation. No harness, memory profiler or timing output exists in M1.
