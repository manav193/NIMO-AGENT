from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class AuditLogger:
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, action: str, actor: str, resource: str, details: dict[str, Any] | None = None) -> None:
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "actor": actor,
            "resource": resource,
            "details": details or {},
        })
