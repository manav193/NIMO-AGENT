"""NEXUS control-plane integration boundary."""
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class NexusDecision:
    allowed: bool
    requires_approval: bool = False
    reason: str = ""
    risk: str = "unknown"
    fingerprint: str | None = None


@dataclass(frozen=True)
class NexusClient:
    """Transport-neutral NEXUS gateway client."""
    base_url: str | None = None
    timeout: float = 10.0
    transport: Callable[[dict[str, Any]], dict[str, Any]] | None = None

    def evaluate(self, action: dict[str, Any]) -> NexusDecision:
        payload = {"type": "NEXUS_ACTION", "action": action}
        if self.transport is not None:
            response = self.transport(payload)
        elif self.base_url:
            request = Request(
                f"{self.base_url.rstrip('/')}/v1/gateway/evaluate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=self.timeout) as response_obj:
                response = json.loads(response_obj.read().decode("utf-8"))
        else:
            raise RuntimeError("NEXUS transport is not configured.")

        if not isinstance(response, dict):
            raise ValueError("Invalid NEXUS decision response.")
        return NexusDecision(
            allowed=bool(response.get("allowed", False)),
            requires_approval=bool(
                response.get("requiresApproval", response.get("requires_approval", False))
            ),
            reason=str(response.get("reason", "")),
            risk=str(response.get("risk", "unknown")),
            fingerprint=response.get("fingerprint"),
        )

    def authorize(self, action: dict[str, Any]) -> NexusDecision:
        return self.evaluate(action)
