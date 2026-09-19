from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Observation:
    kind: str
    data: dict[str, Any]

class Observer:
    def observe(self, result: Any) -> Observation:
        return Observation(kind="tool_result", data={"result": result})
