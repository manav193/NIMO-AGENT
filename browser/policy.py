"""Browser safety boundary: navigation is constrained before any browser adapter sees it."""
from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class BrowserPolicy:
    enabled: bool=False
    allowed_hosts: set[str]=field(default_factory=set)
    allow_downloads: bool=False
    max_url_length:int=2048

    def check_url(self,url:str)->None:
        if not self.enabled: raise PermissionError("Browser automation is disabled.")
        if len(url)>self.max_url_length: raise ValueError("URL exceeds safety limit.")
        p=urlparse(url)
        if p.scheme not in {"https","http"} or not p.hostname:
            raise ValueError("Only HTTP(S) URLs are supported.")
        if self.allowed_hosts and p.hostname.lower() not in {h.lower() for h in self.allowed_hosts}:
            raise PermissionError("Host is not allowlisted.")

    def check_download(self)->None:
        if not self.enabled: raise PermissionError("Browser automation is disabled.")
        if not self.allow_downloads: raise PermissionError("Downloads are disabled.")
