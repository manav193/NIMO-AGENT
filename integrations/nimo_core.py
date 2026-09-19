from dataclasses import dataclass

@dataclass(frozen=True)
class NimoCoreClient:
    """Transport boundary for NIMO Core; network behavior is added in a later phase."""
    base_url: str

    def health_endpoint(self) -> str:
        return f"{self.base_url.rstrip('/')}/health"
