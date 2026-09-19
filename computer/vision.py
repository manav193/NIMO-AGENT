"""Optional screen observation and OCR boundary."""
from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ScreenObservation:
    width:int
    height:int
    text:str
    image:bytes
class ScreenObserver:
    def __init__(self,max_text=20000): self.max_text=max(100,min(max_text,50000))
    def observe(self,adapter,ocr=False)->ScreenObservation:
        image=adapter.screenshot()
        width=height=0
        try:
            from PIL import Image
            from io import BytesIO
            with Image.open(BytesIO(image)) as im: width,height=im.size
        except Exception: pass
        text=""
        if ocr:
            try:
                import pytesseract
                from PIL import Image
                from io import BytesIO
                text=pytesseract.image_to_string(Image.open(BytesIO(image)))[:self.max_text]
            except ImportError: raise RuntimeError("Install the optional vision dependency for OCR.")
        return ScreenObservation(width,height,text,image)
