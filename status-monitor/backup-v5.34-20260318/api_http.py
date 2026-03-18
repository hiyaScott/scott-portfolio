#!/usr/bin/env python3
"""API Server using http.server module"""
import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import socketserver

API_TOKEN = '8ntaZy2ERLjHI8Gmj1MZmA'
DATA_FILE = '/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json'
PORT = 18080

class APIHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silent
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            return
        
        if self.path.startswith('/status'):
            # Parse query string
            from urllib.parse import parse_qs, urlparse
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            token = query.get('token', [''])[0]
            
            if token != API_TOKEN:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
                return
            
            try:
                with open(DATA_FILE, 'r') as f:
                    data = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
            return
        
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())

if __name__ == '__main__':
    with socketserver.TCPServer(("0.0.0.0", PORT), APIHandler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()
