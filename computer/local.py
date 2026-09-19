"""Optional local desktop adapter.

Install the computer extra to enable real screenshots/input:
    pip install -e '.[computer]'
"""
from __future__ import annotations


class LocalComputer:
    def __init__(self):
        try:
            import mss
            import pyautogui
        except ImportError as exc:
            raise RuntimeError("Install the 'computer' extra to enable local computer control.") from exc
        self._mss=mss
        self._pyautogui=pyautogui
        self._pyautogui.PAUSE=0.08
        self._pyautogui.FAILSAFE=True

    def screenshot(self)->bytes:
        from io import BytesIO

        from PIL import Image
        with self._mss.mss() as sct:
            shot=sct.grab(sct.monitors[0])
            image=Image.frombytes("RGB",shot.size,shot.rgb)
            buf=BytesIO(); image.save(buf,format="PNG",optimize=True); return buf.getvalue()

    def click(self,x:int,y:int)->None: self._pyautogui.click(x=x,y=y)
    def type_text(self,text:str)->None: self._pyautogui.write(text,interval=0.01)
    def press(self,key:str)->None: self._pyautogui.press(key)
    def open_app(self,app:str)->None:
        # Opening arbitrary commands is intentionally unsupported here.
        raise PermissionError("Use an OS-specific allowlisted launcher adapter for applications.")
