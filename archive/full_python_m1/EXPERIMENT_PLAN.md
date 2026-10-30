# Archived Python M1 experimental plan

protocol_status: DRAFT
Language approval: PENDING
Benchmark data: NONE
Memory-byte measurements: NONE
Freeze date: NONE

This archived plan preserves the official research
question and final deliverables. The original C charter/protocol are preserved
under [c_version/docs/](../../c_version/docs/EXPERIMENT_PROTOCOL.md); this plan does
not freeze or silently amend them. Course-level Python approval must still be
recorded with Pavel. The
teacher specification available here is transcribed in the existing brief, not
an independently located original PDF/DOCX. No teacher approval is inferred.

## 1. Predictions before experiments

- H1: sustained large queues cause more shifting work than narrow path frontiers.
  Count shifts as the sum of q_before-1 over successful dequeues. Path cost need
  not be quadratic; center-source stars can exhibit quadratic total shifting.
- H2: doubling concentrates copy work in a single enqueue when full; ordinary
  operations remain cheap in the algorithmic model. List initialization, old
  buffer disposal and Python overhead contribute additional measured work.
- H3: a correct incremental algorithm might spread relocation work, at extra
  bookkeeping/storage cost. A bounded-copy budget does not bound allocation,
  list initialization, buffer reclamation or wall-clock maximum latency.
- H4: linked nodes have object/dictionary/reference overhead and different
  locality/allocator behavior. Do not predict numerical overhead or rankings.

No hypothesis has a measured performance answer yet. Rewriting in Python does
not establish a speed improvement over C or make C measurements interchangeable.

## 2. Identical inputs and frontier profiles

Already implemented deterministic undirected generators:

| Function | Structure / source 0 behavior | Size / edge count |
| --- | --- | --- |
| path(n) | Narrow frontier from endpoint | n vertices, n-1 edges |
| star(n) | Center discovers n-1 leaves at once | n vertices, n-1 edges |
| tree(n, branching=2) | Breadth expands over levels | n vertices, n-1 edges |
| grid(rows, columns) | Expanding and contracting spatial wave | rows*columns vertices; rows*(columns-1)+(rows-1)*columns edges |

Grid IDs use row*columns+column; add only right/down undirected edges to avoid
double construction. Tree parent is (v-1)//branching. Positive sizes required;
one vertex is supported. These generators use no randomness and require no seed.
Additional seeded random/hub families and multi-source BFS remain future scope.
Current random inputs are correctness tests (seeds 20261030/1030), not benchmark
instances or a mandate to use those seeds for future experimental graphs.

Construct each graph once outside timing; reuse that exact adjacency order and
source across queues. Record graph instance/hash, sizes, direction, generator
parameters, source, seeds and reachable counts in a manifest. Pair queue runs on
the same case and repeat; rotate order deterministically to avoid always testing
one queue warm/last. Generate an untimed operation trace if measuring queue-only
workloads; all queues replay identical values and enqueue/dequeue operations.

## 3. Real-world candidate and preprocessing

See [existing decision](../../docs/DATASET_DECISION.md). Candidate source:
[NADINE C. elegans page](https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/),
linked from the teacher's FET NADINE collection. The source-reported matrix is
279x279; this is not a local count. Exact local edges, ID coverage, components
and reachable counts: **UNVERIFIED**. No raw dataset found or ingested here.
No new source statistics verified during the Python foundation task.

Planned file is ssumlinks.txt: three columns interpreted as i, j, weight with
header j->i. Verify this orientation and neuron table before loading; map source
j to target i, convert IDs deterministically, retain positive-weight edges but
ignore magnitudes for unweighted BFS. Do not use the dense Google transition
matrix or silently reverse/undirect the biological graph. Preserve isolates via
verified ID roster. Retain self-loops initially; deduplicate directed pairs and
record before/after counts, stable order and all preprocessing choices. Freeze
source rule before comparative timings (candidate: smallest mapped ID plus a
separate high-outdegree source with deterministic tie rule). Report reachable/
total and -1 distances, not an assumption of complete reachability.

Later acquire from the documented link, record date/source/hash, validate strict
parsing and counts against source, hand-check a small subset then use an
independent oracle. No loader/download is implemented here. Tiny real networks
may not create large growth events, so synthetic controls remain necessary.

## 4. Counters and work accounting

Implemented BFS counters match the C definitions on successful completion:

| Counter | Exact population |
| --- | --- |
| visited | Successful dequeues; each processed reachable vertex once |
| enqueue_count | Successful enqueue calls including initial source |
| dequeue_count | Successful dequeue calls |
| frontier_peak | Maximum pending occupancy after a successful operation, includes initial source |

