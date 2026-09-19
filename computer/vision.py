"""Optional screen observation and OCR boundary."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenObservation:
    width: int
    height: int
    text: str
    image: bytes

class ScreenObserver:
    def __init__(self, max_text=20000):
        self.max_text = max(100, min(max_text, 50000))

    def observe(self, adapter, ocr=False) -> ScreenObservation:
        image = adapter.screenshot()
        width = height = 0
        try:
            from io import BytesIO

            from PIL import Image
            with Image.open(BytesIO(image)) as im:
                width, height = im.size
        except (OSError, ValueError):
            pass
        text = ""
        if ocr:
            try:
                from io import BytesIO

                import pytesseract
                from PIL import Image
                with Image.open(BytesIO(image)) as im:
                    text = pytesseract.image_to_string(im)[:self.max_text]
            except ImportError as exc:
                raise RuntimeError("Install the optional vision dependency for OCR.") from exc
            except (OSError, RuntimeError, ValueError):
                text = ""
        return ScreenObservation(width, height, text, image)
