from agent.runtime import AgentRuntime
from agent.state import AgentState
from security.audit import AuditLogger
from security.permissions import PermissionEngine
from tools.registry import ToolRegistry


def build_runtime() -> AgentRuntime:
    registry = ToolRegistry()
    permissions = PermissionEngine()
    audit = AuditLogger()
    return AgentRuntime(
        registry=registry,
        permissions=permissions,
        audit=audit,
    )

def main() -> None:
    runtime = build_runtime()
    state = AgentState()
    result = runtime.handle_text("NIMO-Agent foundation ready.", state)
    print(result.message)

if __name__ == "__main__":
    main()
