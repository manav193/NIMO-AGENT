from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Verification:
    success: bool
    reason: str

class Verifier:
    def verify(self, result: Any) -> Verification:
        success = bool(getattr(result, "success", True))
        return Verification(success, "Execution completed." if success else "Execution failed.")
