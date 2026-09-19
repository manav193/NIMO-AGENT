"""Consent-aware memory retrieval with bounded, relevance-first results."""
from dataclasses import dataclass
from security.consent import Purpose
@dataclass(frozen=True)
class MemoryHit:
    record_id:str
    text:str
    score:float
class MemoryRetriever:
    def __init__(self,store): self.store=store
    def search(self,query:str,consent_manager,limit:int=5):
        consent_manager.require(Purpose.PERSONAL_MEMORY)
        limit=max(1,min(limit,20))
        q=set(query.lower().split()); hits=[]
        for item in self.store.list():
            text=str(item.get("text",""))
            score=len(q & set(text.lower().split()))
            if score: hits.append(MemoryHit(str(item.get("id","")),text,float(score)))
        return sorted(hits,key=lambda x:x.score,reverse=True)[:limit]
