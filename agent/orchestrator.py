"""End-to-end model -> permission -> tool -> observe -> verify loop."""
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class OrchestrationResult:
    reply: str
    executed: list[dict[str, Any]]
    blocked: list[dict[str, Any]]

class AgentOrchestrator:
    def __init__(self, brain, runtime):
        self.brain = brain
        self.runtime = runtime

    def handle(self, message, state) -> OrchestrationResult:
        brain = self.brain.ask(message)
        executed = []
        blocked = []
        for intent in brain.intents:
            try:
                request = type(
                    "Request",
                    (),
                    {
                        "tool_name": intent.tool_name,
                        "arguments": intent.arguments,
                        "requested_by": "model",
                    },
                )()
                result, _, verification = self.runtime.execute_tool(request)
                item = {
                    "tool": intent.tool_name,
                    "success": result.success,
                    "verified": verification.success,
                }
                (executed if result.success and verification.success else blocked).append(item)
            except Exception as exc:  # noqa: BLE001 - isolate one model intent
                blocked.append({"tool": intent.tool_name, "success": False, "error": str(exc)})
        return OrchestrationResult(brain.text, executed, blocked)
