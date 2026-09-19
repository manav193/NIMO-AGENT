from automation.models import Automation

class AutomationEngine:
    """Stores automation definitions; execution is delegated to approved adapters."""
    def __init__(self) -> None:
        self._automations: dict[str, Automation] = {}
    def register(self, automation: Automation) -> None:
        if automation.id in self._automations:
            raise ValueError(f"Automation already exists: {automation.id}")
        self._automations[automation.id] = automation
    def get(self, automation_id: str) -> Automation:
        return self._automations[automation_id]
    def list(self) -> list[Automation]:
        return list(self._automations.values())
    def disable(self, automation_id: str) -> None:
        item = self.get(automation_id)
        self._automations[automation_id] = Automation(
            id=item.id, name=item.name, trigger=item.trigger,
            action=item.action, config=item.config, enabled=False,
        )
