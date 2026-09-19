from tools.contracts import ToolRequest, ToolResult
from tools.registry import ToolRegistry

class Executor:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    def execute(self, request: ToolRequest) -> ToolResult:
        return self.registry.execute(request)
