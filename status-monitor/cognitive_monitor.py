#!/usr/bin/env python3
"""
Shrimp Jetton 认知负载监控 v5.8 - 智能标签
修复：显示8字以内中文标签，描述正在做的事情
"""

import json
import os
import time
import glob
import psutil
import re
from datetime import datetime
from urllib import request

UPSTASH_REDIS_REST_URL = "https://singular-snake-71209.upstash.io"
UPSTASH_REDIS_REST_TOKEN = "gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk"
WORKSPACE = "/root/.openclaw/agents/main/sessions"

# 关键词到标签的映射
KEYWORD_TAGS = {
    '监控': '系统监控',
    '状态': '系统监控', 
    '负载': '系统监控',
    ' cognitive': '系统监控',
    'redis': '系统监控',
    '战棋': '战棋研究',
    'srpg': '战棋研究',
    '梦幻模拟战': '战棋数据',
    '天地劫': '战棋数据',
    '铃兰之剑': '战棋数据',
    '数据库': '数据整理',
    '数据收集': '数据整理',
    '技能': '战棋研究',
    '英雄': '战棋数据',
    '游戏设计': '游戏设计',
    'gdd': '游戏设计',
    '关卡': '关卡设计',
    '数值': '数值设计',
    'godot': '游戏开发',
    '象棋': '象棋游戏',
    '编钟': '编钟模拟',
    '音频': '音频设计',
    'wwise': '音频设计',
    '文档': '文档整理',
    '飞书': '飞书集成',
    'github': '代码提交',
    'git': '代码提交',
    'push': '代码提交',
    '测试': 'QA测试',
    'qa': 'QA测试',
    'bug': 'Bug修复',
    '修复': 'Bug修复',
    '部署': '系统部署',
    '定时任务': '任务调度',
    'cron': '任务调度',
}

def get_system_metrics():
    """获取系统指标"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        return {
            'cpu_percent': round(cpu_percent, 1),
            'memory_percent': round(memory.percent, 1),
            'memory_used_gb': round(memory.used / (1024**3), 2),
            'memory_total_gb': round(memory.total / (1024**3), 2)
        }
    except:
        return {'cpu_percent': 0, 'memory_percent': 0, 'memory_used_gb': 0, 'memory_total_gb': 0}

def get_session_files():
    pattern = os.path.join(WORKSPACE, "*.jsonl")
    files = glob.glob(pattern)
    sessions = []
    for f in files:
        try:
            stat = os.stat(f)
            if time.time() - stat.st_mtime < 600:
                sessions.append({'file': f, 'name': os.path.basename(f), 'mtime': stat.st_mtime})
        except:
            pass
    return sessions

def extract_task_label(content):
    """从内容中提取8字以内标签"""
    content_lower = content.lower()
    
    # 1. 先检查关键词映射
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in content_lower:
            return tag[:8]
    
    # 2. 检测后台任务
    if 'sessions_spawn' in content:
        # 提取任务描述
        match = re.search(r'"task"\s*:\s*"([^"]{5,50})', content)
        if match:
            task = match.group(1).strip()
            # 提取前8个字或关键词
            if len(task) <= 8:
                return task
            # 尝试提取核心动词+名词
            task_lower = task.lower()
            for keyword, tag in KEYWORD_TAGS.items():
                if keyword in task_lower:
                    return tag[:8]
            # 默认取前8字
            return task[:8]
    
    # 3. 检测工具调用类型
    if 'feishu_doc' in content or 'feishu_wiki' in content:
        return '飞书文档'
    if 'feishu_bitable' in content:
        return '飞书表格'
    if 'feishu_drive' in content:
        return '飞书云盘'
    if 'web_search' in content or 'kimi_search' in content:
        return '信息检索'
    if 'web_fetch' in content:
        return '网页抓取'
    if 'read' in content or 'write' in content:
        return '文件操作'
    if 'exec' in content:
        return '命令执行'
    if 'browser' in content:
        return '浏览器操作'
    if 'github' in content or 'git ' in content:
        return '代码提交'
    
    # 4. 检测消息内容主题
    if '计策' in content or '策略' in content:
        return '计策设计'
    if '角色' in content and '技能' in content:
        return '技能设计'
    if '关卡' in content:
        return '关卡设计'
    if '数值' in content:
        return '数值设计'
    if '剧情' in content or '故事' in content:
        return '剧情设计'
    if 'ui' in content_lower or '界面' in content:
        return 'UI设计'
    if '音效' in content or '音乐' in content:
        return '音频设计'
    
    return None

def analyze_session(file_path):
    """分析会话 - v5.8: 智能标签"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_tokens = 0
        tool_calls = 0
        messages = 0
        last_user_time = 0
        last_assistant_time = 0
        
        label = None
        has_recent_thinking = False
        is_group = False
        
        for line in lines[-50:]:  # 只检查最近50条
            try:
                msg = json.loads(line.strip())
                if msg.get('type') == 'message':
                    msg_data = msg.get('message', {})
                    content = str(msg_data.get('content', ''))
                    role = msg_data.get('role', '')
                    timestamp = msg.get('timestamp', '')
                    
                    total_tokens += len(content) // 4
                    messages += 1
                    
                    # 提取标签（从最近的消息中）
                    if label is None:
                        extracted = extract_task_label(content)
                        if extracted:
                            label = extracted
                    
                    # 记录用户消息时间
                    if role == 'user':
                        last_user_time = timestamp
                        # 检测是否群聊
                        if 'group_subject' in content or '"is_group_chat": true' in content.lower():
                            is_group = True
                    
                    # 记录助手消息时间
                    elif role == 'assistant':
                        content_list = msg_data.get('content', [])
                        is_thinking_only = True
                        if isinstance(content_list, list):
                            for item in content_list:
                                if isinstance(item, dict) and item.get('type') != 'thinking':
                                    is_thinking_only = False
                                    break
                                if isinstance(item, dict) and item.get('type') == 'thinking':
                                    has_recent_thinking = True
                        
                        if not is_thinking_only:
                            last_assistant_time = timestamp
                    
                    # 检测工具调用
                    if '"toolCallId"' in content:
                        tool_calls += 1
                        
            except:
                pass
        
        # 确定会话类型和标签
        if label:
            session_type = "🤖" if 'sessions_spawn' in str(lines[-30:]) else ("👥" if is_group else "💬")
            session_name = label[:8]
        elif is_group:
            session_type = "👥"
            session_name = "群聊"
        else:
            session_type = "💬"
            session_name = "私聊"
        
        # 状态判断
        file_mtime = os.path.getmtime(file_path)
        last_activity = time.time() - file_mtime
        
        # 解析时间戳
        try:
            user_ts = datetime.fromisoformat(last_user_time.replace('Z', '+00:00')).timestamp() if last_user_time else 0
            assistant_ts = datetime.fromisoformat(last_assistant_time.replace('Z', '+00:00')).timestamp() if last_assistant_time else 0
        except:
            user_ts = assistant_ts = 0
        
        # 三种状态判断
        is_waiting = False
        is_processing = False
        wait_time = 0
        
        if user_ts > assistant_ts:
            is_waiting = True
            wait_time = int(time.time() - user_ts)
        elif last_activity < 30 and has_recent_thinking:
            is_processing = True
        
        return {
            'messages': messages,
            'estimated_tokens': total_tokens,
            'tool_calls': tool_calls,
            'is_waiting': is_waiting,
            'is_processing': is_processing,
            'wait_time': max(0, wait_time),
            'last_mtime': file_mtime,
            'session_type': session_type,
            'session_name': session_name,
            'full_type': f"{session_type} {session_name}"
        }
    except Exception as e:
        print(f"[analyze_session error] {e}")
        return {'messages': 0, 'estimated_tokens': 0, 'tool_calls': 0, 
                'is_waiting': False, 'is_processing': False, 'wait_time': 0, 'last_mtime': 0,
                'session_type': "💭", 'session_name': "未知", 'full_type': "💭 未知"}

