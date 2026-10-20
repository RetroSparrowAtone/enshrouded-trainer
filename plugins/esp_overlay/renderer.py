"""Thin wrapper around the DX11 overlay window (see overlay-core)."""
from __future__ import annotations


class BoxRenderer:
    def __init__(self) -> None:
        self._attached = False
        self._visible = False

    def attach(self) -> None:
        self._attached = True

    def detach(self) -> None:
        self._attached = False

    def set_visible(self, visible: bool) -> None:
        self._visible = visible

    def draw_entity_box(self, world_ptr: int) -> None:
        if not (self._attached and self._visible):
            return
        # screen-space projection handled by overlay-core
        pass