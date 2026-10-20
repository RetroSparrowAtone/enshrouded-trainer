"""ESP overlay: draws entity boxes and labels via the overlay renderer."""
from __future__ import annotations

from contracts.plugin import PluginBase, PluginContext
from plugins.esp_overlay.renderer import BoxRenderer


class EspOverlayPlugin(PluginBase):
    NAME = "esp_overlay"
    VERSION = "1.2.0"
    REQUIRES_OFFSETS = ["entity_list", "player"]

    def __init__(self) -> None:
        self.renderer = BoxRenderer()
        self.enabled = False
        self._last_toggle = 0.0

    def on_load(self, ctx: PluginContext) -> None:
        ctx.hotkeys.bind("f1", self._toggle)
        self.renderer.attach()

    def _toggle(self) -> None:
        self.enabled = not self.enabled
        self.renderer.set_visible(self.enabled)

    def on_tick(self, ctx: PluginContext) -> None:
        if not self.enabled or ctx.process is None:
            return
        head = 0x1C00E100
        count_raw = ctx.process.read(head + 0x0C, 4)
        if not count_raw:
            return
        import struct
        count = struct.unpack("<I", count_raw)[0]
        if count > 512:
            return
        for i in range(min(count, 128)):
            self.renderer.draw_entity_box(head + 0x1F0 * i)

    def on_unload(self) -> None:
        self.renderer.detach()