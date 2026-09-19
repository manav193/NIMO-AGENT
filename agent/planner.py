from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PlanStep:
    action: str
    tool_name: str | None = None
    arguments: dict[str, Any] | None = None

class Planner:
    """Deterministic planner boundary; model-backed planning arrives in a later phase."""

    def create_plan(self, intent: str) -> list[PlanStep]:
        return [PlanStep(action="respond", arguments={"intent": intent})]
