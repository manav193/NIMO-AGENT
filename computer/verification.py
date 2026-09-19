"""Post-action verification primitives."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionVerification:
    success:bool
    reason:str
class ComputerVerifier:
    def verify_click(self,x:int,y:int,screen_size:tuple[int,int])->ActionVerification:
        w,h=screen_size
        return ActionVerification(0<=x<w and 0<=y<h,"coordinate remains inside observed screen")
    def verify_screen(self,image:bytes)->ActionVerification:
        return ActionVerification(bool(image),"screen capture returned data")
