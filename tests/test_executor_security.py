from tools.contracts import RiskLevel, ToolRequest, ToolResult, ToolSpec
from tools.registry import ToolRegistry
from security.audit import AuditLogger
from security.permissions import PermissionEngine
from agent.executor import Executor

def test_executor_blocks_restricted_and_requires_confirmation():
    audit = AuditLogger()
    registry = ToolRegistry()
    called = {"value": False}

    def handler(args):
        called["value"] = True
        return ToolResult(True, args)

    registry.register(ToolSpec("danger", "danger", RiskLevel.RESTRICTED, handler))
    registry.register(ToolSpec("push", "push", RiskLevel.CONFIRMED, handler))
    executor = Executor(registry, PermissionEngine(), audit)

    blocked = executor.execute(ToolRequest("danger"))
    confirmed = executor.execute(ToolRequest("push"))
    assert blocked.success is False
    assert confirmed.success is False
    assert called["value"] is False
