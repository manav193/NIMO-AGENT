from tools.contracts import ToolRequest, ToolResult
from tools.registry import ToolRegistry
from security.audit import AuditLogger
from security.permissions import PermissionEngine

class Executor:
    """Executes tools only after the central permission gate approves them."""
    def __init__(self, registry: ToolRegistry, permissions: PermissionEngine, audit: AuditLogger):
        self.registry = registry
        self.permissions = permissions
        self.audit = audit

    def execute(self, request: ToolRequest) -> ToolResult:
        spec = self.registry.get(request.tool_name)
        decision = self.permissions.evaluate(spec)
        self.audit.record("tool.permission", "agent", request.tool_name, {
            "allowed": decision.allowed,
            "requires_confirmation": decision.requires_confirmation,
        })
        if not decision.allowed:
            return ToolResult(False, error=decision.reason)
        if decision.requires_confirmation:
            return ToolResult(False, error="User confirmation required before execution.")
        result = spec.handler(request.arguments)
        self.audit.record("tool.execute", "agent", request.tool_name, {"success": result.success})
        return result
