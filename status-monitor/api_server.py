#!/usr/bin/env python3
"""
Cognitive Monitor API 代理服务 v1.0
提供安全的认知负载数据查询接口，隐藏 Redis Token
"""

import json
import os
from datetime import datetime
from urllib import request
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# 配置（从环境变量读取，未设置时使用默认值）
UPSTASH_REDIS_REST_URL = os.environ.get(
    'UPSTASH_REDIS_REST_URL', 
    'https://singular-snake-71209.upstash.io'
)
UPSTASH_REDIS_REST_TOKEN = os.environ.get(
    'UPSTASH_REDIS_REST_TOKEN',
    'gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk'
)
API_PORT = int(os.environ.get('COGNITIVE_API_PORT', '8080'))

def fetch_from_redis(key='cognitive.json'):
    """从 Redis 获取数据"""
    try:
        url = f"{UPSTASH_REDIS_REST_URL}/get/{key}"
        req = request.Request(
            url,
            headers={'Authorization': f'Bearer {UPSTASH_REDIS_REST_TOKEN}'},
            method='GET'
        )
        with request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get('result'):
                    return json.loads(json.loads(data['result'])['value'])
    except Exception as e:
        print(f"[ERROR] Redis fetch failed: {e}")
    return None

class APIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {self.client_address[0]} - {format % args}")
    
    def do_GET(self):
        """处理 GET 请求"""
        # CORS 头
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Cache-Control': 'no-cache'
        }
        
        if self.path == '/api/status':
            # 获取认知负载状态
            data = fetch_from_redis('cognitive.json')
            if data:
                self.send_response(200)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self.send_response(503)
                for key, value in headers.items():
                    self.send_header(key, value)
                self.end_headers()
                error = {'error': 'Service Unavailable', 'message': 'Unable to fetch data from Redis'}
                self.wfile.write(json.dumps(error).encode('utf-8'))
        
        elif self.path == '/api/health':
            # 健康检查
            self.send_response(200)
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()
            health = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
            self.wfile.write(json.dumps(health).encode('utf-8'))
        
        else:
            # 404
            self.send_response(404)
            for key, value in headers.items():
                self.send_header(key, value)
            self.end_headers()
            error = {'error': 'Not Found', 'path': self.path}
            self.wfile.write(json.dumps(error).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    """启动服务器"""
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"[INFO] Cognitive Monitor API Server v1.0")
    print(f"[INFO] Listening on http://0.0.0.0:{API_PORT}")
    print(f"[INFO] Endpoints:")
    print(f"  - GET /api/status  - 获取认知负载状态")
    print(f"  - GET /api/health  - 健康检查")
    print(f"[INFO] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    run_server()
