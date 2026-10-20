"""Discovers plugin packages and imports them by convention."""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path

from trainer_host.registry import PluginRegistry
from contracts.plugin import PluginBase


class PluginLoader:
    def __init__(self, plugins_dir: Path, registry: PluginRegistry):
        self.plugins_dir = plugins_dir
        self.registry = registry

    def discover_and_load(self) -> list[str]:
        loaded: list[str] = []
        for mod in pkgutil.iter_modules([str(self.plugins_dir)]):
            if not mod.ispkg:
                continue
            try:
                module = importlib.import_module(f"plugins.{mod.name}")
            except Exception as exc:
                print(f"[loader] skip {mod.name}: {exc}")
                continue
            for attr in vars(module).values():
                if (
                    isinstance(attr, type)
                    and issubclass(attr, PluginBase)
                    and attr is not PluginBase
                ):
                    self.registry.register(attr)
                    loaded.append(attr.NAME)
        return loaded