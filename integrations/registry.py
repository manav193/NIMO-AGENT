from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PluginSpec:
    name: str
    description: str
    enabled: bool = True
    handler: Callable[[str], Any] | None = None

class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginSpec] = {}

    def register(self, plugin: PluginSpec) -> None:
        key = plugin.name.lower().lstrip("@")
        if key in self._plugins:
            raise ValueError(f"Plugin already registered: {key}")
        self._plugins[key] = PluginSpec(key, plugin.description, plugin.enabled, plugin.handler)

    def resolve(self, name: str) -> PluginSpec:
        key = name.lower().lstrip("@")
        try:
            plugin = self._plugins[key]
        except KeyError as exc:
            raise KeyError(f"Unknown plugin: @{key}") from exc
        if not plugin.enabled:
            raise ValueError(f"Plugin disabled: @{key}")
        return plugin

    def list(self) -> list[PluginSpec]:
        return list(self._plugins.values())
