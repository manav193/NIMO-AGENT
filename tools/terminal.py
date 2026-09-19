import subprocess
from tools.contracts import RiskLevel, ToolResult, ToolSpec

class SafeTerminal:
    def __init__(self, allowed_commands=None, timeout=10):
        self.allowed_commands = allowed_commands or {"python", "python3", "pytest", "ruff", "git"}
        self.timeout = max(1, min(timeout, 30))

    def run(self, args):
        command = args.get("command", "")
        parts = command.split()
        if not parts or parts[0] not in self.allowed_commands:
            return ToolResult(False, error="Command is not allowlisted.")
        if any(x in command for x in ["&&", "||", ";", "|", ">", "<", "$("]):
            return ToolResult(False, error="Shell chaining/redirection is blocked.")
        try:
            p = subprocess.run(parts, capture_output=True, text=True, timeout=self.timeout, shell=False)
            return ToolResult(p.returncode == 0, {"stdout": p.stdout[-20000:], "stderr": p.stderr[-20000:], "returncode": p.returncode}, None if p.returncode == 0 else "Command failed.")
        except subprocess.TimeoutExpired:
            return ToolResult(False, error="Command timed out.")
        except Exception as exc:
            return ToolResult(False, error=str(exc))

    def spec(self):
        return ToolSpec("terminal.run", "Run a restricted local command.", RiskLevel.CONFIRMED, self.run)
