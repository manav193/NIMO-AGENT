from security.approvals import ApprovalManager

def test_approval_is_explicit():
    manager = ApprovalManager()
    assert manager.approve("x") is False
    manager.grant("x")
    assert manager.approve("x") is True
