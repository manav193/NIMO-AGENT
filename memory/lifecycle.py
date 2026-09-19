"""Memory lifecycle and explicit forgetting boundary."""
class MemoryLifecycle:
    def __init__(self,store): self.store=store
    def forget(self,record_id): return self.store.delete(record_id)
