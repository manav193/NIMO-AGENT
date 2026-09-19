"""Policy-enforced computer controller."""
from __future__ import annotations
from dataclasses import dataclass
from computer.adapter import ComputerAdapter
from computer.policy import ComputerPolicy

@dataclass
class ComputerController:
    adapter: ComputerAdapter
    policy: ComputerPolicy

    def screenshot(self)->bytes:
        self.policy.check_enabled()
        return self.adapter.screenshot()

    def click(self,x:int,y:int)->None:
        self.policy.check_point(x,y); self.adapter.click(x,y)

    def type_text(self,text:str)->None:
        self.policy.check_enabled()
        if len(text)>4000: raise ValueError("Text input exceeds the safety limit.")
        self.adapter.type_text(text)

    def press(self,key:str)->None:
        self.policy.check_enabled()
        allowed={"enter","esc","escape","tab","space","backspace","up","down","left","right","home","end"}
        if key.lower() not in allowed: raise PermissionError("Key is not in the safe key allowlist.")
        self.adapter.press(key.lower())

    def open_app(self,app:str)->None:
        self.policy.check_app(app); self.adapter.open_app(app)

    def stop(self)->None:
        self.policy.emergency_stop=True
