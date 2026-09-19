from pathlib import Path

from tools.filesystem import SafeFileSystem
from tools.terminal import SafeTerminal


def test_filesystem_blocks_escape(tmp_path: Path):
    fs = SafeFileSystem([tmp_path])
    result = fs.read_file({"path": str(tmp_path.parent)})
    assert result.success is False

def test_terminal_blocks_chaining():
    result = SafeTerminal().run({"command": "python --version && whoami"})
    assert result.success is False
