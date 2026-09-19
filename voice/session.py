"""Hands-free voice session with explicit stop and bounded input."""
from dataclasses import dataclass
@dataclass
class VoiceSession:
    active:bool=False
    max_text:int=4000
    def start(self): self.active=True
    def stop(self): self.active=False
    def accept(self,text:str)->str:
        if not self.active: raise PermissionError("Voice session is not active.")
        text=text.strip()
        if not text: raise ValueError("Voice input is empty.")
        if len(text)>self.max_text: raise ValueError("Voice input exceeds safety limit.")
        return text
