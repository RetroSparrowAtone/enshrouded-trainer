"""Shared plugin contract — the only thing host and plugins agree on."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar, Optional


@dataclass
class PluginContext:
    process: Any
    hotkeys: Any
    config: dict = field(default_factory=dict)

    def read_f32(self, offset: int) -> Optional[float]:
        if self.process is None:
            return None
        raw = self.process.read(offset, 4)
        if raw is None:
            return None
        import struct
        return struct.unpack("<f", raw)[0]


class PluginBase:
    NAME: ClassVar[str] = "unnamed"
    VERSION: ClassVar[str] = "0.0.0"
    REQUIRES_OFFSETS: ClassVar[list[str]] = []

    def on_load(self, ctx: PluginContext) -> None: ...
    def on_tick(self, ctx: PluginContext) -> None: ...
    def on_unload(self) -> None: ...