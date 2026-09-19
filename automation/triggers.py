"""Allowlisted trigger types."""
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Trigger:
    kind: str
    value: str

class TriggerRegistry:
    ALLOWED: ClassVar[set[str]] = {"schedule", "event", "manual", "webhook"}

    def validate(self, trigger):
        if trigger.kind not in self.ALLOWED:
            raise ValueError("Unsupported trigger type.")
        if len(trigger.value) > 500:
            raise ValueError("Trigger value too long.")
