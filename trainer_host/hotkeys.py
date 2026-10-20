"""Central hotkey bus so plugins don't fight over keyboard hooks."""
from __future__ import annotations

import threading
from typing import Callable

try:
    import keyboard
except ImportError:
    keyboard = None


class HotkeyBus:
    def __init__(self) -> None:
        self._bindings: dict[str, Callable[[], None]] = {}
        self._thread: threading.Thread | None = None
        self._running = False

    def bind(self, combo: str, fn: Callable[[], None]) -> None:
        if combo in self._bindings:
            raise ValueError(f"hotkey {combo} already bound")
        self._bindings[combo] = fn

    def start(self) -> None:
        if keyboard is None:
            return
        self._running = True
        for combo in self._bindings:
            keyboard.add_hotkey(combo, self._bindings[combo])

    def stop(self) -> None:
        self._running = False
        if keyboard is not None:
            try:
                keyboard.unhook_all_hotkeys()
            except Exception:
                pass