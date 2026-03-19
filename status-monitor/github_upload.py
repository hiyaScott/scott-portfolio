#!/usr/bin/env python3
"""
GitHub 文件上传工具
用于推送监控数据到独立数据仓库
"""
import base64
import json
import sys
import urllib.request
import urllib.error
import os

GITHUB_API = "https://api.github.com/repos/hiyaScott/scott-portfolio-data"

def get_file_sha(filepath, token):
    """获取文件当前SHA"""
    try:
        req = urllib.request.Request(
            f"{GITHUB_API}/contents/{filepath}",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get("sha", "")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return ""  # 文件不存在
        raise

def upload_file(filepath, message, token, repo_dir):
    """上传文件到GitHub"""
    sha = get_file_sha(filepath, token)
    
    with open(f"{repo_dir}/{filepath}", "rb") as f:
        content = base64.b64encode(f.read()).decode()
    
    payload = {
        "message": message,
        "content": content
    }
    if sha:
        payload["sha"] = sha
    
    data = json.dumps(payload).encode()
    
    req = urllib.request.Request(
        f"{GITHUB_API}/contents/{filepath}",
        data=data,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="PUT"
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        return "content" in result

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: github_upload.py <filepath> <message> <token> <repo_dir>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    message = sys.argv[2]
    token = sys.argv[3]
    repo_dir = sys.argv[4]
    
    try:
        success = upload_file(filepath, message, token, repo_dir)
        print("success" if success else "failed")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"failed: {e}")
        sys.exit(1)
