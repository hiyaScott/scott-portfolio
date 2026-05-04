# 课件系统技术规范 v2.0

> 适用于 research/junior-{subject}/courseware-{subject}/ 目录下的所有章节课件

---

## 目录结构

```
research/junior-{subject}/                    # 学科主页
  courseware-{subject}/grade{grade}-sem{sem}-ch{chapter}/  # 具体章节
    index.html                                 # 游戏
    tutorial.html                              # 教程
```

**示例：**
- `research/junior-physics/courseware-physics/grade6-sem1-ch01/`
- `research/junior-math/courseware-math/grade6-sem1-ch01/`

---

## 视觉系统

### 配色

| 角色 | 物理 | 数学 |
|------|------|------|
| 背景 | `#06080f` | `#06080f` |
| 强调色 | `#00f0c8` | `#00f5d4` |
| 辅助色 | `#00bbf9` | `#00bbf9` |
| 危险 | `#ef476f` | `#ef476f` |
| 成功 | `#06d6a0` | `#06d6a0` |
| 警告 | `#ffd166` | `#ffd166` |

### 字体
- 标题：`Orbitron` (科幻无衬线)
- 正文：`Share Tech Mono` + `Courier New` fallback

### HUD风格元素
- 扫描线：`body::before` repeating-linear-gradient
- 网格背景：`#hud-grid` 60px网格
- 四角装饰：`.corner-tl/br/bl/tr` 2px边框
- 毛玻璃：`backdrop-filter: blur(12px)`

---

## 交互系统

### 按钮体系

```css
.btn           /* 主按钮：实心填充 */
.btn-ghost     /* 次级按钮：透明边框 */
.btn-warn      /* 警告按钮：黄色 */
```

### 反馈系统

```javascript
showFeedback(text, type)  // type: 'ok' | 'wrong'
```
- 正确：绿色闪烁 + 成功音效
- 错误：红色抖动 + 错误音效

### 章节跳转面板

```css
.stage-nav-panel   /* 物理游戏 */
.level-nav-panel   /* 数学游戏 */
```

**规范：**
- 触发按钮：`☰` 符号，位于HUD右上角
- 面板位置：`fixed; top: 70px; right: 20px`
- 背景：毛玻璃 + 边框
- 当前项高亮：`border-left` + 加粗
- 点击外部关闭：`document.addEventListener('click')`

---

## 移动端适配标准

### 必 breakpoint 清单

```css
/* 折叠屏展开 / 大平板 */
@media (max-width: 1024px) { ... }

/* 平板竖屏 */
@media (max-width: 768px) { ... }

/* 手机 */
@media (max-width: 480px) { ... }

/* 横屏手机 */
@media (max-height: 500px) and (orientation: landscape) { ... }

/* 折叠屏展开模式 */
@media (min-width: 700px) and (max-width: 900px) and (min-height: 1000px) { ... }
```

### 适配原则
1. **触摸目标最小 44px**
2. **文字不低于 12px**
3. **弹性布局优先**：flex + grid，避免绝对定位
4. **视觉元素缩放**：`transform: scale(0.7~0.85)` 保持比例
5. **内容折叠**：横屏时精简HUD、缩小非核心元素

---

## 游戏文件规范

### 物理游戏结构

```
├── intro-screen        # 封面
├── stage1 (Length)     # 刻度尺估读
├── stage2 (Mass)       # 天平砝码
├── stage3 (Volume)     # 量筒排水法
├── stage4 (Density)    # 密度计算
└── end-screen          # 结算
```

**Stage 4 特殊规范：**
- 步骤1：正视图（长×高）+ 顶面视图（宽）
- 步骤2：微型天平示意
- 步骤3：量筒动画（盒子放入→液面上升）

### 数学游戏结构

```
├── intro-screen
├── level1 (密码破解)    # 因数倍数判断
├── level2 (整除特征)    # 数字网格点击
├── level3 (GCD暗号)     # 最大公因数
├── level4 (质数搜捕)    # 密码输入
└── result-screen        # 特工评级
```

---

## 教程文件规范

### 内容结构

每章包含：
1. **理论讲解**：CSS动画演示（刻度尺/天平/量筒）
2. **例题**：3道逐步引导
3. **随堂测验**：3题即时反馈
4. **公式总结**：`.formula-box` 高亮框

### 导航

底部固定导航栏：
```
Ch1 长度测量 → Ch2 质量测量 → Ch3 体积测量 → Ch4 密度计算 → 🎮 进入特工装备室
```

---

## Git提交规范

```
feat(courseware): 物理/数学课件v2.0升级 - Stage4顶面视图+移动端适配+章节跳转
```

**格式：** `type(scope): subject`
- `type`: feat / fix / docs / style
- `scope`: courseware / physics-game / math-game / tutorial
- `subject`: 做了什么（动词开头，不超过50字）

---

## QA检查清单

发布前必须验证：

- [ ] 4个文件 HTTP 200
- [ ] 物理游戏包含 `s4-top-view`
- [ ] 物理游戏包含 `stage-nav-panel` + `toggleStageNav`
- [ ] 数学游戏包含 `level-nav-panel` + `toggleLevelNav`
- [ ] 全部 @media 断点存在
- [ ] HTML 语法正确（可通过解析器）

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-04 | 初始课件系统 |
| v1.1 | 2026-05-04 | L1限时改为10秒，超时不再自动失败 |
| v2.0 | 2026-05-04 | Stage4顶面视图、移动端适配5断点、章节跳转导航 |
