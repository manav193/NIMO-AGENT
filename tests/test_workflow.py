from automation.retry import RetryPolicy
from automation.triggers import Trigger, TriggerRegistry
from automation.workflow import Workflow, WorkflowEngine, WorkflowStep


def test_workflow_has_step_bound():
    w=Workflow("x",[WorkflowStep("1","noop")])
    out=WorkflowEngine(lambda a,args: a).run(w); assert out==["noop"]
def test_trigger_allowlist():
    TriggerRegistry().validate(Trigger("manual","x"))
    try: TriggerRegistry().validate(Trigger("shell","x"))
    except ValueError: pass
    else: raise AssertionError("unsafe trigger accepted")
def test_retry_is_bounded():
    r=RetryPolicy(3); assert r.decide(0).retry and not r.decide(3).retry
