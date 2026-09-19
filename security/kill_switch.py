class KillSwitch:
    def __init__(self): self._stopped=False
    def stop(self): self._stopped=True
    def reset(self): self._stopped=False
    def check(self):
        if self._stopped: raise PermissionError("NIMO emergency shutdown is active.")
