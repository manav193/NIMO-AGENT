"""Durable, bounded workflow execution built on the existing automation primitives."""
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True)
class WorkflowStep:
    id: str
    action: str
    arguments: dict[str, Any] = field(default_factory=dict)
    requires_confirmation: bool = False

@dataclass(frozen=True)
class Workflow:
    id: str
    steps: list[WorkflowStep]
    max_steps: int = 20

class WorkflowEngine:
    def __init__(self, executor, approval=None):
        self.executor = executor
        self.approval = approval

    def validate(self, workflow):
        if not workflow.steps or len(workflow.steps) > min(workflow.max_steps, 50):
            raise ValueError("Invalid workflow size.")
        ids = set()
        for step in workflow.steps:
            if not step.id or step.id in ids:
                raise ValueError("Duplicate workflow step.")
            ids.add(step.id)

    def run(self, workflow):
        self.validate(workflow)
        results = []
        for step in workflow.steps:
            if step.requires_confirmation and self.approval is not None and not self.approval.approve(step.id):
                return results
            results.append(self.executor(step.action, step.arguments))
        return results
