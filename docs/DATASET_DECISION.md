# Real-world dataset decision (M1 candidate)

Status: **PROPOSED; not downloaded, parsed or traversed locally**.
Source pages inspected online on 2026-10-25. No locally measured graph counts.

Preferred candidate: C. elegans neural network, following entry 18 of the
teacher's [FET NADINE collection](https://www.quantware.ups-tlse.fr/FETNADINE/datasets.htm).
The [dataset page](https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/)
describes a 279 x 279 matrix and links to synaptic, gap and summed connections.
Use **summed biological links**, not the dense Google transition matrix G.
Provenance: V. Kandiah and D. L. Shepelyansky,
[Google matrix analysis of C.elegans neural network](https://arxiv.org/abs/1311.2013),
2013 preprint / Physics Letters A 378 (2014), 1932.

Claimed size: 279 neurons on the source matrix page. Exact unique edge count,
identifier coverage, self-loops and duplicates remain to be checked after local
download; no edge-count claim is inferred from a partial browser rendering.
Small size makes independent verification feasible but may be insufficient to
stress large queue growth; synthetic graphs will cover that range.

Raw candidate [ssumlinks.txt](https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/ssumlinks.txt)
is accessible as text. Its header says **j points to i** and rows contain three
columns, so treat a row `i j weight` as an edge **j -> i**. Weights represent
synapse+gap link weights. Example observed first row `2 1 1` maps to 1->2,
then zero-based IDs 0->1. Verify orientation against the accompanying paper and
neuron-ID table before freezing the final loader; do not silently transpose it.
For unweighted BFS retain edges with positive weight, ignore weight magnitude,
preserve directedness, and disclose this projection. Reachability is source
dependent; report reachable/total rather than assuming all neurons reachable.

Acquisition plan (future milestone, commands from Linux/WSL repo root):

```sh
mkdir -p data/raw
curl --fail --location https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/ssumlinks.txt -o data/raw/ssumlinks.txt
sha256sum data/raw/ssumlinks.txt
```

Record retrieval date, raw SHA-256 and source attribution. Inspect header and
full rows; obtain the neuron table via the dataset page (its browser link did
not load in this session) to account for isolates. Implement a strict C loader
with line diagnostics, comment handling, three-column validation, range checks,
deterministic ID mapping and stable adjacency ordering. Preserve raw data;
deduplicate directed pairs and disclose loop policy and before/after counts.
Keep self-loops initially (BFS discovery skips revisits). Validate a hand subset
and all distances with an independent reference; then compare the three queues.
Pin mapped sources before comparative timings; report isolated/unreachable nodes.
The acquisition commands are a plan, not commands run during M1.

Backup only, subject to student/teacher agreement:
[SNAP Wiki-Vote](https://snap.stanford.edu/data/wiki-Vote.html), directed votes
between Wikipedia users, not article hyperlinks. Published whole-graph statistics
are 7,115 nodes / 103,689 edges; these are source claims, not local measurements.
It is a larger possible complement if the neural graph is too small; no switch
or download has been made. The SNAP page also supplies a gzip edge-list link.

No dataset redistribution license was verified. Keep raw downloads excluded;
provide verifiable source/download instructions and attribution. Do not present
the synthetic samples as real-world observations.
