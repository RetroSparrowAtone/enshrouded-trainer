"""In-game inventory editor: give items, resize stacks, unlock slots."""
from __future__ import annotations

from contracts.plugin import PluginBase, PluginContext
from plugins.inventory_editor.slots import SlotTable


class InventoryEditorPlugin(PluginBase):
    NAME = "inventory_editor"
    VERSION = "0.9.2"
    REQUIRES_OFFSETS = ["inventory"]

    def __init__(self) -> None:
        self.slots = SlotTable(base=0x1B00A000, slot_size=64, count=40)

    def on_load(self, ctx: PluginContext) -> None:
        ctx.hotkeys.bind("f4", lambda: self.slots.dump_to_log())
        ctx.hotkeys.bind("f5", lambda: self._give_item(ctx, item_id=0x0064, qty=99))

    def _give_item(self, ctx: PluginContext, item_id: int, qty: int) -> None:
        if ctx.process is None:
            return
        empty = self.slots.find_empty(ctx.process)
        if empty is None:
            return
        import struct
        ctx.process.write(empty, struct.pack("<IHH", item_id, qty, 0))

    def on_tick(self, ctx: PluginContext) -> None:
        pass