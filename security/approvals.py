from dataclasses import dataclass

@dataclass
class ApprovalManager:
    """Phase-2 approval boundary. UI/interactive approval is added later."""

    def approve(self, reason: str) -> bool:
        return False
