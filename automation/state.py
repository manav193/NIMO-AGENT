"""Explicit workflow lifecycle state."""
from enum import Enum
class WorkflowStatus(str,Enum):
    PENDING="pending"; RUNNING="running"; WAITING="waiting"; FAILED="failed"; COMPLETED="completed"; CANCELLED="cancelled"
