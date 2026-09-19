"""Consent-gated learning ingestion; no raw personal records enter knowledge."""
from __future__ import annotations

from dataclasses import dataclass

from security.consent import ConsentManager, Purpose


@dataclass(frozen=True)
class LearningProposal:
    proposal_id:str
    consent_id:str
    category:str
    sanitized_text:str
    pii_removed:bool
    secrets_removed:bool
    minimized:bool

class LearningPipeline:
    def __init__(self,consent:ConsentManager): self.consent=consent
    def propose(self,p:LearningProposal)->LearningProposal:
        self.consent.require(p.consent_id,Purpose.LEARNING_CONTRIBUTION,p.category)
        if not (p.pii_removed and p.secrets_removed and p.minimized):
            raise ValueError("Learning proposal must be sanitized, minimized, and secret-free")
        if not p.sanitized_text.strip(): raise ValueError("Empty sanitized proposal")
        return p
