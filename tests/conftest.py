"""Shared test setup: put the repo modules on sys.path.

The insertion order mirrors how gui/dashboard.py sets up imports, so
`import datamodel` resolves to misc/datamodel.py exactly as it does when
the dashboard replays strategies.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

for _p in (
    REPO_ROOT,
    REPO_ROOT / "misc",
    REPO_ROOT / "ROUND3",
    REPO_ROOT / "trading_algos" / "TUTORIAL",
):
    _s = str(_p)
    if _s not in sys.path:
        sys.path.insert(0, _s)
