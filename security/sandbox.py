from dataclasses import dataclass


@dataclass(frozen=True)
class SandboxPolicy:
    max_seconds:int=30
    network_allowed:bool=False
    writable_roots:tuple[str,...]=()
    def validate(self,command):
        if not command or len(command)>32: raise PermissionError("Invalid sandbox command.")
        blocked=("&&","||",";","|",">","<")
        if any(any(x in arg for x in blocked) for arg in command): raise PermissionError("Shell composition blocked.")
