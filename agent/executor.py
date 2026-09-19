from security.audit import AuditLogger
from security.kill_switch import KillSwitch
from security.permissions import PermissionEngine
from security.rate_limit import RateLimiter
from security.suspicious import SuspiciousActivityDetector
from tools.contracts import ToolRequest, ToolResult
from tools.registry import ToolRegistry


class Executor:
    """Single execution choke point: lookup -> policy -> handler -> audit."""
    def __init__(self, registry: ToolRegistry, permissions: PermissionEngine, audit: AuditLogger, nexus=None):
        self.registry = registry
        self.permissions = permissions
        self.audit = audit
        self.detector = SuspiciousActivityDetector()
        self.rate_limiter = RateLimiter()
        self.kill_switch = KillSwitch()
        self.nexus = nexus

    def execute(self, request: ToolRequest) -> ToolResult:
        self.kill_switch.check()
        if not self.rate_limiter.allow(request.requested_by):
            return ToolResult(False, error="Rate limit exceeded.")
        findings = self.detector.inspect(request.tool_name, request.arguments)
        if any(f.severity == "critical" for f in findings):
            self.audit.record("security.block", request.requested_by, request.tool_name, {"findings":[f.rule for f in findings]})
            return ToolResult(False, error="Security policy blocked this action.")
        spec = self.registry.get(request.tool_name)
        if self.nexus is not None:
            decision = self.nexus.authorize({
                "tool": request.tool_name,
                "arguments": request.arguments,
                "requested_by": request.requested_by,
                "risk": spec.risk.value,
            })
            self.audit.record("nexus.decision", request.requested_by, request.tool_name, {
                "allowed": decision.allowed,
                "requires_approval": decision.requires_approval,
                "risk": decision.risk,
                "fingerprint": decision.fingerprint,
            })
            if not decision.allowed:
                return ToolResult(False, error=decision.reason or "NEXUS blocked this action.")
            if decision.requires_approval:
                return ToolResult(False, error="NEXUS approval required before execution.")
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
        except Exception as exc:  # noqa: BLE001 - isolate untrusted tool handlers
            self.audit.record("tool.error", request.requested_by, request.tool_name, {"type": type(exc).__name__})
            return ToolResult(False, error=f"Tool execution failed: {type(exc).__name__}")
        self.audit.record("tool.execute", request.requested_by, request.tool_name, {"success": result.success})
        return result
