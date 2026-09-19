from agent.context import ContextWindow
from agent.model_brain import ModelBrain
from agent.recovery import RecoveryPolicy


class Core:
    def chat(self,message,intent=None): return {"reply":"ok","tool_calls":[{"tool_name":"fs.read","arguments":{"path":"README.md"},"reason":"inspect docs"}]}
def test_brain_parses_structured_tool_calls():
    r=ModelBrain(Core()).ask("inspect"); assert r.text=="ok" and r.intents[0].tool_name=="fs.read"
def test_context_is_bounded():
    assert sum(len(x["content"]) for x in ContextWindow(10).build([{"role":"user","content":"123456789"},{"role":"user","content":"abc"}]))<=10
def test_recovery_is_bounded():
    p=RecoveryPolicy(2); assert p.decide("x",0).retry; assert not p.decide("x",2).retry