def get_cognitive_load():
    sessions = get_session_files()
    
    if not sessions:
        return {
            'active_sessions': 0, 'pending_count': 0, 'processing_count': 0, 'max_wait_sec': 0,
            'total_tokens': 0, 'last_active_sec': 999, 'task_queue': [], 'cognitive_score': 0
        }
    
    total_tokens = 0
    pending_count = 0
    processing_count = 0
    max_wait = 0
    recent_mtime = 0
    details = []
    
    for sess in sessions:
        a = analyze_session(sess['file'])
        total_tokens += a['estimated_tokens']
        recent_mtime = max(recent_mtime, a['last_mtime'])
        
        if a['is_waiting']:
            pending_count += 1
            max_wait = max(max_wait, a['wait_time'])
        elif a['is_processing']:
            processing_count += 1
        
        # 状态显示
        if a['is_waiting']:
            if a['wait_time'] > 120:
                status = f"🔴 等待{a['wait_time']//60}分钟"
            elif a['wait_time'] > 60:
                status = f"🟡 等待{a['wait_time']//60}分钟"
            else:
                status = f"⏳ 等待{a['wait_time']}秒"
        elif a['is_processing']:
            status = "🔄 处理中"
        else:
            status = "✅ 已回复"
        
        details.append({
            'name': a['full_type'],
            'status': status,
            'tokens': a['estimated_tokens']
        })
    
    last_active = int(time.time() - recent_mtime) if recent_mtime > 0 else 999
    
    # 评分
    if pending_count > 0:
        if max_wait < 30:
            score = 30
        elif max_wait < 90:
            score = 55
        elif max_wait < 180:
            score = 80
        else:
            score = 95
    elif processing_count > 0:
        score = 60
    else:
        score = 10
    
    return {
        'active_sessions': len(sessions),
        'pending_count': pending_count,
        'processing_count': processing_count,
        'max_wait_sec': max_wait,
        'total_tokens': total_tokens,
        'last_active_sec': last_active,
        'task_queue': details,
        'cognitive_score': score,
        'system': get_system_metrics()
    }

def determine_status(score):
    if score >= 80:
        return "high", "🔴 高负载", "正在处理中，建议稍后"
    elif score >= 55:
        return "medium", "🟡 中等负载", "正在处理，可派简单任务"
    elif score >= 30:
        return "medium", "🟡 轻负载", "30秒内响应"
    else:
        return "low", "🟢 空闲", "可立即响应"

def update_redis(data):
    try:
        url = f"{UPSTASH_REDIS_REST_URL}/set/cognitive.json"
        req = request.Request(
            url,
            data=json.dumps({"value": json.dumps(data)}).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {UPSTASH_REDIS_REST_TOKEN}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except:
        return False

def main():
    print("🧠 Shrimp Jetton v5.8 - 智能标签")
    while True:
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
                "max_wait_sec": load['max_wait_sec'],
                "total_tokens": load['total_tokens'],
                "last_active_sec": load['last_active_sec'],
                "task_queue": load['task_queue'],
                "cpu_percent": load['system']['cpu_percent'],
                "memory_percent": load['system']['memory_percent']
            }
            
            if update_redis(data):
                ts = datetime.now().strftime("%H:%M:%S")
                tasks = ", ".join([d['name'] for d in load['task_queue'][:2]])
                print(f"[{ts}] {text} | {tasks}")
        except Exception as e:
            print(f"[ERR] {e}")
        
        time.sleep(15)

if __name__ == "__main__":
    main()
