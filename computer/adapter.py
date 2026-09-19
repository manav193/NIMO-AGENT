"""Platform adapter boundary. The agent never talks to OS input APIs directly."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol

class ComputerAdapter(Protocol):
    def screenshot(self) -> bytes: ...
    def click(self,x:int,y:int)->None: ...
    def type_text(self,text:str)->None: ...
    def press(self,key:str)->None: ...
    def open_app(self,app:str)->None: ...

@dataclass
class DryRunComputer:
    """Safe default adapter: records requested actions without touching the OS."""
    actions:list[dict]
    def screenshot(self)->bytes: return b""
    def click(self,x:int,y:int)->None: self.actions.append({"action":"click","x":x,"y":y})
    def type_text(self,text:str)->None: self.actions.append({"action":"type","length":len(text)})
    def press(self,key:str)->None: self.actions.append({"action":"press","key":key})
    def open_app(self,app:str)->None: self.actions.append({"action":"open_app","app":app})
