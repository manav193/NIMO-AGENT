from agent.executor import Executor
from agent.runtime import AgentRuntime
from agent.state import AgentState
from security.audit import AuditLogger
from security.permissions import PermissionEngine
from tools.contracts import RiskLevel, ToolRequest, ToolResult, ToolSpec
from tools.registry import ToolRegistry


def ok_handler(args):
    return ToolResult(success=True, output=args)


def test_tool_registry_registers_and_executes_through_executor():
    registry = ToolRegistry()
    registry.register(ToolSpec("echo", "Echo input", RiskLevel.READ, ok_handler))
    result = Executor(registry, PermissionEngine(), AuditLogger()).execute(
        ToolRequest("echo", {"value": "hello"})
    )
    assert result.success is True
    assert result.output == {"value": "hello"}


def test_restricted_tool_is_blocked():
    spec = ToolSpec("danger", "Restricted", RiskLevel.RESTRICTED, ok_handler)
    decision = PermissionEngine().evaluate(spec)
    assert decision.allowed is False


def test_confirmed_tool_requires_confirmation():
    spec = ToolSpec("push", "Push code", RiskLevel.CONFIRMED, ok_handler)
    decision = PermissionEngine().evaluate(spec)
    assert decision.allowed is True
    assert decision.requires_confirmation is True


def test_runtime_records_input_and_plan_audit():
    audit = AuditLogger()
    runtime = AgentRuntime(ToolRegistry(), PermissionEngine(), audit)
    result = runtime.handle_text("hello", AgentState(session_id="test"))
    assert result.status == "ok"
    assert [event["action"] for event in audit.events] == [
        "agent.input", "agent.plan", "agent.verify"
    ]
