#!/usr/bin/env python3
"""Servidor local que imita las URLs limpias de Cloudflare Pages (/salud -> salud.html).

Uso: python3 scripts/dev_server.py [puerto] [carpeta]
"""
import http.server
import os
import sys
from functools import partial

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8440
ROOT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        if path != "/" and not os.path.splitext(path)[1]:
            candidate = os.path.join(self.directory, path.strip("/") + ".html")
            if os.path.isfile(candidate):
                self.path = path.rstrip("/") + ".html"
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    handler = partial(Handler, directory=os.path.abspath(ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"Sirviendo {os.path.abspath(ROOT)} en http://localhost:{PORT}")
        httpd.serve_forever()
