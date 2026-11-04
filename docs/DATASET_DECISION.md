# C. elegans acquisition and validation record
Downloaded locally on 2026-11-03; revalidated during cleanup on 2026-11-04 (27,256 bytes). Raw file ignored at data/raw/ssumlinks.txt.

Sources: https://www.quantware.ups-tlse.fr/FETNADINE/datasets.htm
and https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/
Raw: https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/ssumlinks.txt
Credit V. Kandiah and D. L. Shepelyansky, Google matrix analysis of C.elegans neural network, Phys. Lett. A 378 (2014), 1932; arXiv:1311.2013. The source page asks users to cite the paper and page. Redistribution license not verified; raw remains ignored.

The page describes a 279 x 279 matrix. Actual file header: // sum of links for S matrix (synapse+gap link weights), j points to i
Actual first row: 2 1 1. Interpret columns i j weight as directed j->i, mapped to zero-based IDs. Weights describe summed synaptic and gap connection weights; BFS retains positive edges and ignores magnitude. This is unweighted hop distance, not weighted shortest paths. Preserve direction and self-loops; deduplicate repeated positive pairs in input order. Declared 279 vertices includes potential isolates; all 279 IDs actually occur in this file. No neuron-name mapping is claimed.

Local parse: 2990 data rows, 2990 unique directed edges, 279 observed IDs, zero duplicate pairs, zero nonpositive rows, zero self-loops.
SHA256: 2d553b8ac000d8bebd442369c89480308fce027cfdc98bf824780775d9b78dc5
From zero-based source 0: 275 reachable, 4 unreachable, peak queue occupancy 169. Every baseline produces identical distances, independently checked by repeated edge relaxation in tests. Array queues execute 252 resize copies and 6 growth events; shifting queue also executes 27728 shifts. These are correctness/work observations, not final experiments.

Native PowerShell acquisition from repository root:

```powershell
New-Item -ItemType Directory -Force data/raw
Invoke-WebRequest -Uri https://www.quantware.ups-tlse.fr/QWLIB/wormgooglematrix/ssumlinks.txt -OutFile data/raw/ssumlinks.txt -TimeoutSec 40
Get-FileHash data/raw/ssumlinks.txt -Algorithm SHA256
python -m t10_python.demo --dataset data/raw/ssumlinks.txt
```

Sandbox network initially failed; approved network retry succeeded. The raw browser fetch also failed; the dataset page was accessible. A future download must be parsed and hashed again; do not silently assume these counts for changed contents. Normal demo and synthetic tests do not require network or raw data.
