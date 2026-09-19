"""Wake-word state machine; audio capture is kept behind an adapter."""
from dataclasses import dataclass


@dataclass
class WakeWordGate:
    wake_word:str="nimo"
    active:bool=False
    def feed(self,text:str)->bool:
        normalized=text.strip().lower()
        if self.wake_word.lower() in normalized:
            self.active=True
            return True
        return self.active
    def reset(self): self.active=False
