# 备份说明文档

**备份名称**: backup-v5.34-20260318  
**备份时间**: 2026-03-18  
**原位置**: `/root/.openclaw/workspace/portfolio-blog/status-monitor/`  
**备份原因**: v5.34 大版本清理，归档不再活跃使用的文件

---

## 📁 目录结构

```
backup-v5.34-20260318/
├── README.md                                    # 本文档
├── CHANGELOG/                                   # 版本变更日志
│   └── CHANGELOG-v5.32.md
├── whitepaper/                                  # 技术白皮书
│   ├── whitepaper.html
│   └── 认知负载监控系统技术白皮书_v1.0.md
├── api-experiments/                             # API实验文件（未投产）
│   ├── api_8080.py
│   ├── api_http.py
│   ├── api_server.py
│   ├── api_server_v2.py
│   ├── api_simple.py
│   └── api_v2_1.py
├── legacy-versions/                             # 历史版本备份
│   ├── cognitive-status-v2.html
│   ├── cognitive-status-v5.19.8-backup.html
│   ├── cognitive-status-split.html
│   └── cognitive-monitor-v525.js
├── deprecated-systems/                          # 废弃系统
│   ├── status-sync.py       (Redis同步，已废弃)
│   ├── status.json          (旧状态格式)
│   └── index.html           (旧入口页)
└── misc/                                        # 其他杂项
    ├── config.env.example
    ├── test.html
    └── __pycache__/
```

---

## 📜 长线记忆价值评估

| 文件 | 记忆价值 | 理由 |
|------|----------|------|
| **CHANGELOG-v5.32.md** | ⭐⭐⭐⭐⭐ | 版本演进历史，记录功能迭代轨迹 |
| **技术白皮书** | ⭐⭐⭐⭐⭐ | 核心架构文档，算法原理、运维指南 |
| **test.html** | ⭐ | 临时测试文件，无长期价值 |
| **API实验文件** | ⭐⭐⭐ | 技术探索记录，可参考但不再使用 |

### 值得写入长线记忆的2类文件：

#### 1. CHANGELOG-v5.32.md
**为什么重要**: 记录了v5.32版本的关键功能迭代：
- 混合认知评分算法
- 智能任务标签系统（24个标签）
- 实时负载趋势图
- 收音机调频仪表盘设计

**记忆位置**: `MEMORY.md` 系统配置章节

#### 2. 技术白皮书（2份）
**为什么重要**: 
- 详细记录系统架构演进
- 评分算法数学原理
- Redis→本地文件迁移决策
- 踩坑记录和运维经验

**记忆位置**: 
- `MEMORY.md` 备份至 whitepaper/ 目录
- 原理解析可提炼到 MEMORY.md 架构章节

---

## 🎯 当前活跃系统（v5.34）

清理后保留在生产环境的文件：

```
status-monitor/
├── cognitive_monitor.py        # 核心脚本 v5.34
├── cognitive_cron.sh           # 定时任务
├── cognitive_push.sh           # Git推送 v3.1
├── cognitive-status.html       # 主页面 v5.34.3
├── cognitive-status.css        # 样式
├── cognitive-status.js         # JS逻辑
├── cognitive-data.json         # 实时数据
├── cognitive-history.jsonl     # 历史数据
├── archives/                   # 归档目录
├── README.md                   # 项目说明
├── CLEANUP-LIST-v5.34.md       # 本次清理清单
└── backup-v5.34-20260318/      # 本备份文件夹
```

---

## ⚠️ 注意事项

1. **备份完整性**: 此备份包含除 `archives/`、`cognitive-data.json`、`cognitive-history.jsonl` 外的全部文件
2. **恢复方式**: 如需恢复某文件，直接从本目录复制到 `../` 即可
3. **删除时机**: 确认 v5.34 稳定运行30天后，可删除本备份
4. **长期保存**: whitepaper/ 和 CHANGELOG/ 建议永久保留

---

**备份创建者**: Jetton  
**备份目的**: v5.34 版本大清理归档