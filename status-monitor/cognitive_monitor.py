#!/usr/bin/env python3
"""
Shrimp Jetton 认知负载监控 v5.6 - 添加"处理中"状态
修复：正确识别"正在处理任务"vs"已回复完成"
"""

import json
import os
import time
import glob
import psutil
from datetime import datetime
from urllib import request

UPSTASH_REDIS_REST_URL = "https://singular-snake-71209.upstash.io"
UPSTASH_REDIS_REST_TOKEN = "gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk"
WORKSPACE = "/root/.openclaw/agents/main/sessions"

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

def analyze_session(file_path):
    """分析会话 - v5.6: 区分等待中/处理中/已回复"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_tokens = 0
        tool_calls = 0
        messages = 0
        last_user_time = 0
        last_assistant_time = 0
        
        has_group = False
        has_private = False
        has_subagent = False
        has_recent_thinking = False
        
        for line in lines[-100:]:
            try:
                msg = json.loads(line.strip())
                if msg.get('type') == 'message':
                    msg_data = msg.get('message', {})
                    content = str(msg_data.get('content', ''))
                    role = msg_data.get('role', '')
                    timestamp = msg.get('timestamp', '')
                    
                    total_tokens += len(content) // 4
                    messages += 1
                    
                    # 记录用户消息时间
                    if role == 'user':
                        last_user_time = timestamp
                        # 识别类型
                        if 'Feishu' in content:
                            if 'group' in content.lower():
                                has_group = True
                            elif 'user' in content.lower():
                                has_private = True
                        if '"name": "sessions_spawn"' in content:
                            has_subagent = True
                    
                    # 记录助手消息时间（排除纯thinking消息）
                    elif role == 'assistant':
                        content_list = msg_data.get('content', [])
                        is_thinking_only = True
                        if isinstance(content_list, list):
                            for item in content_list:
                                if isinstance(item, dict) and item.get('type') != 'thinking':
                                    is_thinking_only = False
                                    break
                        
                        if not is_thinking_only:
                            last_assistant_time = timestamp
                        
                        # 检测是否有thinking消息（表示正在处理）
                        if isinstance(content_list, list):
                            for item in content_list:
                                if isinstance(item, dict) and item.get('type') == 'thinking':
                                    has_recent_thinking = True
                                    break
                    
                    # 检测工具调用
                    if '"toolCallId"' in content or '"name": "' in content:
                        tool_calls += 1
                        
            except:
                pass
        
        # 确定类型
        if has_subagent:
            session_type = "🤖 后台任务"
        elif has_group:
            session_type = "👥 群聊对话"
        elif has_private:
            session_type = "💬 私聊对话"
        else:
            session_type = "💭 一般对话"
        
        # 状态判断
        file_mtime = os.path.getmtime(file_path)
        last_activity = time.time() - file_mtime
        
        # 解析时间戳
        try:
            from datetime import datetime
            user_ts = datetime.fromisoformat(last_user_time.replace('Z', '+00:00')).timestamp() if last_user_time else 0
            assistant_ts = datetime.fromisoformat(last_assistant_time.replace('Z', '+00:00')).timestamp() if last_assistant_time else 0
        except:
            user_ts = assistant_ts = 0
        
        # 三种状态判断
        is_waiting = False
        is_processing = False
        wait_time = 0
        
        if user_ts > assistant_ts:
            # 用户消息更新 - 等待回复
            is_waiting = True
            wait_time = int(time.time() - user_ts)
        elif last_activity < 30 and has_recent_thinking:
            # 文件最近30秒内有更新，且有 thinking - 正在处理
            is_processing = True
        # 否则：已回复完成
        
        return {
            'messages': messages,
            'estimated_tokens': total_tokens,
            'tool_calls': tool_calls,
            'is_waiting': is_waiting,
            'is_processing': is_processing,
            'wait_time': max(0, wait_time),
            'last_mtime': file_mtime,
            'session_type': session_type
        }
    except Exception as e:
        print(f"[analyze_session error] {e}")
        return {'messages': 0, 'estimated_tokens': 0, 'tool_calls': 0, 
                'is_waiting': False, 'is_processing': False, 'wait_time': 0, 'last_mtime': 0,
                'session_type': "💭 一般对话"}

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
            'name': a['session_type'],
            'status': status,
            'tokens': a['estimated_tokens']
        })
    
    last_active = int(time.time() - recent_mtime) if recent_mtime > 0 else 999
    
    # 评分：处理中也计入负载
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
        score = 60  # 有任务在处理
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
    print("🧠 Shrimp Jetton v5.6 - 处理中状态检测")
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
                tasks = ", ".join([d['name'].split()[1] for d in load['task_queue'][:3]])
                print(f"[{ts}] {text} | 处理:{load['processing_count']} | 等待:{load['pending_count']} | CPU:{load['system']['cpu_percent']}%")
        except Exception as e:
            print(f"[ERR] {e}")
        
        time.sleep(30)

if __name__ == "__main__":
    main()
