"""NIMO-KNOWLEDGE connector boundary. Only approved/sanitized entries are accepted."""
class KnowledgeConnector:
    def __init__(self,source): self.source=source
    def search(self,query,limit=10):
        rows=self.source.search(query,limit=min(max(limit,1),20))
        return [r for r in rows if r.get("sanitized") is True and r.get("status") in {"approved","active"}]
