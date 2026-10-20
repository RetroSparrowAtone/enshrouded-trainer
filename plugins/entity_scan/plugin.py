"""Shared entity scanner used by aimbot and esp plugins."""
from __future__ import annotations

import struct
from dataclasses import dataclass

from contracts.plugin import PluginBase, PluginContext


@dataclass
class Entity:
    ptr: int
    kind: str
    x: float
    y: float
    z: float
    hp: int


class EntityScanPlugin(PluginBase):
    NAME = "entity_scan"
    VERSION = "1.1.0"
    REQUIRES_OFFSETS = ["entity_list"]

    def __init__(self) -> None:
        self.entities: list[Entity] = []

    def on_tick(self, ctx: PluginContext) -> None:
        if ctx.process is None:
            return
        head = 0x1C00E100
        raw = ctx.process.read(head + 0x0C, 4)
        if not raw:
            return
        count = min(struct.unpack("<I", raw)[0], 256)
        scanned: list[Entity] = []
        for i in range(count):
            ptr = head + 0x1F0 * i
            blob = ctx.process.read(ptr, 0x40)
            if not blob or len(blob) < 0x20:
                continue
            x, y, z, hp = struct.unpack_from("<fffI", blob, 0x10)
            scanned.append(Entity(ptr=ptr, kind="npc", x=x, y=y, z=z, hp=hp))
        self.entities = scanned