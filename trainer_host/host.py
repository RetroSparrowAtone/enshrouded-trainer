"""Core host: owns process handle, hotkey loop, plugin lifecycle."""
from __future__ import annotations

import threading
import time
from typing import Optional

from trainer_host.process import EnshroudedProcess
from trainer_host.registry import PluginRegistry
from trainer_host.hotkeys import HotkeyBus
from contracts.plugin import PluginBase


class TrainerHost:
    def __init__(self, registry: PluginRegistry, process: Optional[EnshroudedProcess]):
        self.registry = registry
        self.process = process
        self.hotkeys = HotkeyBus()
        self._stop = threading.Event()
        self._plugins: list[PluginBase] = []

    def run(self) -> None:
        ctx = self.registry.build_context(process=self.process, hotkeys=self.hotkeys)
        for plugin_cls in self.registry.all():
            plugin = plugin_cls()
            plugin.on_load(ctx)
            self._plugins.append(plugin)

        self.hotkeys.start()
        while not self._stop.is_set():
            if self.process and not self.process.alive():
                self.process = EnshroudedProcess.attach("enshrouded.exe")
                ctx.process = self.process
            for p in self._plugins:
                p.on_tick(ctx)
            time.sleep(0.05)

    def shutdown(self) -> None:
        self._stop.set()
        for p in self._plugins:
            try:
                p.on_unload()
            except Exception:
                pass
        self.hotkeys.stop()