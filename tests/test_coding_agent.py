from github.workspace import Workspace,WorkspacePolicy
from github.edit import EditEngine
def test_workspace_blocks_escape(tmp_path):
    w=Workspace(WorkspacePolicy(tmp_path))
    try: w.read("../secret")
    except (PermissionError,FileNotFoundError): pass
    else: raise AssertionError("workspace escape")
def test_edit_requires_real_change(tmp_path):
    (tmp_path/"a.py").write_text("x=1\n")
    w=Workspace(WorkspacePolicy(tmp_path))
    p=EditEngine().propose(w,"a.py","x=2\n")
    assert p.requires_confirmation and "-x=1" in p.diff
