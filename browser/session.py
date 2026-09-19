"""Isolated browser session lifecycle."""
from dataclasses import dataclass

from browser.controller import BrowserController
from browser.playwright_adapter import PlaywrightBrowser
from browser.policy import BrowserPolicy


@dataclass
class BrowserSessionManager:
    policy:BrowserPolicy
    def start(self,headless=True,download_dir=None):
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        adapter=PlaywrightBrowser(headless=headless,download_dir=download_dir)
        return BrowserController(adapter,self.policy)
