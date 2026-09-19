import time
class RateLimiter:
    def __init__(self,limit=30,window_seconds=60): self.limit=max(1,limit); self.window=window_seconds; self.events={}
    def allow(self,key):
        now=time.monotonic(); events=[x for x in self.events.get(key,[]) if now-x<self.window]
        if len(events)>=self.limit: self.events[key]=events; return False
        events.append(now); self.events[key]=events; return True
