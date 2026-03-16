#!/usr/bin/env python3
"""
Shrimp Jetton 认知负载监控 v5.23.0 - GitHub CI监控 + 扩展标签系统
更新：
- 新增 GitHub Actions Workflow 监控
- 扩展标签系统覆盖更多任务类型
- 优化标签显示逻辑
"""

import json
import os
import time
import glob
import psutil
import re
import subprocess
from datetime import datetime
from urllib import request

UPSTASH_REDIS_REST_URL = "https://singular-snake-71209.upstash.io"
UPSTASH_REDIS_REST_TOKEN = "gQAAAAAAARYpAAIncDE2NmRhOGU0OWFhZWM0N2I4OGZlMGZkNGM5NjdjMTI5NnAxNzEyMDk"
WORKSPACE = "/root/.openclaw/agents/main/sessions"

# ============================================================================
# 扩展的关键词到标签映射 - v5.23
# ============================================================================
KEYWORD_TAGS = {
    # 系统监控类
    '监控': '系统监控',
    '状态': '系统监控', 
    '负载': '系统监控',
    'cognitive': '系统监控',
    'redis': '系统监控',
    'upstash': '系统监控',
    
    # SRPG/战棋研究类
    '战棋': '战棋研究',
    'srpg': '战棋研究',
    'tactics': '战棋研究',
    '梦幻模拟战': '战棋数据',
    '天地劫': '战棋数据',
    '铃兰之剑': '战棋数据',
    '三国志': '战棋数据',
    '三国': '战棋数据',
    '望神州': '战棋数据',
    '战棋版': '战棋数据',
    
    # 数据类
    '数据库': '数据整理',
    '数据收集': '数据整理',
    '数据分析': '数据整理',
    '数据': '数据处理',
    
    # 技能/角色设计
    '技能': '技能设计',
    '英雄': '角色数据',
    '角色': '角色数据',
    '英灵': '角色数据',
    '武将': '角色数据',
    '计策': '计策设计',
    '策略': '计策设计',
    
    # 游戏设计类
    '游戏设计': '游戏设计',
    'gdd': '游戏设计',
    '关卡': '关卡设计',
    '数值': '数值设计',
    '剧情': '剧情设计',
    '故事': '剧情设计',
    'ui': 'UI设计',
    '界面': 'UI设计',
    'ux': 'UX设计',
    '交互': 'UX设计',
    
    # 技术开发类
    'godot': 'Godot开发',
    '游戏引擎': '引擎开发',
    '引擎': '引擎开发',
    '导出': '游戏导出',
    '打包': '游戏导出',
    'build': '构建打包',
    '构建': '构建打包',
    '编译': '构建打包',
    
    # 游戏项目类
    '象棋': '象棋游戏',
    '中国象棋': '象棋游戏',
    '编钟': '编钟模拟',
    '乐器': '乐器模拟',
    '音频': '音频设计',
    '音效': '音频设计',
    '音乐': '音乐设计',
    'wwise': 'Wwise音频',
    'fmod': 'FMOD音频',
    
    # 版本控制/CI类
    'github': 'GitHub操作',
    'git': '代码版本',
    'push': '代码提交',
    'commit': '代码提交',
    'pr': 'PR审查',
    'pull request': 'PR审查',
    'merge': '代码合并',
    'workflow': 'CI/CD',
    'actions': 'CI/CD',
    'ci': 'CI/CD',
    'cd': 'CI/CD',
    '部署': '部署发布',
    'release': '版本发布',
    
    # 飞书/文档类
    '文档': '文档整理',
    '飞书': '飞书集成',
    'feishu': '飞书集成',
    'bitable': '飞书表格',
    'wiki': '知识库',
    
    # 测试/QA类
    '测试': 'QA测试',
    'qa': 'QA测试',
    'bug': 'Bug修复',
    '修复': 'Bug修复',
    'fix': 'Bug修复',
    'debug': '调试排查',
    '排查': '调试排查',
    
    # 定时任务/系统
    '定时任务': '任务调度',
    'cron': '任务调度',
    'heartbeat': '心跳监控',
    
    # 网络/搜索
    '搜索': '信息检索',
    '调研': '信息检索',
    '抓取': '网页抓取',
    '爬虫': '网页抓取',
    'api': 'API开发',
    
    # 前端/Web
    'html': '前端开发',
    'css': '前端开发',
    'javascript': '前端开发',
    'js': '前端开发',
    'react': '前端开发',
    'vue': '前端开发',
    '网站': '网站建设',
    '网页': '网页开发',
    
    # 后端/服务
    '后端': '后端开发',
    'server': '后端开发',
    'api': 'API开发',
    '数据库': '数据库',
    'db': '数据库',
    
    # AI/ML
    'ai': 'AI开发',
    '模型': '模型训练',
    '训练': '模型训练',
    '推理': '模型推理',
    'embedding': '向量嵌入',
    '向量': '向量检索',
    
    # 运维/DevOps
    'docker': '容器化',
    'k8s': 'K8s运维',
    'kubernetes': 'K8s运维',
    'nginx': '服务器配置',
    '服务器': '服务器运维',
    'ssl': '安全配置',
    '备份': '数据备份',
}

