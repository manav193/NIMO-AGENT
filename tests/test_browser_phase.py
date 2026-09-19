from browser.recovery import BrowserRecovery
from browser.policy import BrowserPolicy
def test_recovery_is_bounded():
    r=BrowserRecovery(2); assert r.allowed(0); assert r.allowed(1); assert not r.allowed(2)
def test_policy_download_and_scheme_boundaries():
    p=BrowserPolicy(enabled=True,allowed_hosts={"example.com"},allow_downloads=True)
    p.check_url("https://example.com/a")
    try: p.check_url("file:///etc/passwd")
    except ValueError: pass
    else: raise AssertionError("file scheme accepted")
