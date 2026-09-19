from abc import ABC, abstractmethod
from typing import Any

class ModelProvider(ABC):
    name: str

    @abstractmethod
    def generate(self, messages: list[dict[str, Any]], **kwargs: Any) -> str:
        raise NotImplementedError