# GitHub 仓库监控列表
GITHUB_REPOS = [
    'hiyaScott/scott-portfolio',
    'hiyaScott/jetton-monitor',
]

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

def get_github_workflow_status():
    """获取 GitHub Actions 运行状态"""
    workflows = []
    try:
        for repo in GITHUB_REPOS:
            # 使用 gh CLI 获取最近的工作流运行
            result = subprocess.run(
                ['gh', 'run', 'list', '--repo', repo, '--limit', '5', '--json', 'databaseId,workflowName,status,conclusion,startedAt,event,headBranch'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                runs = json.loads(result.stdout)
                for run in runs:
                    # 只返回正在运行或最近完成的
                    if run.get('status') in ['in_progress', 'queued', 'waiting', 'requested']:
                        workflows.append({
                            'repo': repo.split('/')[-1],
                            'name': run.get('workflowName', 'Unknown'),
                            'status': run.get('status'),
                            'conclusion': run.get('conclusion'),
                            'branch': run.get('headBranch', 'unknown'),
                            'run_id': run.get('databaseId'),
                            'type': 'github_workflow'
                        })
    except Exception as e:
        print(f"[GitHub Workflow Error] {e}")
    
    return workflows

def get_local_build_processes():
    """检测本地构建进程"""
    builds = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                # 检测构建相关进程
                build_keywords = [
                    ('godot', 'Godot导出'),
                    ('npm run build', 'NPM构建'),
                    ('webpack', 'Webpack打包'),
                    ('vite build', 'Vite构建'),
                    ('docker build', 'Docker构建'),
                    ('docker-compose', 'Docker编排'),
                    ('python setup.py', 'Python打包'),
                    ('pytest', '测试运行'),
                    ('jest', 'Jest测试'),
                    ('mvn', 'Maven构建'),
                    ('gradle', 'Gradle构建'),
                ]
                
                for keyword, label in build_keywords:
                    if keyword in cmdline.lower():
                        builds.append({
                            'pid': proc.info['pid'],
                            'name': label,
                            'type': 'local_build'
                        })
                        break
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print(f"[Build Process Error] {e}")
    
    return builds

def get_session_files():
    pattern = os.path.join(WORKSPACE, "*.jsonl")
    files = glob.glob(pattern)
    sessions = []
    for f in files:
        try:
            stat = os.stat(f)
            if time.time() - stat.st_mtime < 600:  # 10分钟内活跃
                sessions.append({'file': f, 'name': os.path.basename(f), 'mtime': stat.st_mtime})
        except:
            pass
    return sessions

def extract_task_label(content):
    """从内容中提取标签 - v5.23 增强版"""
    content_lower = content.lower()
    
    # 1. 先检查关键词映射（最长匹配优先）
    matched_tags = []
    for keyword, tag in KEYWORD_TAGS.items():
        if keyword in content_lower:
            matched_tags.append((len(keyword), tag))
    
    if matched_tags:
        # 按关键词长度排序，取最长的匹配
        matched_tags.sort(reverse=True)
        return matched_tags[0][1][:10]
    
    # 2. 检测后台任务
    if 'sessions_spawn' in content:
        match = re.search(r'"task"\s*:\s*"([^"]{5,80})', content)
        if match:
            task = match.group(1).strip()
            task_lower = task.lower()
            for keyword, tag in KEYWORD_TAGS.items():
                if keyword in task_lower:
                    return tag[:10]
            # 提取前10个字
            return task[:10]
    
    # 3. 检测工具调用类型
    tool_tags = [
        (['feishu_doc', 'feishu_wiki'], '飞书文档'),
        (['feishu_bitable'], '飞书表格'),
        (['feishu_drive'], '飞书云盘'),
        (['web_search', 'kimi_search'], '信息检索'),
        (['web_fetch', 'kimi_fetch'], '网页抓取'),
        (['browser'], '浏览器操作'),
        (['exec', 'process'], '命令执行'),
        (['read', 'write', 'edit'], '文件操作'),
        (['github', 'gh '], 'GitHub操作'),
        (['git '], '代码版本'),
        (['cron'], '任务调度'),
        (['sessions_spawn'], '后台任务'),
        (['canvas'], '画布操作'),
        (['nodes'], '节点控制'),
        (['gateway'], '网关管理'),
        (['message'], '消息发送'),
        (['tts'], '语音合成'),
    ]
    
    for tools, tag in tool_tags:
        for tool in tools:
            if tool in content_lower:
                return tag[:10]
    
    # 4. 检测内容主题（更智能的匹配）
    topic_patterns = [
        (r'计策|策略|谋略', '计策设计'),
        (r'角色.*技能|技能.*设计', '技能设计'),
        (r'关卡.*设计|地图.*设计', '关卡设计'),
        (r'数值.*设计|数值.*平衡', '数值设计'),
        (r'剧情|故事|叙事', '剧情设计'),
        (r'ui|界面|布局', 'UI设计'),
        (r'ux|交互|体验', 'UX设计'),
        (r'音效|音乐|声音', '音频设计'),
        (r'导出|打包|构建|build', '构建打包'),
        (r'测试|qa|验证', 'QA测试'),
        (r'bug|修复|fix', 'Bug修复'),
        (r'部署|发布|release', '部署发布'),
    ]
    
    for pattern, tag in topic_patterns:
        if re.search(pattern, content_lower):
            return tag[:10]
    
    return None

def analyze_session(file_path):
    """分析会话 - v5.23: 增强标签提取"""
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
        is_spawn = False
        
        for line in lines[-80:]:  # 检查最近80条，提高准确度
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
                    
                    # 检测后台任务
                    if 'sessions_spawn' in content:
                        is_spawn = True
                    
                    # 记录用户消息时间
                    if role == 'user':
                        last_user_time = timestamp
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
                    if '"toolCallId"' in content or '"tool_calls"' in content:
                        tool_calls += 1
                        
            except:
                pass
        
        # 确定会话类型和标签
        if label:
            if is_spawn:
                session_type = "🤖"
            elif is_group:
                session_type = "👥"
            else:
                session_type = "💬"
            session_name = label[:10]
        elif is_spawn:
            session_type = "🤖"
            session_name = "后台任务"
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
    """获取认知负载 - v5.23: 添加 GitHub CI 和本地构建监控"""
    sessions = get_session_files()
    github_workflows = get_github_workflow_status()
    local_builds = get_local_build_processes()
    
    # 合并所有任务
    all_tasks = []
    
    # 1. 会话任务
    if sessions:
        total_tokens = 0
        pending_count = 0
        processing_count = 0
        max_wait = 0
        recent_mtime = 0
        
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
            
            all_tasks.append({
                'name': a['full_type'],
                'status': status,
                'tokens': a['estimated_tokens'],
                'type': 'session'
            })
    else:
        total_tokens = 0
        pending_count = 0
        processing_count = 0
        max_wait = 0
        recent_mtime = 0
    
    # 2. GitHub Workflow 任务
    for wf in github_workflows:
        status_emoji = "🔄" if wf['status'] == 'in_progress' else "⏳"
        status_text = f"{status_emoji} {wf['status']}"
        all_tasks.append({
            'name': f"🚀 CI: {wf['repo']}/{wf['name'][:15]}",
            'status': status_text,
            'tokens': 0,
            'type': 'github_workflow',
            'details': wf
        })
        # GitHub 构建也算作处理中任务
        if wf['status'] in ['in_progress', 'queued']:
            processing_count += 1
    
    # 3. 本地构建进程
    for build in local_builds:
        all_tasks.append({
            'name': f"🔨 Build: {build['name']}",
            'status': "🔄 运行中",
            'tokens': 0,
            'type': 'local_build',
            'pid': build['pid']
        })
        processing_count += 1
    
    last_active = int(time.time() - recent_mtime) if recent_mtime > 0 else 999
    
    # 评分算法 v5.23
    # 基础分 + 等待/Token评分 + GitHub构建加成
    base_score = 0
    
    # 活跃会话基础分
    if len(sessions) > 0:
        base_score += min(len(sessions) * 5, 15)
    
    # GitHub构建加成
    github_bonus = len(github_workflows) * 10
    
    # 本地构建加成
    build_bonus = len(local_builds) * 8
    
    # 等待评分
    if pending_count > 0:
        if max_wait < 30:
            wait_score = 20
        elif max_wait < 90:
            wait_score = 35
        elif max_wait < 180:
            wait_score = 50
        else:
            wait_score = 65
    else:
        wait_score = 0
    
    # Token评分（只算处理中）
    if processing_count > 0 and total_tokens > 0:
        tokens_per_task = total_tokens / processing_count
        if tokens_per_task > 100000:
            token_score = 25
        elif tokens_per_task > 50000:
            token_score = 15
        elif tokens_per_task > 10000:
            token_score = 8
        else:
            token_score = 3
    else:
        token_score = 0
    
    # 最终评分
    score = min(base_score + wait_score + token_score + github_bonus + build_bonus, 100)
    
    return {
        'active_sessions': len(sessions),
        'pending_count': pending_count,
        'processing_count': processing_count,
        'github_workflows': len(github_workflows),
        'local_builds': len(local_builds),
        'max_wait_sec': max_wait,
        'total_tokens': total_tokens,
        'last_active_sec': last_active,
        'task_queue': all_tasks,
        'cognitive_score': score,
        'system': get_system_metrics(),
        'workflow_details': github_workflows,
        'build_details': local_builds
    }

def determine_status(score):
    if score >= 80:
        return "high", "🔴 高负载", "建议等待，系统忙碌"
    elif score >= 55:
        return "medium", "🟡 中等负载", "可派简单任务"
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
    print("🧠 Shrimp Jetton v5.23 - GitHub CI监控 + 扩展标签")
    print(f"📊 监控仓库: {', '.join(GITHUB_REPOS)}")
    
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
                "github_workflows": load['github_workflows'],
                "local_builds": load['local_builds'],
                "max_wait_sec": load['max_wait_sec'],
                "total_tokens": load['total_tokens'],
                "last_active_sec": load['last_active_sec'],
                "task_queue": load['task_queue'],
                "cpu_percent": load['system']['cpu_percent'],
                "memory_percent": load['system']['memory_percent'],
                "workflow_details": load['workflow_details'],
                "build_details": load['build_details']
            }
            
            if update_redis(data):
                ts = datetime.now().strftime("%H:%M:%S")
                tasks = ", ".join([d['name'].split()[1] if ' ' in d['name'] else d['name'] 
                                   for d in load['task_queue'][:3]])
                wf_info = f" | {load['github_workflows']} CI" if load['github_workflows'] > 0 else ""
                build_info = f" | {load['local_builds']} Build" if load['local_builds'] > 0 else ""
                print(f"[{ts}] {text} | {tasks}{wf_info}{build_info}")
        except Exception as e:
            print(f"[ERR] {e}")
        
        time.sleep(15)

if __name__ == "__main__":
    main()
