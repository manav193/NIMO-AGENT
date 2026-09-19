"""Hard consent gate for reusable learning data."""
from security.consent import Purpose


class LearningConsentGate:
    def __init__(self,consent_manager): self.consents=consent_manager
    def require_learning(self): self.consents.require(Purpose.LEARNING_CONTRIBUTION)
    def require_model_improvement(self): self.consents.require(Purpose.MODEL_IMPROVEMENT)
