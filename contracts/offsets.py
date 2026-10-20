"""Loader for versioned offset tables."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_offsets(build: str, root: Path | None = None) -> dict[str, Any]:
    root = root or Path("offsets")
    path = root / f"en_shrouded_{build}.json"
    if not path.exists():
        raise FileNotFoundError(f"no offsets for build {build} ({path})")
    return json.loads(path.read_text(encoding="utf-8"))