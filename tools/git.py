"""Safe Git workspace operations for the coding-agent phase."""
from __future__ import annotations
import subprocess
from dataclasses import dataclass
from pathlib import Path

_ALLOWED={"status","diff","log","branch","show"}
_MAX_OUTPUT=100_000

@dataclass(frozen=True)
class GitResult:
    success:bool
    output:str
    error:str|None=None

class GitWorkspace:
    def __init__(self,root:str|Path):
        self.root=Path(root).resolve()
        if not (self.root/".git").exists():
            raise ValueError("Workspace is not a Git repository.")

    def _run(self,args:list[str],timeout:int=15)->GitResult:
        if not args or args[0] not in _ALLOWED:
            raise PermissionError("Git operation is not allowlisted.")
        if any(x in {"--exec","--upload-pack","--receive-pack"} or x.startswith("--exec=") for x in args):
            raise PermissionError("Git command injection options are blocked.")
        p=subprocess.run(["git",*args],cwd=self.root,text=True,capture_output=True,
                         timeout=min(timeout,30),shell=False)
        out=(p.stdout+p.stderr)[-_MAX_OUTPUT:]
        return GitResult(p.returncode==0,out,None if p.returncode==0 else "git command failed")

    def status(self): return self._run(["status","--short","--branch"])
    def diff(self,staged:bool=False): return self._run(["diff","--cached"] if staged else ["diff"])
    def log(self,limit:int=20):
        limit=max(1,min(limit,50)); return self._run(["log",f"--max-count={limit}","--oneline","--decorate"])
    def branch(self): return self._run(["branch","--show-current"])
    def show(self,ref="HEAD"):
        if not ref or ref.startswith("-") or any(c in ref for c in [";","&&","|"]):
            raise ValueError("Invalid git ref.")
        return self._run(["show","--stat","--oneline",ref])
