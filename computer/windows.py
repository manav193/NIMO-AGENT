"""Window/app observation boundary; no arbitrary process launching."""
from dataclasses import dataclass


@dataclass(frozen=True)
class WindowInfo:
    title:str
    app:str
class WindowObserver:
    def list_windows(self)->list[WindowInfo]:
        try:
            import pygetwindow as gw
        except ImportError: return []
        result=[]
        for w in gw.getAllWindows():
            title=(w.title or "").strip()
            if title: result.append(WindowInfo(title,title))
        return result
    def active_window(self)->WindowInfo|None:
        try:
            import pygetwindow as gw
            w=gw.getActiveWindow()
            return WindowInfo(w.title,w.title) if w and w.title else None
        except ImportError: return None
