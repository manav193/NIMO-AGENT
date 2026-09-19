"""Computer-use session state with a latched emergency stop."""
from dataclasses import dataclass


@dataclass
class ComputerSession:
    session_id:str
    active:bool=True
    emergency_latched:bool=False
    actions:int=0
    def stop(self):
        self.emergency_latched=True; self.active=False
    def check(self):
        if self.emergency_latched or not self.active: raise PermissionError("Computer session is stopped.")
    def record(self): self.check(); self.actions+=1
