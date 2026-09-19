"""Approval-gated commit/push/PR workflow contract."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ReleaseProposal:
    branch:str
    commit_message:str
    files:list[str]
    tests_passed:bool
    requires_approval:bool=True
class ReleaseWorkflow:
    def __init__(self,git,github,approval): self.git=git; self.github=github; self.approval=approval
    def propose(self,branch,files,tests_passed,message):
        if not tests_passed: raise RuntimeError("Tests must pass before release proposal.")
        return ReleaseProposal(branch,message,list(files),True,True)
    def approve_and_execute(self,proposal):
        if not self.approval.approve(proposal.branch): raise PermissionError("Release approval required.")
        commit=self.git.commit(proposal.commit_message)
        self.git.push(proposal.branch)
        return self.github.create_pr(proposal.branch,proposal.commit_message)
