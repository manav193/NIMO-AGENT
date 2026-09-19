from github.branching import BranchPolicy
from github.release import ReleaseWorkflow
def test_protected_branch():
    try: BranchPolicy().validate("main")
    except PermissionError: pass
    else: raise AssertionError("main accepted for direct modification")
def test_release_requires_passing_tests():
    class X: pass
    try: ReleaseWorkflow(X(),X(),X()).propose("feat/x",[],False,"x")
    except RuntimeError: pass
    else: raise AssertionError("release proposed without tests")
