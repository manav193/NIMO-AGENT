from agent.executor import Executor
from agent.observer import Observer
from agent.planner import Planner
from agent.verifier import Verifier
from tools.contracts import RiskLevel, ToolRequest, ToolResult, ToolSpec
from tools.registry import ToolRegistry
from security.audit import AuditLogger
from security.permissions import PermissionEngine

def echo(args):
    return ToolResult(success=True, output=args)

def test_plan_observe_verify_flow():
    plan = Planner().create_plan("echo hello")
    assert plan[0].action == "respond"
    registry = ToolRegistry()
    registry.register(ToolSpec("echo", "Echo", RiskLevel.READ, echo))
    result = Executor(registry, PermissionEngine(), AuditLogger()).execute(ToolRequest("echo", {"value": "hello"}))
    observation = Observer().observe(result)
    verification = Verifier().verify(result)
    assert observation.kind == "tool_result"
    assert observation.data["result"].output == {"value": "hello"}
    assert verification.success is True
