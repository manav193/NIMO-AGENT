from dataclasses import replace
from automation.models import Automation, AutomationRun, AutomationStatus

class AutomationEngine:
    """Registry and lifecycle manager; adapters execute approved actions."""
    def __init__(self) -> None:
        self._automations: dict[str, Automation] = {}
        self._runs: list[AutomationRun] = []
    def register(self, automation: Automation) -> None:
        if automation.id in self._automations:
            raise ValueError(f"Automation already exists: {automation.id}")
        self._automations[automation.id] = automation
    def get(self, automation_id: str) -> Automation:
        return self._automations[automation_id]
    def list(self) -> list[Automation]:
        return list(self._automations.values())
    def pause(self, automation_id: str) -> None:
        self._automations[automation_id] = replace(self.get(automation_id), status=AutomationStatus.PAUSED)
    def disable(self, automation_id: str) -> None:
        self._automations[automation_id] = replace(self.get(automation_id), status=AutomationStatus.DISABLED)
    def enable(self, automation_id: str) -> None:
        self._automations[automation_id] = replace(self.get(automation_id), status=AutomationStatus.ENABLED)
    def record_run(self, run: AutomationRun) -> None:
        self._runs.append(run)
    def runs(self) -> list[AutomationRun]:
        return list(self._runs)
