"""Policy-enforced browser controller. No direct browser calls from the agent."""
from __future__ import annotations
from dataclasses import dataclass
from browser.adapter import BrowserAdapter
from browser.policy import BrowserPolicy

@dataclass
class BrowserController:
    adapter:BrowserAdapter
    policy:BrowserPolicy

    def open(self,url:str)->str:
        self.policy.check_url(url); return self.adapter.open(url)

    def page_text(self,max_chars:int=100000)->str:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        max_chars=max(1,min(max_chars,100000))
        return self.adapter.page_text(max_chars)

    def click(self,selector:str)->None:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if not selector or len(selector)>500: raise ValueError("Invalid selector.")
        self.adapter.click(selector)

    def fill(self,selector:str,text:str)->None:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if len(text)>4000: raise ValueError("Form input exceeds safety limit.")
        if not selector: raise ValueError("Selector is required.")
        self.adapter.fill(selector,text)

    def download(self,url:str)->str:
        self.policy.check_url(url); self.policy.check_download(); return self.adapter.download(url)

    def close(self)->None:
        if self.policy.enabled: self.adapter.close()
