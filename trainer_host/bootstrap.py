"""Entry point: build the host, load plugins, run the hotkey loop."""
from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console

from trainer_host.host import TrainerHost
from trainer_host.loader import PluginLoader
from trainer_host.registry import PluginRegistry
from trainer_host.process import EnshroudedProcess

console = Console()


def main() -> int:
    console.rule("[bold cyan]enshrouded-trainer 2.4.1")
    proc = EnshroudedProcess.attach("enshrouded.exe")
    if proc is None:
        console.print("[yellow]Enshrouded not running — waiting for attach...")

    registry = PluginRegistry()
    loader = PluginLoader(Path("plugins"), registry)
    loaded = loader.discover_and_load()
    console.print(f"[green]loaded {len(loaded)} plugins[/]")

    host = TrainerHost(registry=registry, process=proc)
    try:
        host.run()
    except KeyboardInterrupt:
        console.print("[red]shutdown requested")
    finally:
        host.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())