from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

class TriggerType(str, Enum):
    SCHEDULE = "schedule"
    EVENT = "event"

@dataclass(frozen=True)
class Automation:
    id: str
    name: str
    trigger: TriggerType
    action: str
    config: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True

@dataclass(frozen=True)
class EmailPolicy:
    auto_acknowledge: bool = True
    auto_reply: bool = False
    require_confirmation_for_send: bool = True

@dataclass(frozen=True)
class ScheduledJob:
    automation_id: str
    run_at: datetime
