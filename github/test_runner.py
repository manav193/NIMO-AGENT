"""Bounded project validation runner using the safe terminal boundary."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TestReport:
    passed:bool
    output:str
    command:str
class CodingTestRunner:
    def __init__(self,terminal): self.terminal=terminal
    def run(self,command=("pytest","-q")):
        result=self.terminal.run({"command":list(command)},confirmed=True)
        output=result.output if isinstance(result.output,str) else str(result.output or result.error or "")
        return TestReport(result.success,output," ".join(command))
