from pathlib import Path

from tools.contracts import RiskLevel, ToolResult, ToolSpec

class SafeFileSystem:
    def __init__(self, roots: list[Path]):
        self.roots = tuple(p.resolve() for p in roots)

    def _resolve(self, raw: str) -> Path:
        path = Path(raw).expanduser().resolve()
        if not any(path == r or r in path.parents for r in self.roots):
            raise PermissionError("Path is outside configured NIMO-Agent roots.")
        return path

    def list_dir(self, args: dict) -> ToolResult:
        try:
            p = self._resolve(args.get("path", "."))
            return ToolResult(True, [x.name for x in sorted(p.iterdir())]) if p.is_dir() else ToolResult(False, error="Not a directory.")
        except (KeyError, OSError, PermissionError, ValueError) as exc:
            return ToolResult(False, error=str(exc))

    def read_file(self, args: dict) -> ToolResult:
        try:
            p = self._resolve(args["path"])
            if not p.is_file():
                return ToolResult(False, error="Not a file.")
            return ToolResult(True, p.read_text(encoding="utf-8")[:100000])
        except (KeyError, OSError, PermissionError, UnicodeError, ValueError) as exc:
            return ToolResult(False, error=str(exc))

    def specs(self) -> list[ToolSpec]:
        return [
            ToolSpec("fs.list", "List an allowlisted directory.", RiskLevel.READ, self.list_dir),
            ToolSpec("fs.read", "Read an allowlisted text file.", RiskLevel.READ, self.read_file),
        ]
