from voice.wake import WakeWordGate
from voice.session import VoiceSession
def test_wake_gate():
    g=WakeWordGate(); assert g.feed("hey NIMO"); assert g.active
def test_voice_session_bounds():
    s=VoiceSession(); s.start(); assert s.accept("hello")=="hello"
    try: s.accept("x"*4001)
    except ValueError: pass
    else: raise AssertionError("oversized voice input accepted")
def test_voice_stops():
    s=VoiceSession(); s.start(); s.stop()
    try: s.accept("hello")
    except PermissionError: pass
    else: raise AssertionError("stopped voice session accepted input")
