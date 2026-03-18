#!/usr/bin/env python3
"""Simple API server using only standard library"""
import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import time

API_TOKEN = '8ntaZy2ERLjHI8Gmj1MZmA'
DATA_FILE = '/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json'
API_PORT = 18080

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        # CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        if path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'ok', 'version': '2.0', 'auth_required': True}
            self.wfile.write(json.dumps(response).encode())
            return
        
        if path == '/status':
            # Check token
            token = query.get('token', [''])[0]
            if token != API_TOKEN:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
                return
            
            # Load data
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
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
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

def run_server():
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"[*] API Server starting on port {API_PORT}")
    print(f"[*] Health: http://0.0.0.0:{API_PORT}/health")
    print(f"[*] Status: http://0.0.0.0:{API_PORT}/status")
    server.serve_forever()

if __name__ == '__main__':
    run_server()
