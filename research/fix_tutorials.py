#!/usr/bin/env python3
"""
课件 Tutorial 统一修复脚本
1. 术语统一: "章"/"节" → "单元"（导航按钮）
2. 添加"去挑战模式"按钮（标题栏内）
3. 添加单元进度条
"""

import os, re, sys

BASE_DIR = "/root/.openclaw/workspace/portfolio-blog/research"

# ========== 标准组件模板 ==========

# 进度条 CSS（插入到 </style> 前）
PROGRESS_CSS = """
/* Progress bar */
.progress-bar {
  display: flex; gap: 8px;
  margin-bottom: 32px;
  justify-content: center;
}
.progress-seg {
  width: 60px; height: 4px;
  background: rgba(88,96,112,0.3);
  border-radius: 2px;
  transition: all 0.3s;
}
.progress-seg.active { background: var(--accent); box-shadow: 0 0 10px var(--accent); }
.progress-seg.done { background: var(--success); }
"""

# 导航按钮 CSS（如果文件没有 .nav-btns 样式）
NAV_BTN_CSS = """
/* Nav buttons */
.nav-btns {
  display: flex; gap: 12px;
  justify-content: center;
  margin-top: 32px;
}
.nav-btn {
  background: transparent;
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.3s;
}
.nav-btn:hover:not(:disabled) { background: var(--accent); color: var(--bg); }
.nav-btn:disabled { opacity: 0.3; cursor: not-allowed; border-color: var(--text-dim); color: var(--text-dim); }
"""

def fix_terminology(content):
    """修复术语：导航按钮中的章/节 → 单元"""
    # 只替换按钮文本，不替换正文中的"章节"等词
    content = re.sub(r'(←\s*)上一节', r'\1上一单元', content)
    content = re.sub(r'下一节(\s*→)', r'下一单元\1', content)
    content = re.sub(r'(←\s*)上一章', r'\1上一单元', content)
    content = re.sub(r'下一章(\s*→)', r'下一单元\1', content)
    # 也处理 chapter-num 中的 "第 X / Y 章"
    content = re.sub(r'第\s*(\d+)\s*/\s*(\d+)\s*章', r'第 \1 / \2 单元', content)
    return content

def add_challenge_button(content):
    """在 title-bar 内添加"去挑战模式"按钮"""
    # 检查是否已有挑战按钮
    if '挑战模式' in content and 'href="index.html"' in content:
        return content  # 已有
    
    # 在 title-bar 的 </div> 前添加按钮
    # 匹配模式：<div class="title-bar"> ... </div>
    pattern = r'(<div class="title-bar"[^>]*>.*?)(</div>\s*<div class="progress-bar)'
    replacement = r'\1<div style="margin-top:12px;"><a class="btn btn-warn" href="index.html" style="padding:10px 28px;font-size:14px;">🎮 去挑战模式</a></div>\2'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    if new_content != content:
        return new_content
    
    # 备选：在 title-bar 后插入
    pattern2 = r'(</div>\s*)(<div class="progress-bar|<div class="card)'
    replacement2 = r'\1<div style="text-align:center;margin-bottom:24px;"><a class="btn" href="index.html" style="padding:10px 28px;font-size:14px;display:inline-block;text-decoration:none;">🎮 去挑战模式</a></div>\2'
    new_content = re.sub(pattern2, replacement2, content, count=1)
    return new_content

def add_progress_bar(content, num_segments=4):
    """在 title-bar 后添加进度条"""
    if 'progress-bar' in content or 'progressBar' in content:
        return content  # 已有
    
    # 在 title-bar </div> 后插入进度条
    segs = '\n'.join([f'    <div class="progress-seg{" active" if i == 0 else ""}"></div>' for i in range(num_segments)])
    progress_html = f'''<div class="progress-bar" id="progress-bar">
{segs}
</div>
'''
    
    pattern = r'(</div>\s*)(<div class="card)'
    replacement = r'\1' + progress_html + r'\2'
    new_content = re.sub(pattern, replacement, content, count=1)
    return new_content

def add_progress_css(content):
    """在 </style> 前添加进度条 CSS"""
    if '.progress-bar {' in content:
        return content  # 已有
    return content.replace('</style>', PROGRESS_CSS + '\n</style>')

def add_nav_css(content):
    """在 </style> 前添加导航按钮 CSS（如果没有）"""
    if '.nav-btns {' in content:
        return content
    return content.replace('</style>', NAV_BTN_CSS + '\n</style>')

def count_sections(content):
    """粗略统计文件中有多少个单元/section"""
    # 数 id="ch1", id="ch2" 等
    ch_matches = re.findall(r'id="ch(\d+)"', content)
    if ch_matches:
        return max(int(m) for m in ch_matches)
    # 数 data-sec
    sec_matches = re.findall(r'data-sec="(\d+)"', content)
    if sec_matches:
        return max(int(m) for m in sec_matches) + 1
    # 数 <div class="card section" 或 <div class="card"
    card_count = content.count('<div class="card"') + content.count('<div class="card section"')
    if card_count > 1:
        return card_count
    return 4  # 默认4个单元

def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. 术语修复
    content = fix_terminology(content)
    if content != original:
        changes.append("术语修复")
    
    # 2. 添加进度条 CSS（如果缺少）
    if '.progress-bar {' not in content:
        content = add_progress_css(content)
        changes.append("添加进度条CSS")
    
    # 3. 添加导航按钮 CSS（如果缺少）
    if '.nav-btns {' not in content and 'nav-btn' in content:
        content = add_nav_css(content)
        changes.append("添加导航CSS")
    
    # 4. 添加进度条 HTML（如果缺少）
    if 'progress-bar' not in content and 'progressBar' not in content:
        num = count_sections(content)
        content = add_progress_bar(content, num)
        changes.append(f"添加进度条({num}单元)")
    
    # 5. 添加挑战按钮（如果缺少）
    if '去挑战模式' not in content:
        content = add_challenge_button(content)
        changes.append("添加挑战按钮")
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return changes
    return []

def main():
    subjects = [
        ('junior-physics/courseware-physics', '物理'),
        ('junior-math/courseware-math', '数学'),
    ]
    
    total_changed = 0
    for subdir, name in subjects:
        base = os.path.join(BASE_DIR, subdir)
        if not os.path.exists(base):
            continue
        print(f"\n{'='*60}")
        print(f"处理 {name}")
        print(f"{'='*60}")
        for root, dirs, files in os.walk(base):
            if 'tutorial.html' in files:
                filepath = os.path.join(root, 'tutorial.html')
                changes = process_file(filepath)
                if changes:
                    rel = filepath.replace(BASE_DIR + '/', '')
                    print(f"  ✓ {rel}: {', '.join(changes)}")
                    total_changed += 1
                else:
                    rel = filepath.replace(BASE_DIR + '/', '')
                    print(f"  - {rel}: 无需修改")
    
    print(f"\n共修改 {total_changed} 个文件")

if __name__ == '__main__':
    main()
