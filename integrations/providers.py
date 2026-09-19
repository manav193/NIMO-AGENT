from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class ProviderCapability(str, Enum):
    READ = "read"
    SEARCH = "search"
    CREATE = "create"
    UPDATE = "update"
    EVENT = "event"
    SCHEDULE = "schedule"

@dataclass(frozen=True)
class ProviderRequest:
    provider: str
    operation: str
    payload: dict[str, Any] = field(default_factory=dict)
    idempotency_key: str | None = None

@dataclass(frozen=True)
class ProviderResult:
    success: bool
    data: Any = None
    error: str | None = None
    retryable: bool = False

class ProviderAdapter(Protocol):
    name: str
    capabilities: frozenset[ProviderCapability]
    def execute(self, request: ProviderRequest) -> ProviderResult: ...

class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderAdapter] = {}

    def register(self, provider: ProviderAdapter) -> None:
        key = provider.name.lower().lstrip("@")
        if key in self._providers:
            raise ValueError(f"Provider already registered: @{key}")
        self._providers[key] = provider

    def resolve(self, name: str) -> ProviderAdapter:
        key = name.lower().lstrip("@")
        if key not in self._providers:
            raise KeyError(f"Unknown provider: @{key}")
        return self._providers[key]

    def list(self) -> list[ProviderAdapter]:
        return list(self._providers.values())
