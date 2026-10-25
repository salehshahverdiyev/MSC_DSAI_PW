# Incremental circular queue: preliminary design

**NOT IMPLEMENTED. No correctness or worst-case bound established.**
`queue_create(QUEUE_CIRCULAR_INCREMENTAL, ...)` returns `QUEUE_UNSUPPORTED`.
M1 supplies baselines; this note defines the next proof/design problem.

Goal: distribute relocation work over queue operations, replacing a full-buffer
copy episode with bounded algorithmic work per successful operation, under
explicit assumptions. Allocation/free latency and page faults remain outside any
constant-copy-work argument; wall-clock maxima still require measurement.

Proposed direction (not approved pseudocode): logical sequence numbers h..t-1
name live entries independent of ring indices. When capacity C fills, allocate
a 2C destination and remember migration boundary b=t at that instant. Old live
entries have IDs below b; new enqueues go to the destination at their reserved
logical positions. A cursor records how much of the old logical interval has
been resolved. Modular slots alone cannot distinguish old generations; explicit
interval/ownership metadata must decide the authoritative location of every ID.

Candidate invariants to prove before coding:

1. Each live ID has exactly one authoritative location. A migration copy can
   temporarily duplicate storage but cannot duplicate the logical item.
2. Peek/dequeue use ID h and its recorded owner, then increment h exactly once;
   enqueue writes ID t after all required allocation succeeds, then increments t.
3. Migration selects the next unresolved pre-b ID, skips IDs already dequeued,
   and never overwrites a slot holding another live ID. New enqueues cannot be
   inserted ahead of unmigrated old entries.
4. Retire old storage only once every still-live pre-b ID is authoritative in
   destination. Reset to a normal ring with an explicit head mapping.
5. Emptying during migration, refill, and failed destination allocation preserve
   the logical sequence and can clean up without dangling owners.

Why naive migration fails: with old FIFO [A,B,C,D], if the first new enqueue E
lands at new[0] and copies append after E, reading new head returns E before A.
If a dequeue removes A and a physical copy cursor still copies its stale slot,
A can be resurrected. Wrapped storage invalidates assumptions that physical
index order is FIFO order. Writing new tail modulo C can overwrite uncopied old
entries even if the final intended destination has ample space.

Capacity/progress problem: at trigger there are C old entries and C additional
slots in a 2C destination. In a run of only enqueues, migration must finish no
later than those C slots fill. Scheduling k copies per operation gives a useful
counting intuition but does not prove slot disjointness or completion under
interleaved dequeues. Need a progress measure such as unresolved pre-b live IDs,
with a proof that every successful operation either resolves at least one old
ID or reduces the obligation, while enqueue demand cannot outrun available
destination slots. Specify whether the triggering enqueue also migrates; avoid
an off-by-one deadline. Prove no second growth is needed before retirement.
Shrinking is excluded initially; it would add another interacting migration.

Unresolved: exact destination mapping and head-owner lookup in O(1), wrapped
logical epochs without integer overflow, migration budget and ordering relative
to enqueue/dequeue, all-dequeue migration, reuse of consumed slots, OOM rollback
and bounded finalization. Bulk allocation/free is an explicit assumption/caveat,
never a consequence of the copying proof. Compare peak requested dual-buffer
bytes including unused slots. No k=2 guarantee is asserted.

Validation planned before integration: small-capacity state enumeration against
a fixed FIFO oracle; force wrap at every head offset and migrate after alternating
enqueue/dequeue; long only-enqueue/only-dequeue phases; drain/refill mid-migration;
capacity-deadline tests; failure injection at every allocation; logical-counter
overflow simulation; invariants checked after each operation; ASan/UBSan.
Only then add BFS parity and diagnostic copy counters. M2 needs explicit approval.
