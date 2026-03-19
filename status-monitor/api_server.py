#!/usr/bin/env python3
"""
认知监控 API 服务器 v1.0
提供实时数据接口，支持 CORS，供 GitHub Pages 前端调用
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# 添加监控脚本路径
sys.path.insert(0, '/root/.openclaw/workspace/portfolio-blog/status-monitor')
from cognitive_monitor import get_cognitive_load, determine_status

# 配置
PORT = 8080
HOST = '0.0.0.0'  # 监听所有接口

class CORSRequestHandler(BaseHTTPRequestHandler):
    """支持 CORS 的 HTTP 请求处理器"""
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/status':
            self.handle_status()
        elif path == '/api/health':
            self.handle_health()
        else:
            self.send_error(404, 'Not Found')
    
    def handle_status(self):
        """返回实时认知负载状态"""
        try:
            load = get_cognitive_load()
            code, text, sug = determine_status(load['cognitive_score'])
            
            data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "cognitive_score": load['cognitive_score'],
                "status_code": code,
                "status_text": text,
                "suggestion": sug,
                "active_sessions": load['active_sessions'],
                "pending_count": load['pending_count'],
                "processing_count": load['processing_count'],
                "github_workflows": load['github_workflows'],
                "local_builds": load['local_builds'],
                "max_wait_sec": load['max_wait_sec'],
                "total_tokens": load['total_tokens'],
                "total_tokens_formatted": f"{(load['total_tokens'] // 1000)}k" if load['total_tokens'] > 1000 else str(load['total_tokens']),
                "estimated_response": load['max_wait_sec'] if load['max_wait_sec'] > 0 else 5,
                "estimated_response_formatted": f"{load['max_wait_sec']}s" if load['max_wait_sec'] > 0 else "Now",
                "last_active_sec": load['last_active_sec'],
                "task_queue": [{'label': t['name'], 'status': t['status'], 'tokens': t['tokens']} for t in load['task_queue']],
                "cpu_percent": load['system']['cpu_percent'],
                "memory_percent": load['system']['memory_percent'],
                "workflow_details": load['workflow_details'],
                "build_details": load['build_details']
            }
            
            response = json.dumps(data, ensure_ascii=False)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def handle_health(self):
        """健康检查端点"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "time": datetime.now(timezone.utc).isoformat()}).encode())
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {args[0]}")

def run_server():
    """启动服务器"""
    server = HTTPServer((HOST, PORT), CORSRequestHandler)
    print(f"🚀 认知监控 API 服务器启动")
    print(f"📡 监听: http://{HOST}:{PORT}")
    print(f"🔗 API 端点: http://{HOST}:{PORT}/api/status")
    print(f"❤️  健康检查: http://{HOST}:{PORT}/api/health")
    print(f"⏹️  按 Ctrl+C 停止")
    print("-" * 50)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  服务器已停止")
        server.shutdown()

if __name__ == '__main__':
    run_server()
