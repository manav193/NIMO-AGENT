"""Rollback proposal boundary; execution remains approval-gated."""
class RollbackWorkflow:
    def __init__(self,git,approval): self.git=git; self.approval=approval
    def propose(self,branch,target):
        return {"branch":branch,"target":target,"requires_approval":True}
    def execute(self,proposal):
        if not self.approval.approve(proposal["branch"]): raise PermissionError("Rollback approval required.")
        return self.git.reset(proposal["target"])
