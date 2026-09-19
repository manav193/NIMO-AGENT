from dataclasses import dataclass
from typing import Any

from agent.state import AgentState
from security.audit import AuditLogger
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

    def handle_text(self, text: str, state: AgentState) -> AgentResult:
        state.messages.append({"role": "user", "content": text})
        self.audit.record(
            action="agent.input",
            actor="user",
            resource="session",
            details={"session_id": state.session_id},
        )
        return AgentResult(message="NIMO-Agent foundation ready.", data={"input": text})
