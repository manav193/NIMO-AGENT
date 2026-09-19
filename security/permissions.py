from dataclasses import dataclass
from tools.contracts import RiskLevel, ToolSpec

@dataclass(frozen=True)
class PermissionDecision:
    allowed: bool
    requires_confirmation: bool = False
    reason: str = ""

class PermissionEngine:
    """Central policy gate. Restricted actions are never auto-approved."""

    def evaluate(self, spec: ToolSpec) -> PermissionDecision:
        if spec.risk is RiskLevel.RESTRICTED:
            return PermissionDecision(False, False, "Restricted action blocked.")
        if spec.risk is RiskLevel.CONFIRMED:
            return PermissionDecision(True, True, "User confirmation required.")
        return PermissionDecision(True, False, "Allowed by policy.")
