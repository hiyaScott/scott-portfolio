# 认知负载监控修复记录 v5.32.0

## 修复时间
2026-03-17 13:50

## 修复内容

### 问题诊断
用户反馈的三个问题：
1. **评分一直停留在3%** 
2. **任务队列没有变化** 
3. **Token消耗不显示**

### 根本原因
`is_processing` 判断逻辑太严格：
```python
# 旧逻辑（v5.31）
if last_activity < 10 and has_recent_thinking:
    is_processing = True
```
- 只有10秒窗口期
- 实际处理可能持续数分钟
- 导致所有任务显示为"已回复"

### 修复方案（v5.32）
```python
# 新逻辑
# 1. 检测 .lock 文件（表示会话正在被写入）
lock_file = file_path + '.lock'
has_lock = os.path.exists(lock_file)

# 2. 有lock文件 = 正在处理中
if user_ts > assistant_ts:
    is_waiting = True
    wait_time = int(time.time() - user_ts)
    # 如果waiting时间短且有lock文件，说明正在处理中
    if wait_time < 300 and has_lock:
        is_processing = True
        is_waiting = False
elif has_lock or (last_activity < 60 and has_recent_thinking):
    is_processing = True
```

### 改进点
1. **检测 .lock 文件** - OpenClaw 在写入会话文件时会创建 .lock 文件
2. **放宽窗口期** - 从10秒放宽到60秒
3. **优先显示处理中** - 如果用户消息时间短且有lock，显示为处理中而非等待中

### 修复结果
| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| 评分 | 3% | 16% |
| 处理中 | 0 | 1 |
| Tokens | 0k | 135k |
| 任务状态 | 全部已回复 | 正确显示处理中 |

### 文件修改
- `cognitive_monitor.py` - 修复processing检测逻辑
- `cognitive-data.json` - 更新数据文件
- `cognitive-status.html` - 更新版本号至v5.32.0

### Git Commit
```
0a22c14 fix(monitor): v5.32 修复processing检测逻辑
```
