from github.coding_agent import CodingAgent
from tools.git import GitWorkspace


def test_git_workspace_is_inspection_only(tmp_path):
    import subprocess
    subprocess.run(["git","init"],cwd=tmp_path,check=True,capture_output=True)
    g=GitWorkspace(tmp_path)
    assert g.branch().success
    assert g.status().success

def test_coding_agent_requires_confirmation():
    class Fake:
        def status(self): return type("R",(),{"output":"clean"})()
        def branch(self): return type("R",(),{"output":"main"})()
        def log(self): return type("R",(),{"output":"abc"})()
        def diff(self): return type("R",(),{"output":""})()
    p=CodingAgent(Fake()).propose("Add feature",["a.py"],["pytest"])
    assert p.requires_confirmation is True
