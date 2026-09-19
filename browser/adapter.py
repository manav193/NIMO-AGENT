"""Browser adapter contract with a dry-run implementation."""
from __future__ import annotations

from typing import Protocol


class BrowserAdapter(Protocol):
    def open(self,url:str)->str: ...
    def page_text(self,max_chars:int=100000)->str: ...
    def click(self,selector:str)->None: ...
    def fill(self,selector:str,text:str)->None: ...
    def download(self,url:str)->str: ...
    def close(self)->None: ...

class DryRunBrowser:
    def __init__(self): self.actions=[]
    def open(self,url): self.actions.append({"action":"open","url":url}); return "dry-run"
    def page_text(self,max_chars=100000): self.actions.append({"action":"read"}); return ""
    def click(self,selector): self.actions.append({"action":"click","selector":selector})
    def fill(self,selector,text): self.actions.append({"action":"fill","selector":selector,"length":len(text)})
    def download(self,url): self.actions.append({"action":"download","url":url}); return "dry-run"
    def close(self): self.actions.append({"action":"close"})
