"""Safe Git workspace inspection/edit staging boundary."""
import difflib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WorkspacePolicy:
    root:Path
    max_file_bytes:int=500_000
    def resolve(self,path:str)->Path:
        root=self.root.resolve(); p=(root/path).resolve()
        if p!=root and root not in p.parents: raise PermissionError("Path escapes workspace.")
        return p
class Workspace:
    def __init__(self,policy:WorkspacePolicy): self.policy=policy
    def read(self,path):
        p=self.policy.resolve(path)
        if p.stat().st_size>self.policy.max_file_bytes: raise ValueError("File exceeds workspace limit.")
        return p.read_text(encoding="utf-8")
    def diff(self,before:str,after:str,path:str)->str:
        return "".join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile=path,tofile=path))
