#!/usr/bin/env python3
"""Jetton Monitor API Server v2.1 - Fixed"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
from datetime import datetime

API_TOKEN = '8ntaZy2ERLjHI8Gmj1MZmA'
DATA_FILE = '/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json'
PORT = 18080

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silent
    
    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        if path == '/health':
            self.send_json_response({
                'status': 'ok',
                'version': '2.1',
                'timestamp': datetime.now().isoformat()
            })
            return
        
        if path == '/status':
            token = query.get('token', [''])[0]
            if token != API_TOKEN:
                self.send_json_response({'error': 'Unauthorized'}, 401)
                return
            
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                self.send_json_response(data)
            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)
            return
        
        self.send_json_response({'error': 'Not found'}, 404)

if __name__ == '__main__':
    print(f"[*] Jetton Monitor API v2.1 on port {PORT}")
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    server.serve_forever()
