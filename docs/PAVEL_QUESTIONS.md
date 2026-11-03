# Fifteen source-code questions to rehearse
1. Why does bfs assign distances before queue.enqueue? It marks discovery and prevents duplicate insertion.
2. Why is the first discovered distance shortest? FIFO processes layers in increasing distance.
3. What does -1 mean? Unreachable or undiscovered; source is zero.
4. Trace the shifting dequeue loop. Each remaining reference moves left once; size-1 shifts.
5. Why clear the freed array slot? Release the queue’s reference to the removed payload.
6. Why reset linked tail when size becomes zero? Otherwise the next enqueue could attach to a removed node.
7. Can queues store None? Yes; size, not payload value, determines emptiness.
8. Explain (front + size) % capacity. It identifies the next free tail slot, including wrap-around.
9. Why copy (front + index) % capacity during growth? Physical index order may differ from FIFO order.
10. Why reset front after growth? Copied FIFO data starts at new index zero.
11. How do the counters avoid estimating work? Each shift/copy increments inside its executed loop; tests check exact totals.
12. Why is capacity_history empty for the linked queue? It has nodes rather than a reserved array; this does not imply zero memory.
13. What does with_stats change? Only the return value and collected diagnostics; default callers still receive distances.
14. How is the real graph interpreted and checked? i j w means j->i, positive weights only, zero-based IDs, deduplicated pairs; independent relaxation verifies distances.
15. Why is incremental resizing unfinished? FIFO ownership and migration deadlines need proof, and Python bulk allocation remains linear even if copy work is spread.
