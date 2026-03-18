#!/usr/bin/env python3
"""
Shrimp Jetton 认知负载监控 v5.35 - 优化状态显示
更新：
- v5.35: 状态显示改为"最后活跃时间"替代"等待时间"，更准确反映会话状态
- v5.34: 从Redis迁移到本地JSON Lines存储，添加自动归档
- v5.32: 扩展时间窗口检测子代理任务(1小时)，添加勘误相关关键词
- v5.31.1: 更严格的处理中判断(10秒)，降低token评分权重，空闲状态(max 10%)
- v5.31.0: 优化空闲状态评分，无任务时负载不超过15%
- v5.28: 降低等待时间评分权重（等待4分钟不再高负载）
- v5.28: 修复任务名称重复显示问题
- v5.28: 优化任务状态判断逻辑
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
DATA_FILE = "/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json"
HISTORY_FILE = "/root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-history.jsonl"
ARCHIVE_DIR = "/root/.openclaw/workspace/portfolio-blog/status-monitor/archives"

# v5.34: 历史数据保留配置
HISTORY_RETENTION_DAYS = 7  # 7天热数据
ARCHIVE_RETENTION_MONTHS = 12  # 保留12个月归档

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
    
    # 数据勘误/校对
    '勘误': '数据勘误',
    'correction': '数据勘误',
    '数据库勘误': '数据勘误',
    '数据勘误': '数据勘误',
    '数据核对': '数据勘误',
    '数据对比': '数据勘误',
    '数据验证': '数据勘误',
    '数据校对': '数据勘误',
    '数据纠错': '数据勘误',
    '错误修正': '数据勘误',
    '数据质量': '数据勘误',
    
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
    """获取会话文件 - v5.32: 扩展时间窗口以检测子代理任务"""
    pattern = os.path.join(WORKSPACE, "*.jsonl")
    files = glob.glob(pattern)
    sessions = []
    now = time.time()
    for f in files:
        try:
            stat = os.stat(f)
            mtime = stat.st_mtime
            age = now - mtime
            
            # 策略调整：
            # 1. 10分钟内修改的文件 -> 活跃会话
            # 2. 10-60分钟内修改的文件 -> 可能是子代理任务，也包含进来
            if age < 600:  # 10分钟内
                sessions.append({'file': f, 'name': os.path.basename(f), 'mtime': mtime, 'is_subagent': False})
            elif age < 3600:  # 10-60分钟内，可能是子代理任务
                sessions.append({'file': f, 'name': os.path.basename(f), 'mtime': mtime, 'is_subagent': True})
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
                        has_tool_result = False
                        has_text_output = False
                        
                        if isinstance(content_list, list):
                            for item in content_list:
                                if isinstance(item, dict):
                                    if item.get('type') == 'toolResult':
                                        has_tool_result = True
                                    elif item.get('type') == 'text' and len(item.get('text', '')) > 50:
                                        has_text_output = True
                                    elif item.get('type') == 'thinking':
                                        has_recent_thinking = True
                        
                        # 只有有实际输出时才更新最后助手时间
                        if has_tool_result or has_text_output:
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
        
        # 三种状态判断 - v5.34: 区分当前对话和后台任务
        is_waiting = False
        is_processing = False
        is_current_session = False  # 新增：是否是当前正在进行的对话
        wait_time = 0
        
        # 检测是否有lock文件（表示正在被写入/处理中）
        lock_file = file_path + '.lock'
        has_lock = os.path.exists(lock_file)
        
        # 判断是否是"当前对话"（用户消息在30秒内且lock存在）
        if has_lock and user_ts > 0:
            time_since_user_msg = time.time() - user_ts
            if time_since_user_msg < 30:  # 30秒内的用户消息 = 当前对话
                is_current_session = True
        
        if user_ts > assistant_ts:
            is_waiting = True
            wait_time = int(time.time() - user_ts)
            # 如果waiting时间短且有lock文件，说明正在处理中
            if wait_time < 300 and has_lock:
                is_processing = True
                is_waiting = False  # 优先显示为处理中
        elif has_lock or (last_activity < 60 and has_recent_thinking):
            # 有lock文件，或60秒内有thinking消息 = 处理中
            is_processing = True
        
        return {
            'messages': messages,
            'estimated_tokens': total_tokens,
            'tool_calls': tool_calls,
            'is_waiting': is_waiting,
            'is_processing': is_processing,
            'user_ts': user_ts,  # 新增：返回用户消息时间戳
            'wait_time': max(0, wait_time),
            'last_mtime': file_mtime,
            'session_type': session_type,
            'session_name': session_name,
            'full_type': f"{session_type} {session_name}",
            'has_lock': has_lock
        }
    except Exception as e:
        print(f"[analyze_session error] {e}")
        return {'messages': 0, 'estimated_tokens': 0, 'tool_calls': 0, 
                'is_waiting': False, 'is_processing': False, 'user_ts': 0, 'wait_time': 0, 'last_mtime': 0,
                'session_type': "💭", 'session_name': "未知", 'full_type': "💭 未知", 'has_lock': False}

def get_cognitive_load():
    """获取认知负载 - v5.33: 修复任务去重问题"""
    sessions = get_session_files()
    github_workflows = get_github_workflow_status()
    local_builds = get_local_build_processes()
    
    # 合并所有任务
    all_tasks = []
    seen_sessions = set()  # 用于去重
    
    # 1. 会话任务
    if sessions:
        total_tokens = 0
        pending_count = 0
        processing_count = 0
        max_wait = 0
        recent_mtime = 0
        
        for sess in sessions:
            file_key = os.path.basename(sess['file'])  # 用于去重的key
            if file_key in seen_sessions:
                continue  # 跳过重复
            seen_sessions.add(file_key)
            
            a = analyze_session(sess['file'])
            total_tokens += a['estimated_tokens']
            recent_mtime = max(recent_mtime, a['last_mtime'])
            
            if a['is_waiting']:
                pending_count += 1
                max_wait = max(max_wait, a['wait_time'])
            elif a['is_processing']:
                processing_count += 1
            
            # 状态显示 - v5.35: 改为"最后活跃"而非"等待"，更准确
            if a['is_waiting']:
                if a['wait_time'] > 120:
                    status = f"💤 {a['wait_time']//60}分钟前活跃"
                elif a['wait_time'] > 60:
                    status = f"💤 {a['wait_time']//60}分钟前活跃"
                else:
                    status = f"💤 {a['wait_time']}秒前活跃"
            elif a['is_processing']:
                status = "🔄 处理中"
            else:
                status = "✅ 已回复"
            
            # 标记系统监控任务 - v5.34: 特殊处理
            is_system_monitor = '系统监控' in a['full_type']
            
            all_tasks.append({
                'name': a['full_type'],
                'status': status,
                'tokens': a['estimated_tokens'],
                'type': 'session',
                'file_key': file_key,
                'user_ts': a.get('user_ts', 0),  # 用户消息时间戳
                'is_system_monitor': is_system_monitor  # 标记系统监控
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
    
    # 评分算法 v5.34 - 当前对话特殊处理
    # 当前对话的处理中加分减半（7分而不是15分）
    
    # 基础分：只基于待处理和处理中的任务
    base_score = 0
    
    # 活跃会话基础分 - 空闲会话不应产生明显负载
    if pending_count > 0 or processing_count > 0:
        # 有实际工作时，会话数才有意义
        base_score += min(len(sessions) * 1, 4)  # v5.34: 降低为1分/个，最高4分
    else:
        # 空闲状态，只有非常低的背景分
        base_score = min(len(sessions), 2)
    
    # GitHub构建加成
    github_bonus = len(github_workflows) * 10
    
    # 本地构建加成  
    build_bonus = len(local_builds) * 8
    
    # 等待评分 - 根据等待时间和待处理数量
    wait_score = 0
    if pending_count > 0:
        # 基础等待分
        wait_score = min(pending_count * 8, 20)
        # 长时间等待加成
        if max_wait > 300:  # 5分钟以上
            wait_score += 15
        elif max_wait > 120:  # 2分钟以上
            wait_score += 8
        elif max_wait > 60:  # 1分钟以上
            wait_score += 3
    
    # 处理中任务评分 - v5.34: 区分当前对话、后台任务、系统监控
    processing_score = 0
    
    # 识别当前对话：检查每个处理中任务的最后用户消息时间
    current_session_count = 0
    system_monitor_count = 0
    normal_processing_count = 0
    
    for t in all_tasks:
        if '🔄' in t.get('status', ''):
            if t.get('is_system_monitor'):
                # 系统监控：单独计数
                system_monitor_count += 1
            else:
                user_ts = t.get('user_ts', 0)
                # 如果用户消息在600秒内（10分钟），标记为当前对话
                if user_ts > 0 and time.time() - user_ts < 600:
                    t['is_current_session'] = True
                    current_session_count += 1
                else:
                    normal_processing_count += 1
    
    # 普通后台任务：15分/个
    processing_score += normal_processing_count * 15
    # 当前对话：7分/个
    processing_score += current_session_count * 7
    # 系统监控：4分/个
    processing_score += system_monitor_count * 4
    
    # 任务排序：系统监控排最后，超过4个任务时隐藏
    # 排序优先级：最近活跃 > 处理中(非系统监控) > 已回复 > 系统监控
    def task_priority(t):
        if '前活跃' in t.get('status', ''):
            return (0, 0, t.get('wait_time', 0))  # 等待时间长的排前面
        elif '🔄' in t.get('status', '') and not t.get('is_system_monitor'):
            return (1, 0, 0)
        elif '✅' in t.get('status', ''):
            return (2, 0, 0)
        else:
            return (3, 0, 0)  # 系统监控排最后
    
    all_tasks.sort(key=task_priority)
    
    # 如果任务超过4个，隐藏系统监控任务
    if len(all_tasks) > 4:
        all_tasks = [t for t in all_tasks if not t.get('is_system_monitor', False)]
        # 重新计算processing_count（排除系统监控）
        processing_count = sum(1 for t in all_tasks if '🔄' in t.get('status', '') or '前活跃' in t.get('status', ''))
    
    # 最终评分
    if pending_count == 0 and processing_count == 0 and len(github_workflows) == 0 and len(local_builds) == 0:
        # 真正的空闲状态
        score = min(base_score, 8)
    else:
        score = min(base_score + wait_score + processing_score + github_bonus + build_bonus, 100)
    
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

def update_data_file(data):
    """更新 cognitive-data.json 文件供前端读取"""
    try:
        # 转换 task_queue 格式以兼容前端
        formatted_tasks = []
        for task in data.get('task_queue', []):
            # 修复：只保留一个名称，避免重复显示
            task_name = task.get('name', '💭 未知任务')
            formatted_tasks.append({
                'label': task_name,
                'status': task.get('status', '✅ 空闲'),
                'tokens': task.get('tokens', 0),
                'type': task.get('type', 'session'),
                'last_role': 'user' if '前活跃' in task.get('status', '') else 'assistant'
            })
        
        # 构建前端兼容的数据格式
        output = {
            "timestamp": data.get('timestamp'),
            "cognitive_score": data.get('cognitive_score'),
            "score_breakdown": {
                "wait_score": 0,
                "token_score": 0,
                "base_score": data.get('cognitive_score', 0),
                "active_sessions": data.get('active_sessions', 0),
                "recent_active": data.get('active_sessions', 0),
                "tool_calls": 0,
                "pending": data.get('pending_count', 0),
                "processing": data.get('processing_count', 0),
                "estimated_response": 30
            },
            "status_code": data.get('status_code'),
            "status_text": data.get('status_text'),
            "suggestion": data.get('suggestion'),
            "active_sessions": data.get('active_sessions', 0),
            "recent_active_count": data.get('active_sessions', 0),
            "total_tool_calls": 0,
            "pending_count": data.get('pending_count', 0),
            "processing_count": data.get('processing_count', 0),
            "github_workflows": data.get('github_workflows', 0),
            "local_builds": data.get('local_builds', 0),
            "total_tokens": data.get('total_tokens', 0),
            "total_tokens_formatted": f"{(data.get('total_tokens', 0) / 1000):.1f}k",
            "estimated_response": 30,
            "estimated_response_formatted": f"{30}s",
            "task_queue": formatted_tasks,
            "cpu_percent": data.get('cpu_percent', 0),
            "memory_percent": data.get('memory_percent', 0),
            "workflow_details": data.get('workflow_details', []),
            "build_details": data.get('build_details', [])
        }
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[DATA_FILE ERROR] {e}")
        return False

def update_history_file(data):
    """v5.34: 追加历史数据到 JSON Lines 文件"""
    try:
        # 精简数据，只存储必要的走势数据
        history_record = {
            "timestamp": data.get('timestamp'),
            "score": data.get('cognitive_score', 0),
            "sessions": data.get('active_sessions', 0),
            "pending": data.get('pending_count', 0),
            "processing": data.get('processing_count', 0),
            "tokens": data.get('total_tokens', 0),
            "cpu": data.get('cpu_percent', 0),
            "memory": data.get('memory_percent', 0)
        }
        
        # 追加写入 JSON Lines
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(history_record, ensure_ascii=False) + '\n')
        
        return True
    except Exception as e:
        print(f"[HISTORY_FILE ERROR] {e}")
        return False

def cleanup_history_file():
    """v5.34: 清理过期历史数据（7天前的数据归档）"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return
        
        cutoff_time = time.time() - (HISTORY_RETENTION_DAYS * 24 * 3600)
        current_month = datetime.now().strftime("%Y-%m")
        archive_file = os.path.join(ARCHIVE_DIR, f"cognitive-{current_month}.jsonl")
        
        # 确保归档目录存在
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        
        # 读取所有记录
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        recent_lines = []
        old_lines = []
        
        for line in lines:
            try:
                record = json.loads(line.strip())
                record_ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00')).timestamp()
                
                if record_ts > cutoff_time:
                    recent_lines.append(line)
                else:
                    old_lines.append(line)
            except:
                continue
        
        # 将过期数据归档
        if old_lines:
            with open(archive_file, 'a', encoding='utf-8') as f:
                f.writelines(old_lines)
            print(f"[HISTORY] 归档 {len(old_lines)} 条记录到 {archive_file}")
        
        # 重写历史文件（只保留最近7天）
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            f.writelines(recent_lines)
        
        return True
    except Exception as e:
        print(f"[HISTORY_CLEANUP ERROR] {e}")
        return False

