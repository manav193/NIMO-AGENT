"""Bounded context builder for latency and data minimization."""
from dataclasses import dataclass


@dataclass
class ContextWindow:
    max_chars:int=12000
    def build(self,messages:list[dict])->list[dict]:
        clean=[]; total=0
        for m in reversed(messages):
            if not isinstance(m,dict): continue
            content=str(m.get("content",""))
            if total+len(content)>self.max_chars: break
            clean.append({"role":str(m.get("role",""))[:32],"content":content}); total+=len(content)
        return list(reversed(clean))
