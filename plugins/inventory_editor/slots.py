"""Inventory slot table helper."""
from __future__ import annotations


class SlotTable:
    def __init__(self, base: int, slot_size: int, count: int) -> None:
        self.base = base
        self.slot_size = slot_size
        self.count = count

    def slot_addr(self, idx: int) -> int:
        if not 0 <= idx < self.count:
            raise IndexError(idx)
        return self.base + idx * self.slot_size

    def find_empty(self, process) -> int | None:
        for i in range(self.count):
            addr = self.slot_addr(i)
            raw = process.read(addr, 4)
            if raw == b"\x00\x00\x00\x00":
                return addr
        return None

    def dump_to_log(self) -> None:
        print(f"[inventory] {self.count} slots @ 0x{self.base:X}")