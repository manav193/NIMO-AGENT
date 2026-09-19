from dataclasses import dataclass
from typing import Any
from agent.state import AgentState
from security.audit import AuditLogger
from agent.executor import Executor
from agent.observer import Observer
from agent.planner import Planner
from agent.verifier import Verifier
from security.permissions import PermissionEngine
from tools.registry import ToolRegistry

@dataclass
class AgentResult:
    message: str
    status: str = "ok"
    data: dict[str, Any] | None = None

class AgentRuntime:
    """Plan -> act -> observe -> verify runtime shell with a mandatory permission gate."""
    def __init__(self, registry: ToolRegistry, permissions: PermissionEngine, audit: AuditLogger) -> None:
        self.registry = registry
        self.permissions = permissions
        self.audit = audit
        self.planner = Planner()
        self.executor = Executor(registry, permissions, audit)
        self.observer = Observer()
        self.verifier = Verifier()

    def execute_tool(self, request):
        result = self.executor.execute(request)
        observation = self.observer.observe(result)
        verification = self.verifier.verify(result)
        self.audit.record("agent.verify", "agent", request.tool_name, {"success": verification.success})
        return result, observation, verification

    def handle_text(self, text: str, state: AgentState) -> AgentResult:
        state.messages.append({"role": "user", "content": text})
        self.audit.record("agent.input", "user", "session", {"session_id": state.session_id})
        plan = self.planner.create_plan(text)
        self.audit.record("agent.plan", "agent", "session", {"steps": len(plan)})
        verification = {"success": True, "reason": "No tool execution required."}
        self.audit.record("agent.verify", "agent", "session", verification)
        return AgentResult(
            message="Plan created.",
            data={"input": text, "steps": [step.action for step in plan], "verification": verification},
        )
