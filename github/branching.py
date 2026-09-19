"""Explicit Git branch workflow; no implicit merge/push."""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class BranchPolicy:
    protected: tuple[str, ...] = ("main", "master")

    def validate(self, name):
        if not re.fullmatch(r"[A-Za-z0-9._/-]{1,80}", name):
            raise ValueError("Invalid branch name.")
        if name in self.protected:
            raise PermissionError("Protected branch cannot be directly modified.")

class BranchWorkflow:
    def __init__(self, git, policy=None):
        self.git = git
        self.policy = policy or BranchPolicy()

    def create(self, name):
        self.policy.validate(name)
        return self.git.create_branch(name)
