"""Guarded GitHub coding workflow boundary."""
from __future__ import annotations

from dataclasses import dataclass

from tools.git import GitWorkspace


@dataclass(frozen=True)
class ChangeProposal:
    summary:str
    files:list[str]
    checks:list[str]
    requires_confirmation:bool=True

class CodingAgent:
    def __init__(self,workspace:GitWorkspace):
        self.workspace=workspace

    def inspect(self)->dict:
        return {"status":self.workspace.status().output,
                "branch":self.workspace.branch().output,
                "recent":self.workspace.log().output,
                "diff":self.workspace.diff().output}

    def propose(self,summary:str,files:list[str],checks:list[str])->ChangeProposal:
        if not summary.strip(): raise ValueError("Proposal summary is required.")
        if len(files)>100 or len(checks)>50: raise ValueError("Proposal is too large.")
        return ChangeProposal(summary,files,checks,True)
