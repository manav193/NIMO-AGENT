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

    def select(self,selector:str,value:str)->None:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if not selector or len(selector)>500 or len(value)>500: raise ValueError("Invalid select input.")
        if not hasattr(self.adapter,"select"): raise NotImplementedError("Adapter does not support select.")
        self.adapter.select(selector,value)

    def press(self,selector:str,key:str)->None:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if not selector or len(selector)>500 or len(key)>64: raise ValueError("Invalid key input.")
        if not hasattr(self.adapter,"press"): raise NotImplementedError("Adapter does not support press.")
        self.adapter.press(selector,key)

    def upload(self,selector:str,path:str)->None:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if not selector or not path: raise ValueError("Selector and path are required.")
        if not hasattr(self.adapter,"upload"): raise NotImplementedError("Adapter does not support upload.")
        self.adapter.upload(selector,path)

    def screenshot(self,path:str|None=None)->bytes:
        if not self.policy.enabled: raise PermissionError("Browser automation is disabled.")
        if not hasattr(self.adapter,"screenshot"): raise NotImplementedError("Adapter does not support screenshots.")
        return self.adapter.screenshot(path)

    def download(self,url:str)->str:
        self.policy.check_url(url); self.policy.check_download(); return self.adapter.download(url)

    def close(self)->None:
        if self.policy.enabled: self.adapter.close()
