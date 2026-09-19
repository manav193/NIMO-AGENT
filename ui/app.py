"""Minimal local consent UI. Intentionally product-like, not 'AI themed'."""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler,HTTPServer
import html

CSS="""body{margin:0;background:#f4f1ea;color:#252525;font-family:Inter,system-ui,sans-serif}
main{max-width:760px;margin:64px auto;padding:0 24px}.card{background:#fff;border:1px solid #ddd7cc;border-radius:14px;padding:28px;margin:16px 0}
h1{font-size:30px;font-weight:600;margin-bottom:8px}h2{font-size:18px;font-weight:600}p,li{line-height:1.6;color:#5d5a54}
.row{display:flex;justify-content:space-between;gap:18px;padding:14px 0;border-bottom:1px solid #eee8de}
button{border:1px solid #aaa398;background:#292722;color:#fff;border-radius:8px;padding:9px 14px;cursor:pointer}
.muted{font-size:13px;color:#777269}input{accent-color:#292722}"""
HTML=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>NIMO Settings</title><style>{CSS}</style></head>
<body><main><div class="muted">NIMO / SETTINGS</div><h1>Privacy & data</h1>
<p>Choose exactly what NIMO may remember or use. These settings are explicit and separate.</p>
<div class="card"><h2>Permissions</h2>
<div class="row"><span>Personal memory<br><small>Store selected information in the encrypted local vault.</small></span><input type="checkbox" aria-label="Personal memory"></div>
<div class="row"><span>Conversation history<br><small>Keep conversation history for this device.</small></span><input type="checkbox" aria-label="Conversation history"></div>
<div class="row"><span>File access<br><small>Allow NIMO to inspect approved local folders.</small></span><input type="checkbox" aria-label="File access"></div>
<div class="row"><span>Screen access<br><small>Allow screen context when you explicitly enable it.</small></span><input type="checkbox" aria-label="Screen access"></div>
<div class="row"><span>Learning contribution<br><small>Allow sanitized, minimized examples to enter the learning pipeline.</small></span><input type="checkbox" aria-label="Learning contribution"></div>
<div class="row"><span>Model improvement<br><small>Separate permission from personal memory.</small></span><input type="checkbox" aria-label="Model improvement"></div></div>
<div class="card"><h2>Storage</h2><p>Personal memory is encrypted locally. Encryption keys are kept outside the repository. Raw personal conversations and secrets are not written into NIMO-KNOWLEDGE.</p><button>Save preferences</button> <button>Review stored data</button></div>
<div class="muted">Nothing is enabled by this page until the user explicitly chooses it.</div></main></body></html>"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!="/": self.send_error(404); return
        body=HTML.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self,*args): pass

def serve(host="127.0.0.1",port=8765):
    HTTPServer((host,port),Handler).serve_forever()
