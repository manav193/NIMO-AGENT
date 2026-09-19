"""Consent-aware retrieval over encrypted personal memory."""
from dataclasses import dataclass

from security.consent import Purpose


@dataclass(frozen=True)
class MemoryHit:
    record_id:str
    text:str
    score:float

class MemoryRetriever:
    def __init__(self,store): self.store=store

    def search(self,query,consent_id,limit=5):
        if not query.strip(): return []
        self.store.consent.require(consent_id,Purpose.PERSONAL_MEMORY,"conversation")
        limit=max(1,min(limit,20)); q=set(query.lower().split()); hits=[]
        for record_id in self.store.vault.list_ids():
            value=self.store.read(record_id,consent_id)
            text=str(value.get("text","")) if isinstance(value,dict) else str(value)
            score=len(q & set(text.lower().split()))
            if score: hits.append(MemoryHit(record_id,text,float(score)))
        return sorted(hits,key=lambda x:x.score,reverse=True)[:limit]
