# 物理课件页面修改规则

> 汇总 2026-05-19 ~ 2026-05-20 第一章「测量」全部修复经验，作为后续章节的制作/审查规范。

---

## 一、视觉与答案必须像素级对齐

**规则 1.1 — 物体位置与答案文字一致**

尺子、天平、量筒等可视化元素的 **CSS 像素位置** 必须与下方文字答案完全匹配。

| 错误示例 | 正确做法 |
|---------|---------|
| 物体 `left:60px; width:120px`，答案写"3.25 cm" | 先算：有效宽度 ÷ 刻度单位 = 每单位像素，再反推 `left` 和 `width` |
| 刻度标记 0/1/2/3/4，物体跨了 2 个单位，答案写 3.25 | 刻度系统、物体跨度、答案文字三者统一 |

**计算公式**：
```
有效宽度 = 容器宽 - paddingLeft - paddingRight
每单位像素 = 有效宽度 / 刻度范围
物体 left = 起点刻度 × 每单位像素 + paddingLeft - 物体偏移修正
物体 width = (终点刻度 - 起点刻度) × 每单位像素
```

**规则 1.2 — 刻度系统内部自洽**

- 刻度线数量、数字标记、有效宽度三者必须匹配
- `justify-content: space-between` 分布的刻度线，首尾的间距由容器 padding 控制，不能搞错

---

## 二、交互优于静态暴露

**规则 2.1 — 答案默认隐藏，交互后显示**

| 错误 | 正确 |
|------|------|
| 答案文字直接写在 HTML 中，页面加载即可见 | 答案放入独立 div，`opacity: 0` + `transition: opacity 0.5s`，点击/操作后 `opacity: 1` |
| "? cm（点击查看读数）" 但没有绑定任何 click 事件 | 必须绑定 `onclick` 函数，且函数体内同时更新读数区和答案区 |

**推荐实现**：
```html
<div class="ruler-viz" onclick="showAnswer()" style="cursor:pointer;">
  <div class="readout">? cm（点击查看读数）</div>
  ...
</div>
<div id="answer" style="opacity:0; transition:opacity 0.5s;">
  答案文字...
</div>

<script>
function showAnswer() {
  document.querySelector('.readout').innerHTML = '✅ 长度 = 2.00 cm';
  document.getElementById('answer').style.opacity = '1';
}
</script>
```

---

## 三、样式体系严格统一

**规则 3.1 — 使用项目统一的 CSS 类名**

本课件的科幻主题已定义完整类名体系，**禁止**使用无样式的遗留类名：

| ✅ 使用 | ❌ 禁止 | 说明 |
|--------|--------|------|
| `.quiz-box` | — | 测验整体容器（深色背景+边框） |
| `.quiz-title` | — | 测验标题 |
| `.quiz-question` | — | 题目文字 |
| `.quiz-options` | — | 选项按钮容器（flex纵向） |
| `.quiz-btn` | `.quiz-option` | 选项按钮（蓝色边框+hover发光） |
| `.quiz-feedback` | `.feedback` | 反馈文字区 |
| `.quiz-btn.correct` / `.quiz-btn.wrong` | `.feedback.ok` / `.feedback.wrong` | 正确/错误状态 |
| `.btn` / `.btn-ghost` / `.btn-warn` | — | 通用按钮体系 |

**规则 3.2 — 复用现有函数，禁止重复造轮子**

- 同一页面多个测验应共用同一个 `checkQuiz(btn, qid, ans, isCorrect, msg)` 函数
- 禁止为每道题写独立的 `checkQ1()` `checkQ2()` ... `checkQ5()`

---

## 四、内容严格遵守教材边界

**规则 4.1 — 不超纲**

| 章节 | 允许内容 | 禁止混入 |
|------|---------|---------|
| 第一章「测量」 | 刻度尺读数、质量测量（天平）、体积量筒、密度计算 | 游标卡尺、螺旋测微器、误差分析 |

- 游标卡尺属于高中/竞赛内容，**八年级第一章不得出现**
- 不确定时，以 **实体课本目录** 为最终依据，不依赖网络搜索的二手信息

---

## 五、代码清理：修复后必须检查残留

**规则 5.1 — 全局搜索确认无遗留**

HTML 文件底部常存在历史残留的重复 JS 代码块，修复后必须执行：

```bash
grep -n "旧类名\|旧函数名\|旧元素ID" tutorial.html
```

本次清理的残留类型：
- 重复的 Canvas IIFE 块（rulerCanvas ×4、vernierCanvas ×4）
- 废弃的独立测验函数（`checkQ1_1` ~ `checkQ1_5`）
- 已移除实验的按钮回调（`setVernier`）

**规则 5.2 — 删除与替换的区别**

- 如果只是隐藏：`display:none` 或移出 DOM 但 JS 仍在 → 仍会执行报错
- 正确做法：**彻底删除** HTML 结构 + 关联 JS + CSS，不留尸体

---

## 六、部署与验证流程

**规则 6.1 — GitHub Pages CDN 缓存时间**

```
git push 后 → 等待 15~25 秒 → CDN 同步完成 → 再执行 QA 验证
```

提前验证会拿到旧版本，导致误判。

**规则 6.2 — QA 验证清单**

| 检查项 | 方法 | 通过标准 |
|--------|------|---------|
| 页面可访问 | `curl -sI URL` | HTTP 200 |
| 新内容已同步 | `curl -s URL \| grep "新关键字"` | 返回匹配 |
| 旧内容已清除 | `curl -s URL \| grep "旧关键字"` | 返回空 |
| 样式一致性 | 浏览器截图对比 | 按钮/反馈颜色与主题一致 |
| 交互逻辑 | 手动点击测试 | 点击后答案正确显示 |

**规则 6.3 — 编辑工具选择**

| 场景 | 推荐工具 | 不推荐 |
|------|---------|--------|
| 单行/小范围修改 | `edit` 工具 | — |
| 大段 HTML 批量替换（>20 行） | Python 脚本 + `write` | `edit` 工具（匹配易失败） |
| 多处分散修改 | Python 脚本（正则/replace） | 多次 `edit` 调用 |
| 清理残留代码 | `grep` 定位 + Python 脚本删除 | 手工逐行删除 |

---

## 七、快速检查清单（每次修改后必做）

- [ ] 视觉元素（尺子/天平/物体）的 CSS 位置与答案文字一致
- [ ] 答案默认隐藏，有交互触发显示
- [ ] 所有按钮使用 `.quiz-btn`，无 `.quiz-option` 残留
- [ ] 所有反馈使用 `.quiz-feedback`，无 `.feedback` 残留
- [ ] 内容不超纲（对照实体课本目录）
- [ ] `grep` 确认无历史残留 JS 代码块
- [ ] git push 后等待 20 秒再 QA 验证
- [ ] curl 验证线上版本包含新内容、不包含旧内容

---

*文档版本: v1.0*
*适用范围: 初中物理课件（courseware-physics）*
*最后更新: 2026-05-20*
