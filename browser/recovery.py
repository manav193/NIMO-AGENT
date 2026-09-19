"""Browser recovery without unbounded retries."""
class BrowserRecovery:
    def __init__(self,max_retries=2): self.max_retries=max(0,min(max_retries,3))
    def allowed(self,attempt): return attempt<self.max_retries
