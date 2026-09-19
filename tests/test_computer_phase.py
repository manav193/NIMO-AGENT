from computer.session import ComputerSession
from computer.verification import ComputerVerifier


def test_session_stop_is_latched():
    s=ComputerSession("x"); s.stop()
    try: s.check()
    except PermissionError: pass
    else: raise AssertionError("stopped session resumed")
def test_screen_verification():
    assert ComputerVerifier().verify_screen(b"png").success
def test_launcher_never_falls_back_to_shell():
    from computer.launcher import AllowlistedLauncher
    l=AllowlistedLauncher({})
    try: l.launch("terminal")
    except PermissionError: pass
    else: raise AssertionError("unknown launcher accepted")
