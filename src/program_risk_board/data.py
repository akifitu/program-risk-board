"""Load risk board input data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


RiskRecord = Dict[str, Any]


def load_risks(data_file: Path | str) -> List[RiskRecord]:
    """Load risk data from JSON."""
    return json.loads(Path(data_file).read_text(encoding="utf-8"))
