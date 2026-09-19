"""Explicit, reviewable code edit proposals."""
from dataclasses import dataclass


@dataclass(frozen=True)
class EditProposal:
    path:str
    before:str
    after:str
    diff:str
    requires_confirmation:bool=True
class EditEngine:
    def propose(self,workspace,path,after):
        before=workspace.read(path)
        diff=workspace.diff(before,after,path)
        if not diff: raise ValueError("Edit produces no change.")
        return EditProposal(path,before,after,diff,True)
    def apply(self,workspace,proposal):
        if proposal.before!=workspace.read(proposal.path): raise RuntimeError("Workspace changed; refresh proposal.")
        p=workspace.policy.resolve(proposal.path); p.write_text(proposal.after,encoding="utf-8")
