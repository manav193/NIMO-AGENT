from tools.contracts import ToolRequest, ToolResult, ToolSpec

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        if spec.name in self._tools:
            raise ValueError(f"Tool already registered: {spec.name}")
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec:
        try:
            return self._tools[name]
        except KeyError as exc:
            raise KeyError(f"Unknown tool: {name}") from exc

    def list(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def execute(self, request: ToolRequest) -> ToolResult:
        return self.get(request.tool_name).handler(request.arguments)
