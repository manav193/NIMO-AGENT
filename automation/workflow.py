"""Durable, bounded workflow execution built on the existing automation primitives."""
from dataclasses import dataclass,field
from typing import Any,Callable
@dataclass(frozen=True)
class WorkflowStep:
    id:str
    action:str
    arguments:dict[str,Any]=field(default_factory=dict)
    requires_confirmation:bool=False
@dataclass(frozen=True)
class Workflow:
    id:str
    steps:list[WorkflowStep]
    max_steps:int=20
class WorkflowEngine:
    def __init__(self,executor,approval=None): self.executor=executor; self.approval=approval
    def validate(self,w):
        if not w.steps or len(w.steps)>min(w.max_steps,50): raise ValueError("Invalid workflow size.")
        ids=set()
        for s in w.steps:
            if not s.id or s.id in ids: raise ValueError("Duplicate workflow step.")
            ids.add(s.id)
    def run(self,w):
        self.validate(w); results=[]
        for step in w.steps:
            if step.requires_confirmation and self.approval is not None:
                if not self.approval.approve(step.id): return results
            results.append(self.executor(step.action,step.arguments))
        return results
