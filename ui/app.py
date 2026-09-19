"""Minimal local consent UI. Intentionally product-like, not 'AI themed'."""
from __future__ import annotations
from http.server import BaseHTTPRequestHandler,HTTPServer
import html

CSS="""body{margin:0;background:#f4f1ea;color:#252525;font-family:Inter,system-ui,sans-serif}
main{max-width:760px;margin:64px auto;padding:0 24px}.card{background:#fff;border:1px solid #ddd7cc;border-radius:14px;padding:28px;margin:16px 0}
h1{font-size:30px;font-weight:600;margin-bottom:8px}h2{font-size:18px;font-weight:600}p,li{line-height:1.6;color:#5d5a54}
.row{display:flex;justify-content:space-between;gap:18px;padding:14px 0;border-bottom:1px solid #eee8de}
.icon{width:18px;height:18px;display:inline-block;vertical-align:-4px;margin-right:8px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}.titleline{display:flex;align-items:center;gap:8px}.webnav{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}.webnav a{display:inline-flex;align-items:center;padding:8px 10px;border:1px solid #ddd7cc;border-radius:8px;color:#292722;text-decoration:none;background:#fff}button{border:1px solid #aaa398;background:#292722;color:#fff;border-radius:8px;padding:9px 14px;cursor:pointer}
.muted{font-size:13px;color:#777269}input{accent-color:#292722}"""
HTML=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>NIMO Settings</title><style>{CSS}</style></head>
<body><main><div class="muted">NIMO / SETTINGS</div><div class="titleline"><svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4 6v5c0 5 3.5 8.5 8 10 4.5-1.5 8-5 8-10V6l-8-3Z"/></svg><h1>Privacy & data</h1></div><nav class="webnav" aria-label="NIMO areas"><a href="#permissions">Permissions</a><a href="#storage">Storage</a><a href="#web">Web</a></nav>
<p>Choose exactly what NIMO may remember or use. These settings are explicit and separate.</p>
<div class="card" id="permissions"><h2 class="titleline"><svg class="icon" viewBox="0 0 24 24"><path d="M6 4h12v16H6z"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>Permissions</h2>
<div class="row"><span>Personal memory<br><small>Store selected information in the encrypted local vault.</small></span><input type="checkbox" aria-label="Personal memory"></div>
<div class="row"><span>Conversation history<br><small>Keep conversation history for this device.</small></span><input type="checkbox" aria-label="Conversation history"></div>
<div class="row"><span>File access<br><small>Allow NIMO to inspect approved local folders.</small></span><input type="checkbox" aria-label="File access"></div>
<div class="row"><span>Screen access<br><small>Allow screen context when you explicitly enable it.</small></span><input type="checkbox" aria-label="Screen access"></div>
<div class="row"><span>Learning contribution<br><small>Allow sanitized, minimized examples to enter the learning pipeline.</small></span><input type="checkbox" aria-label="Learning contribution"></div>
<div class="row"><span>Model improvement<br><small>Separate permission from personal memory.</small></span><input type="checkbox" aria-label="Model improvement"></div></div>
<div class="card" id="storage"><h2 class="titleline"><svg class="icon" viewBox="0 0 24 24"><path d="M4 7h16v13H4z"/><path d="M7 7V4h10v3"/></svg>Storage</h2><p>Personal memory is encrypted locally. Encryption keys are kept outside the repository. Raw personal conversations and secrets are not written into NIMO-KNOWLEDGE.</p><button>Save preferences</button> <button>Review stored data</button></div>
<div class="card" id="web"><h2 class="titleline"><svg class="icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18"/></svg>Web controls</h2><p>Browser automation remains disabled until explicitly enabled and uses host and download policy boundaries.</p></div><div class="muted">Nothing is enabled by this page until the user explicitly chooses it.</div></main></body></html>"""
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path!="/": self.send_error(404); return
        body=HTML.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self,*args): pass

def serve(host="127.0.0.1",port=8765):
    HTTPServer((host,port),Handler).serve_forever()
