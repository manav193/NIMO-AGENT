"""Consent-aware memory facade. Raw memory stays in the encrypted vault."""
from __future__ import annotations

from security.consent import ConsentManager, Purpose
from security.vault import EncryptedVault


class PersonalMemory:
    def __init__(self,vault:EncryptedVault,consent:ConsentManager):
        self.vault=vault; self.consent=consent
    def save(self,record_id:str,value:dict,consent_id:str)->None:
        self.consent.require(consent_id,Purpose.PERSONAL_MEMORY,"conversation")
        self.vault.put(record_id,value,consent_id)
    def read(self,record_id:str,consent_id:str)->dict:
        value=self.vault.get(record_id)
        # Consent is checked before returning private memory to the runtime.
        self.consent.require(consent_id,Purpose.PERSONAL_MEMORY,"conversation")
        return value
    def forget(self,record_id:str,consent_id:str)->bool:
        self.consent.require(consent_id,Purpose.PERSONAL_MEMORY,"conversation")
        return self.vault.delete(record_id)
