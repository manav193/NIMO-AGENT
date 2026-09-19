from dataclasses import dataclass
from urllib.request import Request, urlopen
import json

@dataclass(frozen=True)
class NimoCoreClient:
    """HTTP transport for NIMO Core."""
    base_url: str
    timeout: float = 15.0

    def _url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"

    def health_endpoint(self) -> str:
        return self._url("/api/health")

    def chat(self, message: str, intent: str | None = None) -> dict:
        payload = {"message": message}
        if intent:
            payload["intent"] = intent
        request = Request(
            self._url("/api/nimo/chat"),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))
