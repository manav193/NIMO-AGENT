from browser.adapter import DryRunBrowser
from browser.controller import BrowserController
from browser.policy import BrowserPolicy


def test_browser_disabled_by_default():
    c=BrowserController(DryRunBrowser(),BrowserPolicy())
    try: c.open("https://example.com")
    except PermissionError: pass
    else: raise AssertionError("browser must be disabled by default")

def test_allowlisted_navigation_and_read():
    a=DryRunBrowser(); c=BrowserController(a,BrowserPolicy(enabled=True,allowed_hosts={"example.com"}))
    assert c.open("https://example.com")=="dry-run"
    assert c.page_text()==""
    try: c.open("https://evil.example")
    except PermissionError: pass
    else: raise AssertionError("non-allowlisted host accepted")

def test_download_requires_explicit_permission():
    c=BrowserController(DryRunBrowser(),BrowserPolicy(enabled=True,allowed_hosts={"example.com"}))
    try: c.download("https://example.com/file")
    except PermissionError: pass
    else: raise AssertionError("download permission bypassed")

def test_form_and_selector_limits():
    c=BrowserController(DryRunBrowser(),BrowserPolicy(enabled=True))
    c.fill("#name","Manav")
    try: c.fill("#name","x"*4001)
    except ValueError: pass
    else: raise AssertionError("oversized form input accepted")
