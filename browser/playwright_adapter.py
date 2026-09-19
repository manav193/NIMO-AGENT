"""Optional real Chromium adapter. Install with: pip install 'nimo-agent[browser]' and playwright install chromium."""
from __future__ import annotations
from pathlib import Path
class PlaywrightBrowser:
    def __init__(self,headless:bool=True,download_dir:str|None=None):
        from playwright.sync_api import sync_playwright
        self._pw=sync_playwright().start()
        self._browser=self._pw.chromium.launch(headless=headless)
        self._context=self._browser.new_context(accept_downloads=download_dir is not None)
        self._page=self._context.new_page()
        self._download_dir=Path(download_dir).resolve() if download_dir else None
    def open(self,url): self._page.goto(url,wait_until="domcontentloaded"); return self._page.url
    def page_text(self,max_chars=100000): return self._page.locator("body").inner_text(timeout=10000)[:max_chars]
    def screenshot(self,path:str|None=None)->bytes:
        data=self._page.screenshot(path=path,full_page=False)
        return data
    def click(self,selector): self._page.locator(selector).click(timeout=10000)
    def fill(self,selector,text): self._page.locator(selector).fill(text,timeout=10000)
    def select(self,selector,value): self._page.locator(selector).select_option(value,timeout=10000)
    def press(self,selector,key): self._page.locator(selector).press(key,timeout=10000)
    def upload(self,selector,path):
        self._page.locator(selector).set_input_files(str(Path(path).resolve()),timeout=10000)
    def download(self,url):
        with self._page.expect_download(timeout=15000) as info: self._page.goto(url,wait_until="domcontentloaded")
        download=info.value
        if not self._download_dir: raise PermissionError("Download directory is not configured.")
        self._download_dir.mkdir(parents=True,exist_ok=True)
        target=self._download_dir/download.suggested_filename
        download.save_as(str(target)); return str(target)
    def close(self):
        self._context.close(); self._browser.close(); self._pw.stop()
