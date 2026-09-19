"""Purpose-specific consent enforcement for personal data and learning."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum

class Purpose(StrEnum):
    PERSONAL_MEMORY="personal_memory"
    LEARNING_CONTRIBUTION="learning_contribution"
    MODEL_IMPROVEMENT="model_improvement"
    ANALYTICS="analytics"

@dataclass(frozen=True)
class Consent:
    consent_id:str
    purpose:Purpose
    granted:bool
    data_categories:frozenset[str]
    retention:str="until_revoked"

class ConsentManager:
    def __init__(self): self._records:dict[str,Consent]={}
    def record(self,c:Consent)->None:
        self._records[c.consent_id]=c
    def revoke(self,consent_id:str)->None:
        old=self._records.get(consent_id)
        if old: self._records[consent_id]=Consent(old.consent_id,old.purpose,False,old.data_categories,old.retention)
    def allowed(self,consent_id:str,purpose:Purpose,category:str)->bool:
        c=self._records.get(consent_id)
        return bool(c and c.granted and c.purpose is purpose and category in c.data_categories)
    def require(self,consent_id:str,purpose:Purpose,category:str)->None:
        if not self.allowed(consent_id,purpose,category):
            raise PermissionError(f"Consent required for {purpose.value}:{category}")
