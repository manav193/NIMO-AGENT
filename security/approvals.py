from dataclasses import dataclass, field

@dataclass
class ApprovalManager:
    """Explicit approval boundary; nothing is approved implicitly."""
    approved_tokens: set[str] = field(default_factory=set)

    def request(self, token: str) -> bool:
        return False

    def grant(self, token: str) -> None:
        if token:
            self.approved_tokens.add(token)

    def approve(self, token: str, reason: str = "") -> bool:
        return bool(token) and token in self.approved_tokens
