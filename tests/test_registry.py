from trainer_host.registry import PluginRegistry
from contracts.plugin import PluginBase


class DummyPlugin(PluginBase):
    NAME = "dummy"
    VERSION = "0.0.1"


def test_register_and_lookup():
    reg = PluginRegistry()
    reg.register(DummyPlugin)
    assert reg.get("dummy") is DummyPlugin
    assert reg.get("missing") is None


def test_context_built_with_defaults():
    reg = PluginRegistry()
    ctx = reg.build_context(process=None, hotkeys=None)
    assert ctx.config == {}
    assert ctx.process is None
```