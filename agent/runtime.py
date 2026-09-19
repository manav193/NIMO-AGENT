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
    """Small deterministic shell for the future plan→act→observe→verify loop."""

    def __init__(
        self,
        registry: ToolRegistry,
        permissions: PermissionEngine,
        audit: AuditLogger,
    ) -> None:
        self.registry = registry
        self.permissions = permissions
        self.audit = audit
        self.planner = Planner()
        self.executor = Executor(registry)
        self.observer = Observer()
        self.verifier = Verifier()

    def handle_text(self, text: str, state: AgentState) -> AgentResult:
        state.messages.append({"role": "user", "content": text})
        self.audit.record(
            action="agent.input",
            actor="user",
            resource="session",
            details={"session_id": state.session_id},
        )
        plan = self.planner.create_plan(text)
        self.audit.record(action="agent.plan", actor="agent", resource="session", details={"steps": len(plan)})
        verification = {"success": True, "reason": "No tool execution required."}
        self.audit.record(action="agent.verify", actor="agent", resource="session", details=verification)
        return AgentResult(message="Plan created.", data={"input": text, "steps": [step.action for step in plan], "verification": verification})
