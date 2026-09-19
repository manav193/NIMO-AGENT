from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class AutomationEvent:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str | None = None
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

class EventBus:
    """In-process event boundary. Subscribers must be explicit."""
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[AutomationEvent], None]]] = {}

    def subscribe(self, name: str, handler: Callable[[AutomationEvent], None]) -> None:
        self._subscribers.setdefault(name, []).append(handler)

    def publish(self, event: AutomationEvent) -> int:
        handlers = list(self._subscribers.get(event.name, []))
        for handler in handlers:
            handler(event)
        return len(handlers)
