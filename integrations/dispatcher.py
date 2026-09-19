from dataclasses import dataclass
from typing import Any
from integrations.plugin_router import PluginInvocation
from integrations.registry import PluginRegistry
from integrations.providers import ProviderRegistry, ProviderRequest, ProviderResult
from security.audit import AuditLogger

@dataclass(frozen=True)
class DispatchResult:
    provider: str
    task: str
    success: bool
    output: Any = None
    error: str | None = None

class PluginDispatcher:
    """Routes @commands; side effects use registered providers and are audited."""
    def __init__(self, registry: PluginRegistry, providers: ProviderRegistry | None = None,
                 audit: AuditLogger | None = None) -> None:
        self.registry = registry
        self.providers = providers or ProviderRegistry()
        self.audit = audit or AuditLogger()

    def dispatch(self, invocation: PluginInvocation) -> DispatchResult:
        try:
            plugin = self.registry.resolve(invocation.provider)
            if plugin.handler is not None:
                output = plugin.handler(invocation.task)
                self.audit.record("plugin.dispatch", "agent", invocation.provider, {"success": True})
                return DispatchResult(invocation.provider, invocation.task, True, output=output)
            provider = self.providers.resolve(invocation.provider)
            result: ProviderResult = provider.execute(
                ProviderRequest(provider=invocation.provider, operation="natural_language", payload={"task": invocation.task})
            )
            self.audit.record("provider.dispatch", "agent", invocation.provider, {"success": result.success})
            return DispatchResult(invocation.provider, invocation.task, result.success,
                                  output=result.data, error=result.error)
        except (KeyError, ValueError) as exc:
            self.audit.record("plugin.dispatch_error", "agent", invocation.provider, {"type": type(exc).__name__})
            return DispatchResult(invocation.provider, invocation.task, False, error=str(exc))
        except Exception as exc:
            self.audit.record("plugin.dispatch_error", "agent", invocation.provider, {"type": type(exc).__name__})
            return DispatchResult(invocation.provider, invocation.task, False,
                                  error=f"Provider failure: {type(exc).__name__}")
