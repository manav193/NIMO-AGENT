from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from security.secrets import redact

def _safe(value: Any) -> Any:
    if isinstance(value, str): return redact(value)
    if isinstance(value, dict): return {str(k): _safe(v) for k,v in value.items()}
    if isinstance(value, list): return [_safe(v) for v in value]
    if isinstance(value, tuple): return [_safe(v) for v in value]
    return value

@dataclass
class AuditLogger:
    events:list[dict[str,Any]]=field(default_factory=list)
    def record(self,action:str,actor:str,resource:str,details:dict[str,Any]|None=None)->None:
        self.events.append({"timestamp":datetime.now(timezone.utc).isoformat(),
            "action":redact(action),"actor":redact(actor),"resource":redact(resource),
            "details":_safe(details or {})})
