"""Local workbook-backed API and static frontend. No external messages are sent."""
import argparse
import json
import mimetypes
import os
from pathlib import Path
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

from agent import weekly_review, assistant
from ai import model_status
from tools import dataset, fingerprint, weeks, create_update
import store
import tracing

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'frontend/dist'
WORKFLOW_LOCK = threading.RLock()


class LocalServer(ThreadingHTTPServer):
    allow_reuse_address = False


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        try:
            super().log_message(fmt, *args)
        except OSError:
            # A Windows launcher may close its stderr while the process serves.
            pass

    def send(self, code, content, mime):
        self.send_response(code)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, code, obj):
        self.send(code, json.dumps(obj, ensure_ascii=False).encode(), 'application/json; charset=utf-8')

    def do_GET(self):
        path = urlsplit(self.path).path
        try:
            if path == '/api/health':
                self.send_json(200, {'status': 'ok', 'ai': model_status()})
            elif path == '/api/weeks':
                self.send_json(200, {'weeks': sorted(weeks()), 'mode': model_status()['provider'],
                                     'ai': model_status(), 'dataset': dataset()['metadata']})
            elif path == '/api/data':
                data = dataset()
                self.send_json(200, {'metadata': data['metadata'], 'requests': data['requests'], 'workload': data['workload']})
            elif path == '/api/draft':
                week = parse_qs(urlsplit(self.path).query).get('week', [''])[0]
                if week not in weeks():
                    raise ValueError('Tuần không hợp lệ.')
                self.send_json(200, {'draft': store.get('draft', store.draft_key(week, fingerprint()))})
            else:
                asset = (WEB / ('index.html' if path == '/' else path.removeprefix('/'))).resolve()
                if not asset.is_relative_to(WEB.resolve()) or not asset.is_file():
                    self.send_error(404)
                    return
                self.send(200, asset.read_bytes(), mimetypes.guess_type(str(asset))[0] or 'application/octet-stream')
        except ValueError as error:
            self.send_json(400, {'error': str(error)})
        except Exception:
            self.send_json(503, {'error': 'Không đọc được dữ liệu Excel. Kiểm tra file nguồn và khởi động lại backend.'})

    def do_POST(self):
        path = urlsplit(self.path).path
        allowed = {'/api/review', '/api/propose', '/api/approve', '/api/updates', '/api/assistant',
                   '/api/reload', '/api/publish', '/api/reset'}
        if path not in allowed:
            self.send_error(404)
            return
        origin = self.headers.get('Origin')
        if origin and urlsplit(origin).hostname not in {urlsplit('http://' + self.headers.get('Host', '')).hostname, '127.0.0.1', 'localhost'}:
            self.send_json(403, {'error': 'Yêu cầu phải đến từ website cùng máy chủ.'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 500_000 or self.headers.get_content_type() != 'application/json':
                raise ValueError('Cần JSON hợp lệ, tối đa 500 KB.')
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError('Nội dung phải là đối tượng JSON.')
            with WORKFLOW_LOCK:
                if path == '/api/reload':
                    data = dataset(force=True)
                    self.send_json(200, {'metadata': data['metadata']})
                    return
                week = data.get('week')
                if week not in weeks():
                    raise ValueError('Chọn tuần có trong workbook.')
                if path == '/api/updates':
                    self.send_json(201, create_update(data))
                    return
                if path == '/api/reset':
                    saved = store.save_draft({'week': week, 'changes': {}, 'update': ''}, fingerprint())
                    self.send_json(200, saved)
                    return
                if path == '/api/publish':
                    saved = store.get('handoff', store.draft_key(week, fingerprint()))
                    if not saved or data.get('approved_at') != saved['approved_at']:
                        raise ValueError('Cần bản bàn giao đã duyệt còn hiệu lực.')
                    current = store.get('draft', store.draft_key(week, fingerprint()))
                    if current and current.get('saved_at', '') > saved['approved_at']:
                        raise ValueError('Bản nháp đã thay đổi sau khi duyệt; cần duyệt lại.')
                    checked = weekly_review(week, current.get('changes', {}) if current else {}, current.get('update', '') if current else '')
                    if checked['issues'] or checked['rows'] != saved['rows']:
                        raise ValueError('Lịch hoặc cập nhật phòng đã thay đổi; cần rà soát và duyệt lại trước khi ghi nhận thông báo.')
                    saved['published_at'] = store.stamp()
                    store.put('published', store.draft_key(week, fingerprint()), saved)
                    self.send_json(200, {'published_at': saved['published_at']})
                    return
                changes, update = data.get('changes', {}), data.get('update', '')
                if not isinstance(update, str):
                    raise ValueError('Mã cập nhật phải là chuỗi.')
                tracing.begin(path + ':' + week)
                try:
                    if path == '/api/assistant':
                        result = assistant(week, changes, data.get('question', ''))
                    else:
                        result = weekly_review(week, changes, update, propose=path == '/api/propose')
                finally:
                    summary, events = tracing.end()
                    store.put('trace', store.stamp(), {'summary': summary, 'events': events})
                result['trace'] = summary
                if path == '/api/approve':
                    if result['issues']:
                        self.send_json(409, {'error': 'Còn vấn đề chưa xử lý; chưa thể duyệt lịch.', 'issues': result['issues']})
                        return
                    store.save_draft({'week': week, 'changes': changes, 'update': update}, fingerprint())
                    result = store.handoff(week, result['rows'], result['notice'], fingerprint())
                elif path == '/api/review':
                    result['saved_at'] = store.save_draft({'week': week, 'changes': changes, 'update': update}, fingerprint())['saved_at']
                self.send_json(200, result)
        except (ValueError, TypeError, KeyError) as error:
            self.send_json(400, {'error': str(error)[:500]})
        except RuntimeError as error:
            self.send_json(502, {'error': str(error)[:500]})
        except Exception as error:
            self.log_error('Workflow failed: %s', type(error).__name__)
            self.send_json(500, {'error': 'Tác vụ chưa hoàn tất. Kiểm tra dữ liệu và cấu hình backend.'})


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Điều phối lịch từ hai workbook Excel')
    parser.add_argument('--host', default=os.environ.get('HOST', '127.0.0.1'))
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', '8765')))
    args = parser.parse_args()
    try:
        data = dataset()
        print(f'Excel: {data["metadata"]["sessions"]} bản ghi buổi/phòng, {len(data["weeks"])} tuần, 2 workbook.', flush=True)
    except ValueError as error:
        print('Dữ liệu chưa sẵn sàng:', error, flush=True)
    print('AI:', model_status()['message'], flush=True)
    with LocalServer((args.host, args.port), Handler) as server:
        print(f'http://127.0.0.1:{args.port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
