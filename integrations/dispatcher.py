from dataclasses import dataclass
from typing import Any
from integrations.plugin_router import PluginInvocation
from integrations.registry import PluginRegistry

@dataclass(frozen=True)
class DispatchResult:
    provider: str
    task: str
    success: bool
    output: Any = None
    error: str | None = None

class PluginDispatcher:
    """Resolves @plugins; external side effects remain subject to Agent policy."""
    def __init__(self, registry: PluginRegistry) -> None:
        self.registry = registry

    def dispatch(self, invocation: PluginInvocation) -> DispatchResult:
        try:
            plugin = self.registry.resolve(invocation.provider)
            if plugin.handler is None:
                return DispatchResult(invocation.provider, invocation.task, False, error="Plugin has no handler.")
            return DispatchResult(invocation.provider, invocation.task, True, output=plugin.handler(invocation.task))
        except (KeyError, ValueError) as exc:
            return DispatchResult(invocation.provider, invocation.task, False, error=str(exc))
