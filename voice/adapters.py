"""Optional provider-neutral voice adapters."""
class TextSTT:
    def transcribe(self,audio:bytes):
        raise RuntimeError("No local STT provider configured.")
class TextTTS:
    def synthesize(self,text:str,language="auto")->bytes:
        raise RuntimeError("No local TTS provider configured.")
