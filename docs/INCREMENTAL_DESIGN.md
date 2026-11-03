# Incremental circular resizing — design only
Mandatory final queue; not implemented or proved. Ordinary doubling copies C live references in one full-buffer enqueue, plus allocation of 2C slots. Total copies across growth are geometric, explaining amortized constant copying but not constant work for each enqueue.

Candidate mapping: logical sequence numbers h through t-1 identify live items. Start growth at capacity C with boundary b=t and original head a=h. Old entries occupy old[id % C]; new destination uses new[id % (2*C)]. Keep cursor m starting at a. IDs below m have been resolved; live IDs in [m,b) remain authoritative in old. New IDs >=b go directly to new. Resolve a bounded number of logical IDs on every successful enqueue/dequeue, including the triggering enqueue. A resolved ID already dequeued is skipped; a live one is copied and its old reference cleared. Dequeue reads h from its authoritative buffer according to boundary/cursor, clears it, and increments h. Enqueue writes t and increments t. Read order follows logical IDs, never physical slot order. Starting a migration must preserve the old head mapping, especially after wrap-around.

Proof obligations before code:
1. Every live ID has exactly one authoritative owner, even if physical copies briefly coexist.
2. Destination modulo slots are disjoint for all live IDs while live span is at most 2C; no overwrite of another live value.
3. Dequeued IDs cannot be copied back; cursor advancement over consumed IDs must itself be bounded work, not an unbounded scanning loop.
4. At most C original IDs need resolution. A budget of at least one resolved ID per successful operation, including trigger, should finish within C operations. Show completion before a next growth is needed, accounting for the triggering enqueue and interleaved dequeues. This is a proposed counting argument, not a completed implementation proof.
5. Retirement and normalization preserve ID-to-slot mapping and perform no bulk copy. Empty/refill mid-migration and allocation failure leave valid state.

Keep both buffers until all old obligations are resolved. Peak backing slots can be 3C, plus Python objects and metadata. No shrinking initially. Tests must force each wrap offset, only-enqueue and only-dequeue phases, drain/refill, alternating operations, small capacities, allocation failures and migration deadlines; compare every result with deque.

Python caveat: [None] * (2*C) initializes O(C) slots. Releasing buffers and reference counts also costs work, logical Python integers are not fixed-width, and allocator/GC/scheduling effects remain. Bounded migration copies cannot justify worst-case O(1) Python operation time. A stronger guarantee needs explicit allocation assumptions or a different storage design. Checkpoint readiness takes precedence over an unproved implementation.
