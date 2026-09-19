from automation.engine import AutomationEngine
from automation.models import Automation, TriggerType
from integrations.email import AcknowledgementService, EmailMessage

class FakeEmail:
    def __init__(self):
        self.sent = []
    def send(self, message: EmailMessage) -> str:
        self.sent.append(message)
        return "msg-1"

def test_automation_registration():
    engine = AutomationEngine()
    engine.register(Automation("mail-ack", "Mail acknowledgement", TriggerType.EVENT, "email.ack"))
    assert engine.get("mail-ack").enabled

def test_automation_lifecycle():
    engine = AutomationEngine()
    engine.register(Automation("x", "X", TriggerType.EVENT, "noop"))
    engine.disable("x")
    assert not engine.get("x").enabled
    engine.enable("x")
    assert engine.get("x").enabled

def test_acknowledgement_sends_receipt():
    provider = FakeEmail()
    message_id = AcknowledgementService(provider).acknowledge("a@example.com", "Hello")
    assert message_id == "msg-1"
    assert provider.sent[0].subject == "Received: Hello"
