#!/usr/bin/env python3
"""Serve the reviewer on localhost and persist feedback outside the public root."""
import argparse
import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    def feedback_file(self):
        # Each trial keeps its own feedback file; the original trial keeps the default path.
        trial = parse_qs(urlsplit(self.path).query).get('trial', [''])[0]
        if not trial:
            return self.server.feedback
        if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,80}', trial):
            raise ValueError('Invalid trial name')
        return self.server.feedback.with_name(f'feedback.{trial}.local.json')

    def do_GET(self):
        if urlsplit(self.path).path == '/api/feedback':
            try:
                path = self.feedback_file()
                data = json.loads(path.read_text()) if path.exists() else None
                self.json_response(200, data)
            except (OSError, ValueError):
                self.json_response(500, {'error': 'Could not read saved feedback'})
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != '/api/feedback':
            self.json_response(404, {'error': 'Not found'})
            return
        origin = self.headers.get('Origin')
        expected = 'http://' + self.headers.get('Host', '')
        if origin != expected or self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
            self.json_response(403, {'error': 'Use the local review page'})
            return
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 2_000_000:
                raise ValueError('Invalid feedback size')
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict) or data.get('schema') != 1 or not isinstance(data.get('annotations'), list) or not isinstance(data.get('ratings'), dict):
                raise ValueError('Invalid feedback format')
            path = self.feedback_file()
            tmp = path.with_suffix('.tmp')
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
            os.replace(tmp, path)
            self.json_response(200, {'saved': True})
        except (ValueError, OSError) as exc:
            self.json_response(400, {'error': str(exc)})

    def json_response(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8767)
    parser.add_argument('--feedback', type=Path, default=ROOT / 'feedback.local.json')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, directory=str(ROOT / 'web')))
    server.feedback = args.feedback.resolve()
    print(f'Review: http://127.0.0.1:{server.server_port}', flush=True)
    server.serve_forever()
