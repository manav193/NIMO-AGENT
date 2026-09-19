from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime

from automation.models import Automation, AutomationRun, AutomationStatus


class AutomationEngine:
    """Lifecycle + run journal; actual actions remain behind approved adapters."""
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

    def start_run(self, automation_id: str) -> AutomationRun:
        run = AutomationRun(automation_id, datetime.now(UTC))
        self.record_run(run)
        return run

    def finish_run(self, run: AutomationRun, success: bool, error: str | None = None) -> AutomationRun:
        finished = replace(run, finished_at=datetime.now(UTC), success=success, error=error)
        self._runs[-1] = finished
        return finished

    def runs(self) -> list[AutomationRun]:
        return list(self._runs)
