"""Allowlisted application launcher contract. Never accepts shell commands."""
class AllowlistedLauncher:
    def __init__(self,launchers:dict[str,callable]): self.launchers=dict(launchers)
    def launch(self,app:str):
        if app not in self.launchers: raise PermissionError("Application is not allowlisted.")
        return self.launchers[app]()
