# Status-Monitor 目录清理清单（分类版）

**生成时间**: 2026-03-18 15:10  
**当前版本**: v5.34.3  
**目录**: `/root/.openclaw/workspace/portfolio-blog/status-monitor/`

---

## 📁 一、当前在用（保留）

> v5.34 正在运行的核心文件，**不可删除**

| 文件/目录 | 用途 | 版本 |
|-----------|------|------|
| `cognitive_monitor.py` | 核心监控脚本（会话分析+评分算法） | v5.34 |
| `cognitive_cron.sh` | 定时任务入口（每分钟执行） | v5.34 |
| `cognitive_push.sh` | Git推送脚本（v3.1，双文件推送） | v3.1 |
| `cognitive-status.html` | 主页面（走势图+收音机仪表盘） | v5.34.3 |
| `cognitive-data.json` | 实时数据文件（前端读取） | - |
| `cognitive-history.jsonl` | 历史数据（JSON Lines格式） | - |
| `cognitive-status.css` | 样式文件（当前在用） | - |
| `cognitive-status.js` | JS逻辑（当前在用） | - |
| `archives/` | 归档目录（7天+月度gzip） | - |

---

## 🗂️ 二、历史版本备份（可删除）

> 旧版本备份，当前已不再使用

| 文件 | 说明 | 建议操作 |
|------|------|----------|
| `cognitive-status-v2.html` | v5.19之前的版本 | **删除** |
| `cognitive-status-v5.19.8-backup.html` | v5.19.8备份 | **删除** |
| `cognitive-status-split.html` | 实验性拆分版本 | **删除** |
| `cognitive-monitor-v525.js` | v5.25的JS备份 | **删除** |

---

## 🧪 三、实验性API文件（可删除）

> 早期API实验，未投入生产

| 文件 | 说明 | 建议操作 |
|------|------|----------|
| `api_8080.py` | 8080端口API实验 | **删除** |
| `api_http.py` | HTTP API实验 | **删除** |
| `api_server.py` | API服务器v1 | **删除** |
| `api_server_v2.py` | API服务器v2 | **删除** |
| `api_simple.py` | 简化API实验 | **删除** |
| `api_v2_1.py` | API v2.1实验 | **删除** |

---

## ⏳ 四、旧系统废弃文件（可删除）

> 旧架构遗留，已被新系统替代

| 文件 | 旧用途 | 替代方案 | 建议操作 |
|------|--------|----------|----------|
| `status-sync.py` | Redis同步脚本 | 本地JSON文件 | **删除** |
| `status.json` | 旧状态文件 | `cognitive-data.json` | **删除** |
| `index.html` | 旧版入口页 | 已合并到主页面 | **删除** |

---

## 📝 五、文档类（待确认）

| 文件 | 说明 | 建议 |
|------|------|------|
| `README.md` | 项目说明 | **保留** |
| `CHANGELOG-v5.32.md` | v5.32变更日志 | 可删除（已过时）或 **保留** |
| `whitepaper.html` | 技术白皮书HTML版 | 待确认 |
| `认知负载监控系统技术白皮书_v1.0.md` | 白皮书Markdown | 待确认 |
| `test.html` | 测试页面 | **删除** |
| `config.env.example` | 配置示例（Redis时代） | **删除** |

---

## 📊 六、统计汇总

| 类别 | 数量 | 可删除 | 保留 |
|------|------|--------|------|
| 当前在用 | 9 | 0 | 9 |
| 历史版本 | 4 | 4 | 0 |
| 实验API | 6 | 6 | 0 |
| 旧系统 | 3 | 3 | 0 |
| 文档类 | 6 | 2 | 4 |
| **总计** | **28** | **15** | **13** |

---

## ⚡ 七、清理命令（一键执行）

```bash
cd /root/.openclaw/workspace/portfolio-blog/status-monitor/

# 1. 删除历史版本
rm -f cognitive-status-v2.html \
      cognitive-status-v5.19.8-backup.html \
      cognitive-status-split.html \
      cognitive-monitor-v525.js

# 2. 删除实验API文件
rm -f api_8080.py api_http.py api_server.py \
      api_server_v2.py api_simple.py api_v2_1.py

# 3. 删除旧系统文件
rm -f status-sync.py status.json index.html

# 4. 删除临时/测试文件
rm -f test.html config.env.example

# 5. 可选：删除过时文档
# rm -f CHANGELOG-v5.32.md

# 6. 清理Python缓存
rm -rf __pycache__

echo "清理完成"
ls -la
```

---

## 🎯 八、删除后保留清单

```
status-monitor/
├── archives/                  # 归档目录
├── cognitive_monitor.py       # 核心脚本 v5.34
├── cognitive_cron.sh          # 定时任务 v5.34
├── cognitive_push.sh          # 推送脚本 v3.1
├── cognitive-status.html      # 主页面 v5.34.3
├── cognitive-status.css       # 样式
├── cognitive-status.js        # JS逻辑
├── cognitive-data.json        # 实时数据
├── cognitive-history.jsonl    # 历史数据
├── README.md                  # 项目说明
├── CHANGELOG-v5.32.md         # 旧日志（可选删）
├── whitepaper.html            # 白皮书（待确认）
└── 认知负载监控系统技术白皮书_v1.0.md
```

---

## ⚠️ 九、重要提醒

1. **删除前请再次确认** `cognitive_monitor.py` 和 `cognitive_cron.sh` 是 v5.34 版本
2. **不要删除** `archives/` 目录，里面有历史归档数据
3. **whitepaper** 两份文件如需保留可移动到 `docs/` 目录
4. 清理后建议 **重启一次 cron 服务** 确保定时任务正常

---

**等待确认后执行清理**