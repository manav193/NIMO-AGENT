from integrations.dispatcher import PluginDispatcher
from integrations.plugin_router import PluginInvocation
from integrations.registry import PluginRegistry, PluginSpec


def test_plugin_registry_resolves_at_name():
    registry = PluginRegistry()
    registry.register(PluginSpec("gmail", "Email"))
    assert registry.resolve("@gmail").name == "gmail"

def test_dispatcher_rejects_unknown_plugin():
    result = PluginDispatcher(PluginRegistry()).dispatch(PluginInvocation("unknown", "do it"))
    assert result.success is False

def test_dispatcher_runs_registered_handler():
    registry = PluginRegistry()
    registry.register(PluginSpec("github", "GitHub", handler=lambda task: "ok:" + task))
    result = PluginDispatcher(registry).dispatch(PluginInvocation("github", "inspect PR"))
    assert result.success is True
    assert result.output == "ok:inspect PR"
