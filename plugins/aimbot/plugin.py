"""Silent aim / aimbot plugin with configurable FOV and smoothing."""
from __future__ import annotations

import math
from dataclasses import dataclass

from contracts.plugin import PluginBase, PluginContext


@dataclass
class AimConfig:
    fov_degrees: float = 8.0
    smoothing: float = 0.35
    enabled: bool = False


class AimbotPlugin(PluginBase):
    NAME = "aimbot"
    VERSION = "1.0.4"
    REQUIRES_OFFSETS = ["entity_list", "player"]

    def __init__(self) -> None:
        self.cfg = AimConfig()
        self.target_ptr: int | None = None

    def on_load(self, ctx: PluginContext) -> None:
        ctx.hotkeys.bind("f2", self._toggle)
        ctx.hotkeys.bind("f3", self._cycle_fov)

    def _toggle(self) -> None:
        self.cfg.enabled = not self.cfg.enabled

    def _cycle_fov(self) -> None:
        self.cfg.fov_degrees = 4.0 if self.cfg.fov_degrees >= 12.0 else self.cfg.fov_degrees + 4.0

    def on_tick(self, ctx: PluginContext) -> None:
        if not self.cfg.enabled or ctx.process is None:
            return
        best = self._pick_nearest(ctx)
        self.target_ptr = best
        if best is not None:
            self._aim_at(ctx, best)

    def _pick_nearest(self, ctx: PluginContext) -> int | None:
        return None  # entity scan delegated to entity-scan plugin

    def _aim_at(self, ctx: PluginContext, ptr: int) -> None:
        # smoothing approach: interpolate toward target angle
        _ = math.radians(self.cfg.fov_degrees) * self.cfg.smoothing
        pass