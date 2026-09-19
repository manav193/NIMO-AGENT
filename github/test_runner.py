"""Bounded project validation runner using the existing safe terminal boundary."""
from dataclasses import dataclass
@dataclass(frozen=True)
class TestReport:
    passed:bool
    output:str
    command:str
class CodingTestRunner:
    def __init__(self,terminal): self.terminal=terminal
    def run(self,command=("pytest","-q")):
        result=self.terminal.run(list(command),confirmed=True)
        return TestReport(result.success,result.output," ".join(command))
