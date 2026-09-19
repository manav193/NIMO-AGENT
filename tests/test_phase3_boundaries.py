from datetime import UTC, datetime, timedelta

from automation.events import AutomationEvent, EventBus
from automation.scheduler import Scheduler, ScheduleSpec
from integrations.dispatcher import PluginDispatcher
from integrations.plugin_router import PluginInvocation
from integrations.providers import (
    ProviderCapability,
    ProviderRegistry,
    ProviderRequest,
    ProviderResult,
)
from integrations.registry import PluginRegistry, PluginSpec


class DemoProvider:
    name = "demo"
    capabilities = frozenset({ProviderCapability.READ})
    def execute(self, request: ProviderRequest) -> ProviderResult:
        return ProviderResult(True, {"operation": request.operation, "payload": request.payload})

def test_provider_registry_and_dispatch():
    plugins=PluginRegistry()
    plugins.register(PluginSpec("demo", "demo"))
    providers=ProviderRegistry()
    providers.register(DemoProvider())
    result=PluginDispatcher(plugins, providers).dispatch(PluginInvocation("demo","hello"))
    assert result.success is True
    assert result.output["payload"]["task"] == "hello"

def test_event_bus():
    seen=[]
    bus=EventBus()
    bus.subscribe("x", lambda event: seen.append(event.payload["v"]))
    assert bus.publish(AutomationEvent("x", {"v": 7})) == 1
    assert seen == [7]

def test_persistent_scheduler_claim():
    scheduler=Scheduler()
    when=datetime.now(UTC)+timedelta(seconds=1)
    job=scheduler.schedule(ScheduleSpec("a",when))
    assert scheduler.claim(job) is False
    due=scheduler.due(when+timedelta(seconds=1))
    assert len(due)==1
    assert scheduler.claim(job, now=when + timedelta(seconds=1)) is True
    assert scheduler.due(when+timedelta(seconds=2)) == []
    scheduler.close()
