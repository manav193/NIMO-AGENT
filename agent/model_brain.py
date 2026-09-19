"""Structured model-brain boundary for NIMO-Core backed planning."""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolIntent:
    tool_name:str
    arguments:dict[str,Any]
    reason:str
@dataclass(frozen=True)
class BrainResponse:
    text:str
    intents:list[ToolIntent]
    raw:dict[str,Any]
class ModelBrain:
    def __init__(self,core_client): self.core=core_client
    def ask(self,message:str,intent:str|None=None)->BrainResponse:
        if not message.strip(): raise ValueError("Message cannot be empty.")
        response=self.core.chat(message,intent=intent)
        text=response.get("reply") or response.get("message") or ""
        proposed=response.get("tool_calls") or response.get("actions") or []
        intents=[]
        if isinstance(proposed,list):
            for item in proposed:
                if isinstance(item,dict):
                    name=item.get("tool_name") or item.get("name"); args=item.get("arguments",{})
                    if isinstance(name,str) and name and isinstance(args,dict):
                        intents.append(ToolIntent(name,args,str(item.get("reason",""))))
        return BrainResponse(str(text),intents,response)
