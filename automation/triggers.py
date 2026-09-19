"""Allowlisted trigger types."""
from dataclasses import dataclass
@dataclass(frozen=True)
class Trigger:
    kind:str
    value:str
class TriggerRegistry:
    ALLOWED={"schedule","event","manual","webhook"}
    def validate(self,t):
        if t.kind not in self.ALLOWED: raise ValueError("Unsupported trigger type.")
        if len(t.value)>500: raise ValueError("Trigger value too long.")
