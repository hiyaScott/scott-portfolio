# Shrimp Jetton 设计系统 v1.0

基于认知监控页面 (cognitive-status.html) 提取的完整设计规范

---

## 🎨 设计理念

**风格定位**: 科技感深色界面 / 数据仪表盘 / 赛博朋克微光

**核心特征**:
- 深邃黑色背景 (#0a0a0f)
- 微妙的发光效果与渐变
- 功能性色彩编码 (状态可视化)
- 数据优先的排版层次

---

## 📐 Design Tokens

### 颜色系统

#### 背景色
| Token | 值 | 用途 |
|-------|-----|------|
| `--bg-primary` | `#0a0a0f` | 页面主背景 |
| `--bg-card` | `rgba(255,255,255,0.02)` | 卡片背景 |
| `--bg-elevated` | `rgba(35,35,45,0.98)` | 提升层背景(仪表盘) |
| `--bg-hover` | `rgba(255,255,255,0.06)` | 悬停状态 |

#### 边框色
| Token | 值 | 用途 |
|-------|-----|------|
| `--border-subtle` | `rgba(255,255,255,0.05)` | 微妙边框 |
| `--border-default` | `#222` | 默认卡片边框 |
| `--border-hover` | `#444` | 悬停边框 |

#### 状态色彩 (四色系统)
| 状态 | 主色 | 发光色 | 背景色 |
|------|------|--------|--------|
| **Idle/成功** | `#4ade80` | `rgba(34,197,94,0.6)` | `rgba(34,197,94,0.15)` |
| **Low/信息** | `#60a5fa` | `rgba(59,130,246,0.6)` | `rgba(59,130,246,0.15)` |
| **Medium/警告** | `#facc15` | `rgba(234,179,8,0.6)` | `rgba(234,179,8,0.15)` |
| **High/危险** | `#f87171` | `rgba(239,68,68,0.6)` | `rgba(239,68,68,0.15)` |

#### 强调色
| Token | 值 | 用途 |
|-------|-----|------|
| `--accent-cyan` | `#00ffff` | 主要强调色、倒计时、高亮 |
| `--accent-white` | `rgba(255,255,255,0.9)` | 主文字 |
| `--text-secondary` | `#888` | 次要文字 |
| `--text-muted` | `#666` | 辅助文字 |

### 字体系统

#### 字体栈
```css
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'SF Mono', 'JetBrains Mono', monospace;
```

#### 字号规范
| 级别 | 大小 | 字重 | 用途 |
|------|------|------|------|
| **Display** | 4.5rem (PC) / 3rem (Mobile) | 900 | 大数字显示 |
| **H1** | 1.4rem | 800 | 模块标题 |
| **H2** | 1.1rem | 700 | 弹窗标题 |
| **Body** | 0.9-1rem | 400 | 正文 |
| **Caption** | 0.8rem | 400 | 标签、小字 |
| **Data** | 0.9rem | 600 | 数据值 |
| **Micro** | 9-10px | 400 | 状态栏标签 |

### 间距系统

| Token | 值 | 用途 |
|-------|-----|------|
| `--space-xs` | 4px | 紧凑间距 |
| `--space-sm` | 8px | 小间距 |
| `--space-md` | 12-16px | 标准间距 |
| `--space-lg` | 20-24px | 大间距 |
| `--space-xl` | 30px | 章节间距 |

### 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| `--radius-sm` | 6-8px | 按钮、小元素 |
| `--radius-md` | 10-12px | 卡片、输入框 |
| `--radius-lg` | 16-20px | 大卡片、仪表盘 |
| `--radius-full` | 50% | 圆形元素 |

### 阴影与光效

```css
/* 卡片阴影 */
--shadow-card: 0 10px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(0,0,0,0.5);

/* 发光效果 */
--glow-idle: 0 0 20px rgba(34,197,94,0.6);
--glow-low: 0 0 20px rgba(59,130,246,0.6);
--glow-medium: 0 0 20px rgba(234,179,8,0.6);
--glow-high: 0 0 20px rgba(239,68,68,0.6);

/* 内阴影 (屏幕效果) */
--shadow-inset: inset 0 2px 4px rgba(0,0,0,0.5);
```

---

## 🧩 组件库

### 1. 容器组件

#### Main Container
```css
.container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
}
```

#### Card (基础卡片)
```css
.card {
    background: rgba(255,255,255,0.02);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #222;
    margin-bottom: 24px;
}
```

#### Elevated Card (仪表盘式)
```css
.card-elevated {
    background: linear-gradient(180deg, rgba(35,35,45,0.98) 0%, rgba(25,25,35,0.99) 100%);
    border-radius: 20px;
    padding: 20px 24px;
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.05), 
                0 10px 40px rgba(0,0,0,0.5), 
                0 0 0 1px rgba(0,0,0,0.5);
}
```

### 2. 数据展示组件

#### Metric Card (指标卡片)
```css
.metric-card {
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    padding: 12px 8px;
    border: 1px solid #222;
    text-align: center;
    transition: all 0.2s ease;
}
.metric-card:hover {
    background: rgba(255,255,255,0.06);
    border-color: #444;
    transform: translateY(-2px);
}
.metric-label {
    font-size: 10px;
    color: #666;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 18px;
    font-weight: 700;
    font-family: 'SF Mono', monospace;
}
```

#### Status Badge (状态徽章)
```css
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(10,10,15,0.8) 100%);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
    font-size: 0.95rem;
    font-weight: 600;
}
.status-badge::before {
    content: '';
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: currentColor;
    box-shadow: 0 0 15px currentColor, 0 0 30px currentColor;
}
```

### 3. 交互组件

#### Button (基础按钮)
```css
.btn {
    background: rgba(255,255,255,0.1);
    border: none;
    color: #fff;
    padding: 10px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}
.btn:hover {
    background: rgba(255,255,255,0.2);
}
```

#### Tab Button (标签按钮)
```css
.tab-btn {
    display: block;
    padding: 14px 8px;
    text-align: center;
    font-size: 0.85rem;
    color: #666;
    background: transparent;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
    cursor: pointer;
}
.tab-btn:hover {
    color: #999;
    background: rgba(255,255,255,0.02);
}
.tab-btn.active {
    color: #fff;
    background: rgba(255,255,255,0.05);
    border-bottom-color: #00ffff;
}
```

#### Time Range Button (时间选择按钮)
```css
.time-btn {
    padding: 6px 12px;
    font-size: 12px;
    border: 1px solid #333;
    background: transparent;
    color: #666;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.time-btn:hover {
    border-color: #555;
    color: #999;
}
.time-btn.active {
    background: rgba(0,255,255,0.1);
    border-color: #00ffff;
    color: #00ffff;
}
```

### 4. 表单组件

#### Input (输入框)
```css
.input {
    background: rgba(255,255,255,0.03);
    border: 1px solid #222;
    border-radius: 10px;
    padding: 12px 16px;
    color: #fff;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}
.input:focus {
    outline: none;
    border-color: #00ffff;
    background: rgba(255,255,255,0.05);
}
```

### 5. 列表组件

#### List Item (列表项)
```css
.list-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    margin-bottom: 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.2s ease;
}
.list-item:hover {
    background: rgba(255,255,255,0.05);
    border-color: rgba(255,255,255,0.1);
}
```

---

## 📱 响应式规范

### 断点
```css
/* 移动端 */
@media (max-width: 600px) {
    /* 手机端样式 */
}

/* 平板端 */
@media (max-width: 900px) {
    /* 平板适配 */
}
```

### 移动端适配要点
- 大数字字体缩小 (4.5rem → 3rem)
- 容器宽度调整 (100px → 70px)
- 保持触摸友好的点击区域 (最小44px)
- 网格列数自适应

---

## 🎬 动效规范

### 过渡时间
| 场景 | 时长 | 缓动函数 |
|------|------|----------|
| 悬停反馈 | 0.2s | ease |
| 状态切换 | 0.3s | ease |
| 弹窗出现 | 0.3s | ease |
| 数字变化 | 0.5s | ease-out |

### 常用动画
```css
/* 淡入上浮 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* 缩放出现 */
@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.9); }
    to { opacity: 1; transform: scale(1); }
}

/* 脉冲发光 */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
```

---

## 🔧 使用建议

### 何时使用哪种卡片样式？

| 场景 | 推荐组件 | 原因 |
|------|----------|------|
| 普通内容展示 | Card | 简洁、通用 |
| 数据仪表盘 | Card-Elevated | 突出、有层次感 |
| 关键指标 | Metric Card | 紧凑、数据优先 |
| 状态显示 | Status Badge | 带指示器、醒目 |

### 颜色使用原则
1. **四色状态系统** 专用于表示系统状态/负载等级
2. **青色 (#00ffff)** 用于强调、交互元素
3. **避免过多颜色** - 保持科技感的克制

### 布局建议
- 最大宽度控制在 700-900px，保证阅读舒适度
- 使用 grid/flex 实现响应式布局
- 保持一致的间距节奏 (8px 倍数)

---

## 📦 文件组织建议

```
portfolio-blog/
├── css/
│   ├── design-system.css    # 设计系统基础
│   ├── components.css       # 组件样式
│   └── utilities.css        # 工具类
├── js/
│   └── components.js        # 交互组件
└── pages/
    └── *.html              # 各页面统一引用
```

### 引用方式
```html
<link rel="stylesheet" href="/css/design-system.css">
<link rel="stylesheet" href="/css/components.css">
```

---

## 🔄 版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-03-15 | 基于 cognitive-status.html v5.19.7 提取 |

---

**下次更新建议**: 随着更多页面采用此设计系统，持续收拢通用模式，补充新的组件变体。
