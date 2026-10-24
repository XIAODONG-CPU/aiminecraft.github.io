# -*- coding: utf-8 -*-
"""阿坑启动器 v2 · 宣传网站本地服务
标准库实现：正确 MIME、中文文件名下载（RFC 5987）、支持 HEAD。
用法：pythonw serve.py  → 自动打开 http://127.0.0.1:25570/
"""
import os
import sys
import webbrowser
import urllib.parse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 25570
ROOT = os.path.dirname(os.path.abspath(__file__))

EXE = "阿坑启动器v2-安装包.exe"


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".exe": "application/octet-stream",
        ".zip": "application/zip",
    }

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def version_string(self):
        return "AhKengSite/2.0"

    def end_headers(self):
        # exe 下载：强制 attachment + RFC 5987 中文文件名
        if self.path.rstrip("/").endswith(".exe") or urllib.parse.unquote(self.path).endswith(".exe"):
            fn = urllib.parse.unquote(os.path.basename(self.path))
            self.send_header("Content-Disposition",
                             "attachment; filename*=UTF-8''%s" % urllib.parse.quote(fn))
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()


def main():
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://127.0.0.1:%d/" % PORT
    print()
    print("  ==============================================")
    print("   阿坑启动器 v2 · 宣传网站")
    print("   %s" % url)
    print("   关闭本窗口即停止服务")
    print("  ==============================================")
    print()
    if "--no-open" not in sys.argv:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
