"""Computer-use safety policy. Physical input is opt-in and confirmation-gated."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class ComputerPolicy:
    enabled: bool = False
    allowed_apps: set[str] = field(default_factory=set)
    max_x: int = 10000
    max_y: int = 10000
    emergency_stop: bool = False

    def check_enabled(self) -> None:
        if self.emergency_stop: raise PermissionError("Computer actions are stopped by emergency stop.")
        if not self.enabled: raise PermissionError("Computer control is disabled.")

    def check_point(self,x:int,y:int)->None:
        self.check_enabled()
        if x < 0 or y < 0 or x > self.max_x or y > self.max_y:
            raise ValueError("Screen coordinate is outside the configured boundary.")

    def check_app(self,app:str)->None:
        self.check_enabled()
        if not app or app not in self.allowed_apps:
            raise PermissionError("Application is not allowlisted.")
