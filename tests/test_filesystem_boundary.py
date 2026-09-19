from pathlib import Path
from tools.filesystem import SafeFileSystem

def test_filesystem_allows_only_configured_root(tmp_path: Path):
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("secret", encoding="utf-8")
    fs = SafeFileSystem([allowed])
    result = fs.read_file({"path": str(outside)})
    assert result.success is False
