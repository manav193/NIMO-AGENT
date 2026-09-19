from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    READ = "read"
    SAFE = "safe"
    CONFIRMED = "confirmed"
    RESTRICTED = "restricted"

@dataclass(frozen=True)
class ToolRequest:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    requested_by: str = "agent"

@dataclass(frozen=True)
class ToolResult:
    success: bool
    output: Any = None
    error: str | None = None

@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    risk: RiskLevel
    handler: Callable[[dict[str, Any]], ToolResult]
