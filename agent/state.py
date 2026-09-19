from dataclasses import dataclass, field
from typing import Any

@dataclass
class AgentState:
    session_id: str = "local"
    messages: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
