import re
_PATTERNS=(re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+"),re.compile(r"sk-[A-Za-z0-9_-]{12,}"))
def redact(text):
    out=str(text)
    for p in _PATTERNS: out=p.sub("[REDACTED]",out)
    return out
