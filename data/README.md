# Data status

M1 includes no downloaded real-world data and no real-data loader. The demo's
synthetic path/star/diamond are generated in C in src/samples.c, outside BFS.
See [DATASET_DECISION.md](../docs/DATASET_DECISION.md) for the NADINE C. elegans
candidate, source orientation and acquisition/validation plan. Keep raw files
under data/raw/ (build-independent and Git ignored). Record retrieval date,
SHA-256, source, preprocessing counts and ID map when acquisition is performed.