def compress_old_archives():
    """v5.34: 压缩上月及更早的归档文件"""
    try:
        if not os.path.exists(ARCHIVE_DIR):
            return
        
        current_month = datetime.now().strftime("%Y-%m")
        import gzip
        
        for filename in os.listdir(ARCHIVE_DIR):
            if filename.endswith('.jsonl') and not filename.startswith(current_month):
                filepath = os.path.join(ARCHIVE_DIR, filename)
                gz_path = filepath + '.gz'
                
                # 如果已压缩则跳过
                if os.path.exists(gz_path):
                    continue
                
                # 压缩文件
                with open(filepath, 'rb') as f_in:
                    with gzip.open(gz_path, 'wb') as f_out:
                        f_out.writelines(f_in)
                
                # 删除原文件
                os.remove(filepath)
                print(f"[ARCHIVE] 压缩 {filename} -> {filename}.gz")
        
        return True
    except Exception as e:
        print(f"[ARCHIVE_COMPRESS ERROR] {e}")
        return False

def get_history_data(hours=1, max_points=200):
    """v5.34: 获取指定时间范围的历史数据供前端使用"""
    try:
        if not os.path.exists(HISTORY_FILE):
            return []
        
        cutoff_time = time.time() - (hours * 3600)
        records = []
        
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    record_ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00')).timestamp()
                    
                    if record_ts > cutoff_time:
                        records.append(record)
                except:
                    continue
        
        # 如果数据点太多，进行采样
        if len(records) > max_points:
            step = len(records) // max_points
            records = records[::step]
        
        return records
    except Exception as e:
        print(f"[GET_HISTORY ERROR] {e}")
        return []

