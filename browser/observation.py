"""Bounded browser observation primitives."""
from dataclasses import dataclass


@dataclass(frozen=True)
class PageObservation:
    url:str
    title:str
    text:str
    screenshot:bytes|None
class BrowserObserver:
    def observe(self,adapter,max_chars=20000,with_screenshot=False):
        page=adapter._page
        text=adapter.page_text(max_chars)
        shot=adapter.screenshot() if with_screenshot else None
        return PageObservation(page.url,page.title(),text,shot)
