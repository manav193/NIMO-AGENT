from integrations.nexus import NexusClient


def test_nexus_transport_decision():
    seen = {}

    def transport(payload):
        seen.update(payload)
        return {
            "allowed": True,
            "requiresApproval": True,
            "reason": "approval required",
            "risk": "high",
            "fingerprint": "abc123",
        }

    decision = NexusClient(transport=transport).authorize({
        "tool": "github.release",
        "arguments": {},
    })

    assert decision.allowed is True
    assert decision.requires_approval is True
    assert decision.risk == "high"
    assert seen["type"] == "NEXUS_ACTION"


def test_nexus_fail_closed_when_unconfigured():
    try:
        NexusClient().evaluate({"tool": "test"})
        assert False
    except RuntimeError as exc:
        assert "not configured" in str(exc)
