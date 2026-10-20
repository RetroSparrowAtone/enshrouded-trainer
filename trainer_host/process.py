"""Minimal wrapper around pymem for the Enshrouded process."""
from __future__ import annotations

from typing import Optional

try:
    import pymem
    import pymem.process
except ImportError:
    pymem = None


class EnshroudedProcess:
    def __init__(self, handle, base_module) -> None:
        self.handle = handle
        self.base = base_module.lpBaseOfDll
        self.module = base_module

    @classmethod
    def attach(cls, exe: str) -> Optional["EnshroudedProcess"]:
        if pymem is None:
            return None
        try:
            pm = pymem.Pymem(exe)
            module = pymem.process.module_from_name(pm.process_handle, exe)
            return cls(pm, module)
        except Exception:
            return None

    def alive(self) -> bool:
        try:
            return self.handle.process_handle is not None
        except Exception:
            return False

    def read(self, offset: int, size: int) -> Optional[bytes]:
        try:
            return self.handle.read_bytes(self.base + offset, size)
        except Exception:
            return None

    def write(self, offset: int, data: bytes) -> bool:
        try:
            self.handle.write_bytes(self.base + offset, data, len(data))
            return True
        except Exception:
            return False