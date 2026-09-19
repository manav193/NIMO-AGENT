from agent.executor import Executor
from security.audit import AuditLogger
from security.permissions import PermissionEngine
from tools.contracts import RiskLevel, ToolRequest, ToolResult, ToolSpec
from tools.registry import ToolRegistry


def test_registry_has_no_direct_execute_escape():
    registry=ToolRegistry()
    registry.register(ToolSpec("x","x",RiskLevel.READ,lambda _: ToolResult(True)))
    assert not hasattr(registry, "execute")
    executor=Executor(registry, PermissionEngine(), AuditLogger())
    assert executor.execute(ToolRequest("x")).success is True
