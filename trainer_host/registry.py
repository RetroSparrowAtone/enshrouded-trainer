"""Plugin registry and per-run context factory."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from contracts.plugin import PluginBase
from trainer_host.process import EnshroudedProcess
from trainer_host.hotkeys import HotkeyBus


@dataclass
class HostContext:
    process: Optional[EnshroudedProcess]
    hotkeys: HotkeyBus
    config: dict


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, type[PluginBase]] = {}

    def register(self, cls: type[PluginBase]) -> None:
        self._plugins[cls.NAME] = cls

    def all(self) -> list[type[PluginBase]]:
        return list(self._plugins.values())

    def get(self, name: str) -> Optional[type[PluginBase]]:
        return self._plugins.get(name)

    def build_context(self, process: Optional[EnshroudedProcess], hotkeys: HotkeyBus) -> HostContext:
        return HostContext(process=process, hotkeys=hotkeys, config={})