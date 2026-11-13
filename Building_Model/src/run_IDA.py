# ==================================================================
# Run IDA for all ground motions and PGA levels
# ==================================================================
# Run:  python run_ida.py        (keep this file in the same folder as IDA.py)

import subprocess
import sys
from pathlib import Path

here = Path(__file__).resolve().parent

rsns = [334, 2476, 2510, 3282, 4199, 5259, 5676]
direction = 2                                                       # 1 = X, 2 = Y
pgas = [
    0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 
    0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 
    1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 
    1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2.0
]

for rsn in rsns:
    for pga in pgas:
        print(f"\n===== RSN {rsn} | PGA {pga} g =====")
        result = subprocess.run(
            [sys.executable, str(here / "IDA.py"), str(rsn), str(direction), str(pga)],
            cwd=here
        )
        if result.returncode == 2:           # collapsed: go to the next ground motion
            print(f"RSN {rsn} collapsed at {pga} g.")
            break
        if result.returncode != 0:           # a real error: stop and show it
            raise SystemExit(f"Run failed for RSN {rsn}, PGA {pga} g.")