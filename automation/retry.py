"""Bounded workflow retry/backoff policy."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RetryDecision:
    retry:bool
    delay_seconds:int
class RetryPolicy:
    def __init__(self,max_attempts=3): self.max_attempts=max(0,min(max_attempts,5))
    def decide(self,attempt):
        if attempt>=self.max_attempts: return RetryDecision(False,0)
        return RetryDecision(True,min(60,2**attempt))
