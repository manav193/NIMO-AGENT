from dataclasses import dataclass
from enum import Enum

class PromotionChannel(str, Enum):
    IN_APP = "in_app"
    WEBSITE = "website"
    EMAIL = "email"
    SOCIAL = "social"

@dataclass(frozen=True)
class Promotion:
    project_id: str
    title: str
    body: str
    channel: PromotionChannel
    destination: str
    enabled: bool = True

class PromotionPolicy:
    """Promotions are opt-in, auditable, and never silently injected into unrelated content."""
    def allowed(self, promotion: Promotion, context: str) -> bool:
        return promotion.enabled and bool(promotion.project_id and promotion.destination)
