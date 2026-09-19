from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

class TriggerType(str, Enum):
    SCHEDULE = "schedule"
    EVENT = "event"

class AutomationStatus(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"
    PAUSED = "paused"

@dataclass(frozen=True)
class Automation:
    id: str
    name: str
    trigger: TriggerType
    action: str
    config: dict[str, Any] = field(default_factory=dict)
    status: AutomationStatus = AutomationStatus.ENABLED

    @property
    def enabled(self) -> bool:
        return self.status is AutomationStatus.ENABLED

@dataclass(frozen=True)
class EmailPolicy:
    auto_acknowledge: bool = True
    auto_reply: bool = False
    require_confirmation_for_send: bool = True
    allowed_recipients: tuple[str, ...] = ()

@dataclass(frozen=True)
class ScheduledJob:
    automation_id: str
    run_at: datetime
    job_id: str | None = None

@dataclass(frozen=True)
class AutomationRun:
    automation_id: str
    started_at: datetime
    finished_at: datetime | None = None
    success: bool = False
    error: str | None = None
