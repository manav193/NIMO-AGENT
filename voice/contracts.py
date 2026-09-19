"""Voice pipeline contracts."""
from dataclasses import dataclass
@dataclass(frozen=True)
class VoiceInput:
    text:str
    language:str="auto"
    confidence:float=1.0
@dataclass(frozen=True)
class VoiceOutput:
    text:str
    language:str="auto"
class SpeechToText:
    def transcribe(self,audio:bytes)->VoiceInput: raise NotImplementedError
class TextToSpeech:
    def synthesize(self,text:str,language:str="auto")->bytes: raise NotImplementedError
