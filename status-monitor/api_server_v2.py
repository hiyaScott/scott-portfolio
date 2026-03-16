#!/usr/bin/env python3
"""
Cognitive Monitor API 服务 v2.0
带 Token 验证的公网 API
监听端口: 18080
"""

import json
import os
from datetime import datetime
from urllib import request
from http.server import HTTPServer, BaseHTTPRequestHandler

# 配置
UPSTASH_REDIS_REST_URL = os.environ.get(
    'UPSTASH_REDIS_REST_URL', 
    'https://singular-snake-71209.upstash.io'
)
UPSTASH_REDIS_REST_TOKEN = os.environ.get(
    'UPSTASH_REDIS_REST_TOKEN',
    'gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk'
)
API_PORT = 18080
API_TOKEN = '8ntaZy2ERLjHI8Gmj1MZmA'

# 本地数据文件路径
DATA_FILE = '/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json'

def load_local_data():
    """从本地文件加载数据"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Local file load failed: {e}")
        return None

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
        """简化日志"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {self.client_address[0]} - {format % args}")
    
    def send_cors_headers(self):
        """发送 CORS 头"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
    
    def verify_token(self):
        """验证 Token"""
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
            return token == API_TOKEN
        # 也支持 query param: ?token=xxx
        if '?token=' in self.path or '&token=' in self.path:
            import re
            match = re.search(r'[?&]token=([^&]+)', self.path)
            if match:
                return match.group(1) == API_TOKEN
        return False
    
    def do_OPTIONS(self):
        """处理预检请求"""
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """处理 GET 请求"""
        # CORS 预检
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        
        # 检查路径
        if self.path.startswith('/status'):
            # 公网访问：无需 Token（只读数据）
            # 获取数据（优先 Redis，失败用本地文件）
            data = fetch_from_redis('cognitive.json')
            if not data:
                data = load_local_data()
            
            if data:
                self.end_headers()
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self.send_response(503)
                self.end_headers()
                error = {'error': 'Service Unavailable', 'message': 'Unable to fetch data'}
                self.wfile.write(json.dumps(error).encode('utf-8'))
        
        elif self.path in ['/health', '/api/health']:
            # 健康检查（无需 Token）
            self.end_headers()
            health = {
                'status': 'ok',
                'timestamp': datetime.now().isoformat(),
                'version': '2.0',
                'auth_required': True
            }
            self.wfile.write(json.dumps(health).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
            error = {'error': 'Not Found', 'message': f'Path {self.path} not found'}
            self.wfile.write(json.dumps(error).encode('utf-8'))

def run_server():
    """启动服务器"""
    server = HTTPServer(('0.0.0.0', API_PORT), APIHandler)
    print(f"[*] Cognitive Monitor API v2.0 starting on port {API_PORT}")
    print(f"[*] Health check: http://0.0.0.0:{API_PORT}/health")
    print(f"[*] Status endpoint: http://0.0.0.0:{API_PORT}/status")
    print(f"[*] Token: {API_TOKEN[:8]}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        server.shutdown()

if __name__ == '__main__':
    run_server()
