"""Web cục bộ cho hai luồng lập lịch tuần và cập nhật phòng."""
import argparse
import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from agent import weekly_review
from ai import MODEL_PROVIDER
from tools import weeks

WEB = Path(__file__).resolve().parents[1] / "frontend" / "dist"


class Handler(BaseHTTPRequestHandler):
    def send(self, code, content, mime):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, code, obj):
        self.send(code, json.dumps(obj, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/weeks":
            self.send_json(200, {"weeks": sorted(weeks()), "mode": MODEL_PROVIDER})
            return
        if path == "/" and not (WEB / "index.html").is_file():
            self.send(503, b"Build the frontend first: npm --prefix starter-repo/frontend ci, then npm --prefix starter-repo/frontend run build.",
                      "text/plain; charset=utf-8")
            return
        asset = (WEB / ("index.html" if path == "/" else path.removeprefix("/"))).resolve()
        if not asset.is_relative_to(WEB) or not asset.is_file():
            self.send_error(404)
            return
        mime = mimetypes.guess_type(asset)[0] or "application/octet-stream"
        self.send(200, asset.read_bytes(), mime)

    def do_POST(self):
        if self.path not in {"/api/review", "/api/propose", "/api/approve"}:
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16000 or self.headers.get_content_type() != "application/json":
                raise ValueError("Cần bản nháp JSON hợp lệ.")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict) or not isinstance(data.get("week"), str):
                raise ValueError("Chọn tuần cần rà.")
            result = weekly_review(data["week"], data.get("changes", {}), data.get("update", ""),
                                   propose=self.path == "/api/propose")
            if self.path == "/api/approve":
                if result["issues"]:
                    self.send_json(409, {"error": "Còn lỗi chặn duyệt. Rà lại bản nháp."})
                    return
                self.send_json(200, {"approved": True, "week": data["week"], "rows": result["rows"],
                                     "notice": result["notice"]})
            else:
                self.send_json(200, result)
        except ValueError as error:
            self.send_json(400, {"error": str(error)})
        except Exception as error:
            self.log_error("Workflow failed: %s", type(error).__name__)
            self.send_json(502, {"error": "Tác vụ chưa hoàn tất. Kiểm tra cấu hình model rồi thử lại."})


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Demo lịch tuần")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8765")))
    args = parser.parse_args()
    with HTTPServer((args.host, args.port), Handler) as server:
        print(f"http://127.0.0.1:{args.port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
