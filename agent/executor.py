from tools.contracts import ToolRequest, ToolResult
from tools.registry import ToolRegistry
from security.audit import AuditLogger
from security.permissions import PermissionEngine
from security.suspicious import SuspiciousActivityDetector
from security.secrets import redact
from security.rate_limit import RateLimiter
from security.kill_switch import KillSwitch

class Executor:
    """Single execution choke point: lookup -> policy -> handler -> audit."""
    def __init__(self, registry: ToolRegistry, permissions: PermissionEngine, audit: AuditLogger):
        self.registry = registry
        self.permissions = permissions
        self.audit = audit
        self.detector = SuspiciousActivityDetector()
        self.rate_limiter = RateLimiter()
        self.kill_switch = KillSwitch()

    def execute(self, request: ToolRequest) -> ToolResult:
        self.kill_switch.check()
        if not self.rate_limiter.allow(request.requested_by):
            return ToolResult(False, error="Rate limit exceeded.")
        findings = self.detector.inspect(request.tool_name, request.arguments)
        if any(f.severity == "critical" for f in findings):
            self.audit.record("security.block", request.requested_by, request.tool_name, {"findings":[f.rule for f in findings]})
            return ToolResult(False, error="Security policy blocked this action.")
        spec = self.registry.get(request.tool_name)
        decision = self.permissions.evaluate(spec)
        self.audit.record("tool.permission", request.requested_by, request.tool_name, {
            "allowed": decision.allowed,
            "requires_confirmation": decision.requires_confirmation,
        })
        if not decision.allowed:
            return ToolResult(False, error=decision.reason)
        if decision.requires_confirmation:
            return ToolResult(False, error="User confirmation required before execution.")
        try:
            result = spec.handler(request.arguments)
        except Exception as exc:
            self.audit.record("tool.error", request.requested_by, request.tool_name, {"type": type(exc).__name__})
            return ToolResult(False, error=f"Tool execution failed: {type(exc).__name__}")
        self.audit.record("tool.execute", request.requested_by, request.tool_name, {"success": result.success})
        return result
