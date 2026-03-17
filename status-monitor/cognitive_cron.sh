#!/bin/bash
# Cognitive Monitor 定时任务脚本 v5.33
# 由crontab每分钟调用，生成数据文件

cd /root/.openclaw/workspace/portfolio-blog/status-monitor || exit 1

python3 << 'PYTHON'
import sys
sys.path.insert(0, '.')
from cognitive_monitor import get_cognitive_load, determine_status
import json
from datetime import datetime

try:
    load = get_cognitive_load()
    code, text, sug = determine_status(load['cognitive_score'])
    
    data = {
        "timestamp": datetime.now().isoformat(),
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
        "total_tokens_formatted": f"{load['total_tokens']//1000}k" if load['total_tokens'] > 1000 else str(load['total_tokens']),
        "estimated_response": load['max_wait_sec'] if load['max_wait_sec'] > 0 else 5,
        "estimated_response_formatted": f"{load['max_wait_sec']}s" if load['max_wait_sec'] > 0 else "Now",
        "last_active_sec": load['last_active_sec'],
        "task_queue": [{'label': t['name'], 'status': t['status'], 'tokens': t['tokens']} for t in load['task_queue']],
        "cpu_percent": load['system']['cpu_percent'],
        "memory_percent": load['system']['memory_percent'],
        "workflow_details": load['workflow_details'],
        "build_details": load['build_details']
    }
    
    with open('cognitive-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 数据已更新 score={data['cognitive_score']}%")
except Exception as e:
    print(f"[ERR] {e}")
PYTHON
