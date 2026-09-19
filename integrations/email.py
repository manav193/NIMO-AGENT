from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class EmailMessage:
    to: str
    subject: str
    body: str
    reply_to: str | None = None

class EmailProvider(Protocol):
    def send(self, message: EmailMessage) -> str:
        """Send an email and return a provider message id."""

class AcknowledgementService:
    """Automatic receipt acknowledgement; it does not generate an AI answer."""
    def __init__(self, provider: EmailProvider) -> None:
        self.provider = provider
    def acknowledge(self, sender: str, original_subject: str) -> str:
        return self.provider.send(EmailMessage(
            to=sender,
            subject=f"Received: {original_subject}",
            body=("Thanks for your email. This is an automatic acknowledgement "
                  "confirming that your message was received."),
        ))
