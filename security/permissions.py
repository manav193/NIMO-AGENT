from dataclasses import dataclass
from enum import Enum
from tools.contracts import RiskLevel, ToolSpec

class AgentMode(str, Enum):
    BASIC = "basic"
    MODERATE = "moderate"
    TURBO = "turbo"

@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    requires_confirmation: bool = False
    reason: str = ""

class PermissionEngine:
    """Central policy gate. Modes tune friction; hard security boundaries remain mandatory."""

    def __init__(self, mode: AgentMode = AgentMode.BASIC) -> None:
        self.mode = mode

    def set_mode(self, mode: AgentMode) -> None:
        self.mode = mode

    def evaluate(self, spec: ToolSpec) -> PermissionDecision:
        # Restricted operations never become silently executable in any mode.
        if spec.risk is RiskLevel.RESTRICTED:
            return PermissionDecision(False, False, "Restricted action blocked in every mode.")

        if self.mode is AgentMode.BASIC:
            if spec.risk is RiskLevel.CONFIRMED:
                return PermissionDecision(True, True, "Confirmation required in Basic mode.")
            return PermissionDecision(True, False, "Allowed by Basic mode.")

        if self.mode is AgentMode.MODERATE:
            if spec.risk is RiskLevel.CONFIRMED:
                return PermissionDecision(True, True, "Confirmation required in Moderate mode.")
            return PermissionDecision(True, False, "Allowed by Moderate mode.")

        # Turbo minimizes confirmation friction for non-restricted tools,
        # while retaining filesystem boundaries, command allowlists, secret isolation,
        # audit logging and explicit blocking of restricted actions.
        return PermissionDecision(True, False, "Allowed by Turbo mode.")
