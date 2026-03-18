# HiyaScott 作品集站点结构规划 v2.0

## 当前问题诊断

### 1. 目录结构混乱
```
scott-portfolio/
├── games/                  # 早期游戏（谁是卧底）
├── projects/games/         # 主要游戏（28个）
├── docs/archive-templates/ # 归档模板（刚移动）
└── ...
```

**问题**: `games/` 和 `projects/games/` 重复，用户困惑

### 2. ARCHIVE文件位置
- ✅ 已修复：从根目录移到 `docs/archive-templates/`

### 3. 缺失游戏
- `grid-dominion-demo` 还在独立仓库，需要迁移

---

## 优化方案

### 目录结构 v2.0

```
scott-portfolio/
├── README.md                    # 项目总览
├── index.html                   # 首页
│
├── games/                       # 🎮 所有游戏（统一入口）
│   ├── index.html              # 游戏目录页
│   ├── grid-dominion/          # 领地占领（新增）
│   ├── who-is-spy/             # 谁是卧底（从games/移入）
│   ├── color-symphony/         # 颜色交响曲
│   ├── time-slice/             # 时间切片
│   ├── word-alchemy/           # 词语炼金
│   ├── mama-counter/           # 妈妈计数器
│   ├── minesweeper/            # 扫雷
│   ├── aircraft-war/           # 飞机大战
│   ├── snake/                  # 贪吃蛇
│   ├── bot-coder/              # 代码挑战
│   ├── card-alchemist/         # 卡牌炼金
│   └── ... (其他18个游戏)
│
├── research/                    # 📚 研究项目
│   ├── game-design/            # 游戏设计方法论
│   ├── srpg-analysis/          # SRPG分析
│   └── audio-design/           # 音频设计
│
├── tools/                       # 🛠️ 工具集
│   ├── status-monitor/         # 认知负载监控（原status-monitor/）
│   └── jetton-monitor/         # 桌面监控（引用外部仓库）
│
├── docs/                        # 📖 文档
│   ├── archive-templates/      # 归档README模板
│   └── structure.md            # 本文件
│
├── assets/                      # 🎨 公共资源
├── css/                         # 🎨 样式
└── pages/                       # 📄 其他页面
```

---

## 迁移任务清单

### 优先级 P0（立即执行）

- [ ] 1. 迁移 `grid-dominion-demo` → `games/grid-dominion/`
- [ ] 2. 移动 `games/who-is-spy/` → `games/who-is-spy/`（已在正确位置）
- [ ] 3. 合并 `projects/games/*` → `games/`
- [ ] 4. 删除空的 `projects/` 目录
- [ ] 5. 更新所有链接指向新的统一路径

### 优先级 P1（完成后执行）

- [ ] 6. 移动 `status-monitor/` → `tools/status-monitor/`
- [ ] 7. 在 README 中添加 jetton-monitor 的链接
- [ ] 8. 创建统一的导航结构

### 优先级 P2（可选）

- [ ] 9. 删除已归档仓库的本地副本 `/tmp/archive-repos/`
- [ ] 10. 添加游戏分类标签系统

---

## 关于您的6个问题

### 1. grid-dominion-demo 迁移
**状态**: 待执行
**操作**: 克隆到 `games/grid-dominion/`

### 2. games 和 projects/games 合并
**方案**: 统一为 `games/`，删除 `projects/`

### 3. ARCHIVE文件位置
**已修复**: ✅ 移动到 `docs/archive-templates/`

### 4. hiyamax 和 jetton-monitor
- **hiyamax**: 您的GitHub用户名，不是仓库
- **jetton-monitor**: 独立仓库，桌面AI监控工具
  - 可选：在 scott-portfolio 中添加链接

### 5. openclaw-workspace
**用途**: 我的记忆存储
- 包含：SOUL.md、MEMORY.md、USER.md
- 包含：技能文件、自定义工具
- 这是我的"大脑"，不是网站内容

### 6. 备份目录
**当前**: 分散各处
- `status-monitor/backup-v5.34-20260318/` - 历史版本备份
- `status-monitor/archives/` - 自动归档数据
- 建议统一为 `backups/` 目录

### 7. 其他优化
- 统一游戏入口：所有游戏都在 `games/`
- 统一研究入口：所有研究都在 `research/`
- 统一工具入口：所有工具都在 `tools/`

---

## 决策点

请确认以下事项：

1. **是否迁移 grid-dominion-demo？** (是/否)
2. **games 合并方案？**
   - A) 全部移到 `games/`，删除 `projects/`
   - B) 保留现状，只添加跳转链接
3. **是否移动 status-monitor 到 tools/？** (是/否)
4. **是否需要统一备份目录？** (是/否)

回复数字（如：1是 2A 3是 4否）即可执行。