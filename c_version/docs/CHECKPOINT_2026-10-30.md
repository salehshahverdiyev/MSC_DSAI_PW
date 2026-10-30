# Friday checkpoint — 2026-10-30

Preserved C reference checkpoint. Unqualified `make` commands below run inside
`c_version/`; from the repository root use `make -C c_version <targets>`.

Six-slide Markdown outline, approximately five minutes. M1 prototype; no final
defence deck or measured performance charts are claimed.

## Slide 1 — Research question (40 seconds)

> In BFS-based algorithms on graphs of different structure, including a real-life graph, how do a shifting-array queue, a linked-list queue and circular-array queues compare in average time, worst-case time of a single operation and memory, and can incremental resizing remove the cost spikes caused by frontier growth?

Same BFS, interchangeable FIFO. Authors: Javidan Hajizada and Saleh Shahverdiyev.

## Slide 2 — Frontier pressure (40 seconds)

```text
Path: 0--1--2--3--4--5      Star:      1
                                    |
                                2---0---3
                                   / \
                                  4   5
```

Source 0: path peak live queue 1, star peak 5. Shifting work depends on the sum
of occupancies at removal, not universally V². These are correctness counters.

## Slide 3 — Contract and implementation status (45 seconds)

FIFO int values copied by value; queue owns storage; caller destroys it.
Empty dequeue/peek returns EMPTY with unchanged output; allocation failure
preserves FIFO. Arrays start at 4, double on full, never shrink.

| Queue | Status | Algorithmic work |
| --- | --- | --- |
| Shifting | Working/tested | dequeue O(q), insertion amortized O(1) |
| Linked | Working/tested; capacity N/A | constant pointer work; allocator latency varies |
| Doubling ring | Working/tested | amortized O(1), O(q) growth copy |
| Incremental ring | Design only; API returns UNSUPPORTED | bound unproven |

Migration must preserve old/new ownership and complete before capacity fills.
Copy-work bounds alone do not bound allocation or elapsed time.

## Slide 4 — Correctness evidence (45 seconds)

`make test`: 50,000 seeded FIFO steps per baseline plus boundary/refill tests;
100 small graphs x 16 sources x three queues against repeated edge relaxation.
Explicit head!=0 ring-resize regression and hand path/star/diamond checks.
`make test-failures`: allocation failure sweeps, including partial BFS cleanup.
`make debug`: ASan/UBSan tests, fault injection and demo. All passed on Ubuntu
WSL/GCC 13.3, 2026-10-25. Finite tests are evidence, not exhaustive proof.

## Slide 5 — Live prototype (70 seconds)

Begin with `make walkthrough` for the actual star FIFO event trace (same BFS,
circular-doubling queue). Explain that processing 0 discovers five leaves;
the leaves then leave the queue in discovery order. Final distances are
`0 1 1 1 1 1`, peak 5. The display follows runtime events; it is not a second BFS.
Exact PowerShell learning command:

```powershell
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version walkthrough
```

Then use the regular demo below to show agreement across all three baselines.

From repository root in Ubuntu/WSL:

```sh
make -C c_version clean
make -C c_version all
make -C c_version test demo
```

Exact development-PC PowerShell commands:

```powershell
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version clean
wsl -d Ubuntu -- make -C /mnt/c/Users/javid/MSC_DSAI_PW/c_version all test demo
```

One-command demo: the second PowerShell command, or `make test demo` in WSL.
Expected output under each queue (source 0, -1 unreachable):

```text
path:    0 1 2 3 4 5    visited=6 enq=6 deq=6 peak=1
star:    0 1 1 1 1 1    visited=6 enq=6 deq=6 peak=5
diamond: 0 1 1 2 3 -1   visited=5 enq=5 deq=5 peak=2
```

Diamond: 0->1,0->2,1->3,2->3,3->0,3->4; vertex 5 isolated.
The demo checks every printed distance against hand expectations and exits
nonzero on failure. No timing results exist.

## Slide 6 — Experimental plan and unfinished work (60 seconds)

Proposed [NADINE C. elegans](https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/)
summed neural links: source describes 279 neurons; local counts/loading pending.
Preserve directed j->i orientation; use positive-weight unweighted projection.
See [DATASET_DECISION.md](../../docs/DATASET_DECISION.md) for provenance,
acquisition, hashing and reachability.

H1 occupancy-dependent shifts; H2 doubling copy peaks; H3 possible incremental
copy smoothing at memory/bookkeeping cost; H4 empirical list locality/allocator
trade-offs. Identical inputs, setup outside timing, repeated warmed runs,
median/IQR, documented failures and caps. Protocol **DRAFT**; no freeze today.
Proposed pilot: 3 warm-ups, 11 runs, 5 seconds/run, 256 MiB requested storage.
Those settings are not enforced or validated by M1. Before freezing at the
actual review resolve the pilot, size/source manifest, timer calibration and cap
enforcement; record unresolved items with Pavel rather than claiming readiness
for final measurements. Record freeze date/version/settings and later amendments.

Missing: fourth queue/proof, real loader, timing/memory harness, larger production
generators, multi-source BFS and final slides. After new approval, establish
migration ownership/progress, test it, integrate real data, finalize protocol,
then benchmark. M1 work stops here.

## Rehearsal checklist

- Both students run exact commands and explain FIFO, wrap+resize and oracle.
- Explain amortized vs worst individual work and timing overhead.
- Explain why copy bounds do not bound allocator/scheduler latency.
- Review candidate with Pavel; record feedback and protocol freeze decisions.
- Keep every incomplete component and unsupported numerical claim explicit.
