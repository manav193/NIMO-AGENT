"""Bounded recovery policy for tool failures."""
from dataclasses import dataclass
@dataclass(frozen=True)
class RecoveryDecision:
    retry:bool
    max_attempts:int
    reason:str
class RecoveryPolicy:
    def __init__(self,max_attempts:int=2): self.max_attempts=max(0,min(max_attempts,3))
    def decide(self,error:str,attempt:int)->RecoveryDecision:
        if attempt>=self.max_attempts: return RecoveryDecision(False,self.max_attempts,"retry budget exhausted")
        return RecoveryDecision(True,self.max_attempts,f"bounded retry after: {error}")
