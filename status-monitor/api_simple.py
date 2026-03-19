#!/usr/bin/env python3
"""
Cognitive Monitor API Server - Simple Version
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, '/root/.openclaw/workspace/portfolio-blog/status-monitor')
from cognitive_monitor import get_cognitive_load, determine_status

PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            try:
                load = get_cognitive_load()
                code, text, sug = determine_status(load['cognitive_score'])
                
                data = {
                    "timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
                    "cognitive_score": load['cognitive_score'],
                    "status_code": code,
                    "status_text": text,
                    "suggestion": sug,
                    "active_sessions": load['active_sessions'],
                    "pending_count": load['pending_count'],
                    "processing_count": load['processing_count'],
                    "total_tokens": load['total_tokens'],
                    "total_tokens_formatted": f"{(load['total_tokens'] // 1000)}k" if load['total_tokens'] > 1000 else str(load['total_tokens']),
                    "estimated_response": load['max_wait_sec'] if load['max_wait_sec'] > 0 else 5,
                    "estimated_response_formatted": f"{load['max_wait_sec']}s" if load['max_wait_sec'] > 0 else "Now",
                    "task_queue": [{'label': t['name'], 'status': t['status'], 'tokens': t['tokens']} for t in load['task_queue']],
                    "cpu_percent": load['system']['cpu_percent'],
                    "memory_percent": load['system']['memory_percent']
                }
                
                response = json.dumps(data, ensure_ascii=False)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(response.encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"API Server running on port {PORT}")
    server.serve_forever()
