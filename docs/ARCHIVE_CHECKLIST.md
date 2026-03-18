# 📦 需要归档的资源清单

## 已执行操作总结

### ✅ 步骤1: grid-dominion-demo 迁移
- **状态**: 部分完成（创建占位文件）
- **说明**: wasm文件太大(37MB)下载失败，已创建跳转占位页
- **位置**: `games/grid-dominion/index.html`
- **建议**: 后续手动从原仓库下载完整文件替换

### ✅ 步骤2: games 目录合并
- **操作**: projects/games/ → games/
- **结果**: 32个游戏统一在 games/ 目录
- **删除**: projects/ 空目录已删除

### ✅ 步骤4: backup 目录统一
- **新结构**: `backups/status-monitor/`, `backups/archive-readmes/`
- **迁移**: status-monitor/backup-v5.34-*/ → backups/status-monitor/

### ✅ 步骤5: Debug 检查通过

---

## 🔒 建议归档的 GitHub 仓库

### 已迁移到 scott-portfolio（需归档）
| 仓库 | 迁移位置 | 归档状态 |
|------|----------|----------|
| mama-counter | games/mama-counter/ | ⏳ 待手动归档 |
| minesweeper-demo | games/minesweeper/ | ⏳ 待手动归档 |
| aircraft-war | games/aircraft-war/ | ⏳ 待手动归档 |
| snake-game | games/snake/ | ⏳ 待手动归档 |
| game-design-portfolio | research/game-design/ | ⏳ 待手动归档 |
| **grid-dominion-demo** | games/grid-dominion/ | ⏳ 待归档（README已添加） |

**归档步骤**: 进入仓库 → Settings → Archive this repository

---

## 🗂️ 当前 scott-portfolio 结构

```
scott-portfolio/
├── 📄 index.html              # 首页
├── 📄 README.md               # 项目说明
│
├── 🎮 games/                  # 32个游戏
│   ├── grid-dominion/        # 领地占领（占位）
│   ├── mama-counter/         # 妈妈计数器
│   ├── minesweeper/          # 扫雷（Godot）
│   ├── aircraft-war/         # 飞机大战
│   ├── snake/                # 贪吃蛇
│   ├── color-symphony/       # 颜色交响曲
│   ├── time-slice/           # 时间切片
│   ├── word-alchemy/         # 词语炼金
│   └── ... (24个其他游戏)
│
├── 📚 research/               # 研究项目
│   ├── game-design/          # 游戏设计方法论
│   ├── srpg-analysis/        # SRPG分析
│   └── audio-design/         # 音频设计
│
├── 🛠️ tools/                  # 工具（预留）
│
├── 📊 status-monitor/         # 认知负载监控（保持现状）
│
├── 💾 backups/                # 统一备份
│   ├── status-monitor/       # v5.34备份
│   └── archive-readmes/      # 归档模板
│
├── 📖 docs/                   # 文档
│   ├── archive-templates/    # 5个归档README模板
│   └── structure-plan.md     # 结构规划
│
├── 🎨 assets/                 # 公共资源
├── 🎨 css/                    # 样式
└── 📄 pages/                  # 其他页面
```

---

## ⚠️ 待处理事项

### 高优先级
1. **grid-dominion 完整迁移**: wasm文件太大，需手动下载
   ```bash
   # 下载命令
   curl -L -o games/grid-dominion/index.wasm \
     https://raw.githubusercontent.com/hiyaScott/grid-dominion-demo/main/index.wasm
   ```

2. **6个仓库归档**: 在GitHub网页上手动归档

### 低优先级
3. **更新 games/index.html**: 添加 grid-dominion 卡片
4. **清理 /tmp/archive-repos/**: 本地临时文件可删除

---

## 🔗 重要链接

- **主站**: https://hiyascott.github.io/scott-portfolio/
- **游戏目录**: https://hiyascott.github.io/scott-portfolio/games/
- **grid-dominion（原）**: https://hiyascott.github.io/grid-dominion-demo/
- **认知监控**: https://hiyascott.github.io/scott-portfolio/status-monitor/

---

生成时间: 2026-03-18 22:45
