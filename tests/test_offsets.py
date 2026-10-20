from pathlib import Path
from contracts.offsets import load_offsets


def test_offsets_load_for_known_build():
    data = load_offsets("2026", root=Path("offsets"))
    assert data["build"] == "0.7.2.1"
    assert "player" in data
    assert data["inventory"]["slot_size"] == 64


def test_offsets_missing_build_raises():
    import pytest
    with pytest.raises(FileNotFoundError):
        load_offsets("nope-9999", root=Path("offsets"))