"""Bounded code/test/fix orchestration. No automatic commit or push."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CodingRun:
    proposals:list
    tests:list
    status:str
class CodingLoop:
    def __init__(self,edit_engine,test_runner,max_rounds=3):
        self.edits=edit_engine; self.tests=test_runner; self.max_rounds=max(1,min(max_rounds,3))
    def validate(self,workspace,proposals):
        reports=[]
        for proposal in proposals:
            self.edits.apply(workspace,proposal)
            reports.append(self.tests.run())
            if not reports[-1].passed: break
        return CodingRun(proposals,reports,"passed" if reports and reports[-1].passed else "needs_review")
