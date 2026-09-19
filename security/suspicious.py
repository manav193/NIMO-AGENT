from dataclasses import dataclass
@dataclass(frozen=True)
class Finding:
    rule:str
    severity:str
    detail:str
class SuspiciousActivityDetector:
    def inspect(self,action,arguments):
        text=(action+" "+repr(arguments)).lower()
        rules=[("secret_access","high",("private key","api_key","password","token")),("destructive","critical",("rm -rf","format c:","del /f","shutdown")),("exfiltration","critical",("curl","wget","upload","webhook"))]
        return [Finding(n,s,"matched restricted pattern") for n,s,needles in rules if any(x in text for x in needles)]