storage_info() provides live size; arrays' logical reserved slots and unused
slots; lists' live node count, capacity/unused=N/A. No byte or timing inference.
to_list()/trace output is diagnostic O(q) work; exclude it from all timed paths.

Future diagnostic counters: reference copies/moves from shifting/resize/migration
per operation, one resize_event per successful growth, old/new capacities and
temporary coexisting storage. Define whether vacated-slot clearing and `[None]*C`
initialization count separately (proposed: separate counters). Algorithmic-copy
peaks, actual initialized slots and elapsed latency are different quantities.

## 5. Timing plan: throughput and individual latency stay distinct

Correctness must pass first, including the future fourth queue, on all intended
inputs. No tests-as-benchmarks or performance claims from demonstration output.
Fix interpreter implementation/version/build, OS/CPU, power/affinity policy if
used, flags/environment, GC policy, seeds and input manifest. Record variation.

Use perf_counter_ns for elapsed intervals, with timer properties/resolution and
empty-measurement overhead calibrated on the actual environment. A nanosecond
return unit is not nanosecond accuracy. Very short operations may be below
resolution or dominated by timestamp overhead. Scheduling/preemption remains.

Separate paths:

1. **Throughput / batch average:** prepare inputs, payloads and output buffers
   outside timing. For queue-only enqueue/dequeue measurements replay identical
   traces with per-type totals using suitable runs/batches. A fill-only enqueue
   batch and drain-only dequeue batch have different occupancy profiles: label
   them and do not imply they represent BFS. In mixed BFS traces, explicitly
   account for attribution/loop overhead before calling a value “enqueue time”
   or “dequeue time.” Overall BFS elapsed/total_ops is a combined average only.
2. **Latency diagnostic:** in separate runs timestamp selected individual enqueue
   and dequeue operations with operation ID/type/occupancy/capacity/resize info.
   Store records without per-op print/I/O. Quantify timestamp/logging perturbation.
   Report sampled population, distribution/quantiles and maximum observed value,
   with resolution/noise limitations. A sampled maximum misses unsampled ops.
3. **Repeated operations / batches below resolution:** repeat a well-defined
   sequence in independent reset trials or bracket batches large enough to
   dominate overhead. Divide elapsed by count only to estimate a batch average.
   Replaying changes state/caches; reproduce the same occupancy/events. A batch
   average is not a single-operation maximum and cannot prove a worst-case bound.

Untimed warm-up, repeated measured paired runs, raw records, median and spread
(IQR/quantile method fixed beforehand), deterministic run order. Proposed pilot
starting points inherited from the C draft: 3 warm-ups/11 measured runs, 5 seconds
per run, 256 MiB requested storage. **Not validated, enforced or frozen for Python.**
Python metadata makes “requested storage” enforcement harder; choose a clearly
measured cap and timeouts with a tested process-level enforcement mechanism
before final data. Avoid an in-process check that only happens after a slow
operation completes. Retain timeout/OOM/cap statuses and denominators; never drop
inconvenient cases or shorten only one queue's graph invisibly.

Interpreter dispatch/reference counting, garbage collection, allocator arenas,
OS scheduling, caches and list/node implementation details are confounds, not
proof failures. Baseline measured loops are explicit Python loops (C version
uses memmove for shifting); conclusions apply to the tested implementations and
runtime. Record default-GC behavior; if also disabling cyclic GC for diagnostics,
label the condition, restore it and do not imply reference counting/allocation
cost disappears. No promise of exact hardware-level operation costs.

## 6. Memory measurement plan

Python lists hold references; ints are objects, often shared between graph,
queue and interpreter caches. A Node has a value reference, next reference and
ordinary object/__dict__ overhead. Array `capacity` means len(data) reserved
logical reference slots, not the precise bytes reserved by every Python allocator.
Unused slots matter even though they point to shared None. No shrink means
retained capacity follows historical peak rather than just current occupancy.

Define metrics before collecting:

- **Logical storage:** current q, C, unused C-q, live nodes. Available now via
  storage_info; no total-byte claim. Linked capacity/unused is N/A, not zero.
- **Structural shallow components:** sys.getsizeof(queue) + its __dict__ + array
  list, or queue/__dict__ + each live Node/__dict__. Count each structural object
  once. Clearly state exclusions: referenced metadata ints/payload objects,
  hidden allocator fragmentation/arenas, graph, external references. This is a
  reproducible component metric, not total process or total reachable memory.
- **Optional inclusive retained estimate:** traverse specifically defined queue-
  owned metadata/payload objects with identity deduplication; state whether shared
  graph IDs/None/interned ints are excluded or attributed. Do not multiply an
  int's getsizeof by C as if every slot owns an independent int object.