def main():
    """主循环 - v5.34: 添加历史数据存储和自动归档"""
    print("🧠 Shrimp Jetton v5.34 - 本地历史数据 + 自动归档")
    print(f"📊 监控仓库: {', '.join(GITHUB_REPOS)}")
    print(f"📈 历史数据: {HISTORY_FILE}")
    print(f"📦 归档目录: {ARCHIVE_DIR}")
    print("⏱️  更新频率: 每60秒")
    
    last_cleanup_hour = -1
    last_compress_day = -1
    
    while True:
        try:
            current_hour = datetime.now().hour
            current_day = datetime.now().day
            
            # 每小时整点执行清理
            if current_hour != last_cleanup_hour:
                cleanup_history_file()
                last_cleanup_hour = current_hour
            
            # 每天凌晨3点执行压缩归档
            if current_day != last_compress_day and current_hour == 3:
                compress_old_archives()
                last_compress_day = current_day
            
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
            
            # v5.34: 更新数据文件 + 历史数据
            if update_data_file(data):
                update_history_file(data)
                ts = datetime.now().strftime("%H:%M:%S")
                tasks = ", ".join([d['name'].split()[1] if ' ' in d['name'] else d['name'] 
                                   for d in load['task_queue'][:3]])
                wf_info = f" | {load['github_workflows']} CI" if load['github_workflows'] > 0 else ""
                build_info = f" | {load['local_builds']} Build" if load['local_builds'] > 0 else ""
                print(f"[{ts}] {text} | {tasks}{wf_info}{build_info}")
            
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] [ERR] {e}")
        
        time.sleep(60)  # 每60秒更新一次

if __name__ == "__main__":
    main()
