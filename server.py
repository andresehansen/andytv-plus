import http.server
import json
import os
import re
import socketserver
import urllib.parse
import urllib.request

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def resolve_dynamic_m3u8(raw_url, referer=""):
    """Extrae el flujo HLS (.m3u8) desde el reproductor web sin páginas intermedias."""
    ref = referer.strip() if referer else "https://www.anibaltv.net/"
    req1 = urllib.request.Request(raw_url, headers={"User-Agent": CHROME_UA, "Referer": ref})
    html1 = urllib.request.urlopen(req1, timeout=6).read().decode("utf-8", errors="ignore")

    # Si es puente con /embed2/, seguir hacia el embed directo
    if "/embed2/" not in raw_url:
        m_embed = re.search(r"https?://[^\s\"'<>]*/embed2/[^\s\"'<>]+", html1, re.I)
        if m_embed:
            raw_url = m_embed.group(0).replace("&amp;", "&")
            req1 = urllib.request.Request(raw_url, headers={"User-Agent": CHROME_UA, "Referer": ref})
            html1 = urllib.request.urlopen(req1, timeout=6).read().decode("utf-8", errors="ignore")

    m_stream = re.search(r"https?://[^\s\"'<>]+/stream\.php\?[^\s\"'<>]+", html1, re.I)
    if not m_stream:
        return None
    stream_url = m_stream.group(0).replace("&amp;", "&")

    req2 = urllib.request.Request(stream_url, headers={"User-Agent": CHROME_UA, "Referer": raw_url})
    html2 = urllib.request.urlopen(req2, timeout=6).read().decode("utf-8", errors="ignore")

    m_m3u8 = re.search(r"https?://[^\s\"'<>]+\.m3u8\?token=[^\s\"'<>]+", html2, re.I)
    if not m_m3u8:
        m_m3u8 = re.search(r"[\"'](https?://[^\s\"']+\.m3u8[^\s\"']*)[\"']", html2, re.I)
        return m_m3u8.group(1) if m_m3u8 else None
    return m_m3u8.group(0)


class AndyTVHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/resolve":
            params = urllib.parse.parse_qs(parsed.query)
            target_url = params.get("url", [""])[0]
            referer = params.get("referer", [""])[0]
            try:
                m3u8 = resolve_dynamic_m3u8(target_url, referer) if target_url else None
                body = json.dumps({"ok": bool(m3u8), "m3u8": m3u8}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
            except Exception as exc:
                body = json.dumps({"ok": False, "error": str(exc)}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
            return
        super().do_GET()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), AndyTVHandler) as httpd:
        print(f"AndyTV Plus local server running on http://localhost:{PORT}/")
        httpd.serve_forever()
