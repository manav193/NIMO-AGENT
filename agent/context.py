"""Bounded context builder to control latency and accidental data exposure."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ContextWindow:
    max_chars:int=12000
    def build(self,messages:list[dict])->list[dict]:
        clean=[]
        total=0
        for m in reversed(messages):
            if not isinstance(m,dict): continue
            role=str(m.get("role",""))[:32]
            content=str(m.get("content",""))
            if total+len(content)>self.max_chars: break
            clean.append({"role":role,"content":content})
            total+=len(content)
        return list(reversed(clean))