- **Allocated/peak diagnostic:** isolated queue trials with baseline-subtracted
  tracemalloc snapshots/peak resets, inputs prepared beforehand and instrumentation
  recorded. Traced allocations include other Python work, not exclusively queue;
  they are not necessarily process RSS or every native allocation. Keep separate
  from sys.getsizeof and separate from time-only trials.
- **Process memory:** if later measured, label RSS/high-water/process-wide and
  environment-specific enforcement; it includes interpreter, graph, allocator
  caches and output. It is not queue-only memory.

Per-element structural bytes = defined structural total/q; N/A at q=0. Also
report absolute bytes/peak and occupancy/capacity. A doubling operation can have
old C and new 2C lists simultaneously; incremental resizing may retain both for
many operations. Capturing only final queue state misses transient peaks. Record
allocation/reclamation events in a separate diagnostic design before claiming
peak memory. No byte measurements produced by this implementation phase.

## 7. Incremental resizing: educational design, NOT YET IMPLEMENTED

Doubling currently does an O(C) copy at full size q=C and creates a new 2C-slot
list. Incremental copying aims to spread relocation across subsequent operations
while using old/new buffers temporarily. A useful conceptual model numbers live
FIFO elements h..t-1, records boundary b=t when growth starts, and keeps a cursor
of unresolved old entries below b. Newly enqueued IDs >=b go to reserved new
locations; old live entries remain authoritative in old or copied new locations.
This is a proposed model, not executable code or a proven indexing scheme.

To claim a bound, establish all of these, under an explicit cost model:

1. Every live element has exactly one authoritative logical owner; physical
   temporary copies cannot cause duplicate dequeue results.
2. Dequeue/peek finds logical oldest h regardless of buffer. A dequeue that
   removes an uncopied old element must remove/skip its migration obligation.
3. New enqueues cannot precede old live items or overwrite live/unmigrated slots.
   Wrapped ring indices and consumed-slot reuse must be handled explicitly.
4. Each successful operation reduces a measurable migration obligation, or
   reduces old live occupancy; work per operation is bounded, including finding
   skipped/dead positions (no unbounded scan hidden in a helper).
5. Migration completes before another growth is required. In enqueue-only runs,
   C extra destination slots are consumed in C insertions; budget/progress must
   meet that deadline including the trigger insertion. Interleaved removals,
   drain/refill and capacity reuse cannot violate space or FIFO.
6. Allocation failure, finalization, integer/index assumptions and storage
   reclamation have explicit treatment; shrinking is initially excluded.

Counterexample: old [A,B,C,D], new enqueue E at the new buffer's front, then
reading new before old returns E before A. Copying A's old slot after dequeue
can resurrect A. Therefore “copy two per operation” alone proves neither FIFO
nor capacity safety. No k=2 performance guarantee is asserted.

**Python-specific obstacle:** `[None] * (2*C)` itself initializes O(C) slots;
disposing a C-slot list can also do linear reference-release work. Simply
spreading the copy loop would NOT make the whole Python operation worst-case
O(1) algorithmic work. A final design must either provide a justified storage/
preparation/reclamation strategy that meets the full bound, or explicitly obtain
agreement on a restricted relocation-work model with allocation/initialization
excluded and report those costs separately. Do not silently redefine the
teacher's requirement or call that restricted claim a complete solution.
Any bounded-work claim also assumes bounded-cost integer/reference operations;
Python arbitrary-size integers are not unit-cost without bounds/assumptions.
Allocator/GC/wall-clock latency remains empirical even with a valid model.

Before coding: discuss cost-model feasibility, state/prove FIFO, progress and
space invariants, enumerate small-state/adversarial traces, then implement and
test against the independent oracle (wrap/growth/drain/refill/failures). No fourth
class is exported and no BFS result claims a fourth implementation exists.

## 8. Final evidence and freeze checklist (future work)

- Record outstanding course-level language approval and agree on the cost model
  for the primary Python implementation.
- Prove and implement fourth queue without hiding whole-buffer work.
- Verify real-data loader, actual counts/hash/preprocessing and reachability.
- Expand workload manifest/source rules and correctness for all four queues.
- Pilot timers, attribution, memory/cap enforcement, repetitions and feasibility.
- Freeze actual approved protocol version/settings/date; log later amendments.
- Collect paired raw runs, distributions/medians/spread, copy/resize/frontier
  correlations and memory (including unused/transient storage).
- Report negative/null findings and all failures; prepare final defence slides.

This foundation stops before those experiments. No artificial results, claims
of spike removal, frozen date or completion of the four-queue study are supplied.

