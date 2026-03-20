# 认知负载监控系统 - 数据源同步流程

## 当前架构（v6.1 统一数据源）

### 单一数据源原则

```
┌─────────────────────────────────────────────────────────────┐
│                    服务器 (本地)                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 监控脚本 (cognitive_monitor.py)                        │  │
│  │   ↓ 写入                                               │  │
│  │   ./cognitive-data.json                                │  │
│  │   ./cognitive-history.jsonl                            │  │
│  └───────────────────────────────────────────────────────┘  │
│                           ↓                                  │
│                    推送脚本 (每5分钟)                         │
│                           ↓                                  │
│              GitHub (scott-portfolio 仓库)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    GitHub Pages (部署)
                              ↓
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
   ┌─────────┐          ┌──────────┐         ┌──────────┐
   │ 主页卡片 │          │ 监控页面  │         │ 历史趋势  │
   │ index   │          │ cognitive│         │ 图表     │
   │ .html   │          │ -status  │         │          │
   └─────────┘          │ .html    │         └──────────┘
                        └──────────┘
```

### 数据流

1. **监控脚本** 每5分钟运行一次，生成 `cognitive-data.json`
2. **推送脚本** 每5分钟（错开2分钟）将数据推送到 GitHub
3. **GitHub Pages** 自动部署，所有界面从同一文件读取数据

## 文件清单

### 核心文件（`portfolio-blog/status-monitor/`）

| 文件 | 用途 | 读写 |
|------|------|------|
| `cognitive_monitor.py` | 监控脚本 | 写 |
| `cognitive_push_v6.sh` | 推送脚本 | - |
| `cognitive-data.json` | 实时数据 | 读写 |
| `cognitive-history.jsonl` | 历史数据 | 读写 |
| `trend-data.json` | 趋势数据 | 写 |
| `cognitive-status.html` | 监控页面 | 读 |
| `cognitive-status.css` | 样式 | - |
| `cognitive-status.js` | 前端逻辑 | 读 |
| `archives/` | 归档备份 | 写 |

### 主页文件（`portfolio-blog/`）

| 文件 | 用途 | 读写 |
|------|------|------|
| `index.html` | 主页 | 读 `./status-monitor/cognitive-data.json` |

## 已删除的废弃组件

### 数据源
- ❌ `scott-portfolio-data` 仓库（本地已删除，GitHub 上可手动删除）
- ❌ Redis (Upstash) 连接
- ❌ CDN (jsdelivr) 回退

### 自动化任务
- ❌ systemd 服务 (`cognitive-monitor.service`，已重启 56961 次)
- ❌ 多个版本推送脚本 (v4, v5)
- ❌ 实验性 API 服务器

### 文件
- ❌ 所有 `scott-portfolio-data` 目录下的数据文件
- ❌ `api_server.py`, `api_simple.py`
- ❌ `github_upload.py`
- ❌ `cognitive_cron.sh`
- ❌ 临时 lock 文件

## 调试与验证

### 检查当前数据
```bash
# 本地数据
cat /root/.openclaw/workspace/portfolio-blog/status-monitor/cognitive-data.json | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'时间: {d[\"timestamp\"]}')
print(f'分数: {d[\"cognitive_score\"]}%')
print(f'任务: {[t[\"label\"] for t in d.get(\"task_queue\", [])]}')
"

# GitHub Pages 数据
curl -s 'https://hiyascott.github.io/scott-portfolio/status-monitor/cognitive-data.json' | python3 -c "
import json,sys
d=json.load(sys.stdin)
print(f'时间: {d.get(\"timestamp\", \"N/A\")}')
print(f'分数: {d.get(\"cognitive_score\", \"N/A\")}%')
"
```

### 检查自动化任务
```bash
# 查看 crontab
crontab -l | grep cognitive

# 查看进程
ps aux | grep cognitive_monitor | grep -v grep

# 查看日志
tail -20 /var/log/cognitive_monitor.log
tail -20 /var/log/cognitive_health.log
```

### 手动触发更新
```bash
# 运行监控脚本
cd /root/.openclaw/workspace/portfolio-blog/status-monitor
python3 cognitive_monitor.py

# 推送数据
cd /root/.openclaw/workspace/portfolio-blog
bash status-monitor/cognitive_push_v6.sh
```

## 故障排查

### 主页和监控页面数据不一致

**原因**: 数据未同步到 GitHub Pages

**检查步骤**:
1. 检查本地数据时间戳是否最新
2. 检查推送日志是否有错误
3. 等待 1-2 分钟让 GitHub Pages 部署

### 任务标签错误

**检查会话文件**:
```bash
ls -la /root/.openclaw/agents/main/sessions/*.lock
```

**手动检查标签解析**:
```bash
python3 cognitive_monitor.py  # 查看输出中的任务标签
```

### 监控脚本未运行

**检查**:
```bash
ps aux | grep cognitive_monitor
# 如果没有进程，等待下次 crontab 触发或手动运行
```

## 历史归档

历史数据归档保存在:
- `portfolio-blog/status-monitor/archives/` (热归档，7天)
- `portfolio-blog/backups/status-monitor/backup-v5.34-20260318/` (完整备份)

如需恢复旧版本数据，可从备份中提取。

---

**当前版本**: v6.1  
**最后更新**: 2026-03-20  
**GitHub 提交**: `97e181e`