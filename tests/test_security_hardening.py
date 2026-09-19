from security.rate_limit import RateLimiter
from security.sandbox import SandboxPolicy
from security.secrets import redact
from security.suspicious import SuspiciousActivityDetector


def test_suspicious_patterns(): assert SuspiciousActivityDetector().inspect("terminal.run",{"command":"rm -rf /"})
def test_secret_redaction(): assert "sk-secret" not in redact("token=sk-secret")
def test_rate_limit():
    r=RateLimiter(1,60); assert r.allow("x"); assert not r.allow("x")
def test_shell_composition_blocked():
    try: SandboxPolicy().validate(["python","-c","x && y"])
    except PermissionError: pass
    else: raise AssertionError("shell composition accepted")
