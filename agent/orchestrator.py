"""End-to-end model -> permission -> tool -> observe -> verify loop."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from agent.model_brain import ModelBrain
from agent.state import AgentState

@dataclass(frozen=True)
class OrchestrationResult:
    reply:str
    executed:list[dict[str,Any]]
    blocked:list[dict[str,Any]]

class AgentOrchestrator:
    def __init__(self,brain,runtime):
        self.brain=brain; self.runtime=runtime

    def handle(self,message:str,state:AgentState)->OrchestrationResult:
        brain=self.brain.ask(message)
        executed=[]; blocked=[]
        for intent in brain.intents:
            try:
                result,observation,verification=self.runtime.execute_tool(
                    type("Request",(),{"tool_name":intent.tool_name,"arguments":intent.arguments,"requested_by":"model"})()
                )
                item={"tool":intent.tool_name,"success":result.success,"verified":verification.success}
                (executed if result.success and verification.success else blocked).append(item)
            except Exception as exc:
                blocked.append({"tool":intent.tool_name,"success":False,"error":str(exc)})
        return OrchestrationResult(brain.text,executed,blocked)
