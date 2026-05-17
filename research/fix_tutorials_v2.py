#!/usr/bin/env python3
"""
课件 Tutorial 组件修复脚本 v2 — 处理多种HTML结构
"""

import os, re, sys

BASE_DIR = "/root/.openclaw/workspace/portfolio-blog/research"

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

CHALLENGE_BTN_STYLE = 'padding:10px 28px;font-size:14px;'

def count_sections(content):
    """统计文件中有多少个单元/section"""
    # id="ch1", id="ch2" 等
    ch_matches = re.findall(r'id="ch(\d+)"', content)
    if ch_matches:
        return max(int(m) for m in ch_matches)
    # data-sec
    sec_matches = re.findall(r'data-sec="(\d+)"', content)
    if sec_matches:
        return max(int(m) for m in sec_matches) + 1
    # <section> 标签
    section_count = content.count('<section')
    if section_count > 1:
        return section_count
    # class="card"
    card_count = content.count('class="card"') + content.count('class="card section"')
    if card_count > 1:
        return card_count
    # class="section"
    div_section = len(re.findall(r'<div class="section"', content))
    if div_section > 1:
        return div_section
    return 4

def add_progress_css(content):
    """在 </style> 前添加进度条 CSS"""
    if '.progress-bar {' in content and '.progress-seg' in content:
        return content
    if '</style>' in content:
        return content.replace('</style>', PROGRESS_CSS + '\n</style>')
    return content

def make_progress_html(num_segments):
    segs = '\n'.join([f'  <div class="progress-seg{" active" if i == 0 else ""}"></div>' for i in range(num_segments)])
    return f'<div class="progress-bar" id="progress-bar">\n{segs}\n</div>\n'

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    # 1. 添加进度条CSS（如果缺少）
    if '.progress-bar {' not in content or '.progress-seg' not in content:
        content = add_progress_css(content)
        if content != original:
            changes.append("添加进度条CSS")
            original = content
    
    # 2. 添加进度条HTML（如果缺少）
    if '<div class="progress-bar"' not in content and 'class="progressBar"' not in content and 'id="progress-bar"' not in content:
        num = count_sections(content)
        progress_html = make_progress_html(num)
        
        # 策略A: 有 title-bar，在 title-bar 后、第一个 card/section 前插入
        if 'class="title-bar"' in content:
            # 找到 title-bar 的结束 </div>，然后在后面的第一个 <div class="card" 或 <div class="section" 或 <div class="nav-bar" 前插入
            pattern = r'(class="title-bar"[^>]*>.*?)(</div>\s*)(<div class="(?:card|section|nav-bar)|<!-- |\n\s*<div)'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                insert_pos = match.end(2)
                content = content[:insert_pos] + '\n' + progress_html + '\n' + content[insert_pos:]
                changes.append(f"添加进度条({num}单元)")
            else:
                # 备选：在 title-bar 结束后的任意位置插入
                pattern2 = r'(class="title-bar"[^>]*>.*?)(</div>)'
                matches = list(re.finditer(pattern2, content, re.DOTALL))
                if matches:
                    # 找最后一个匹配（完整的title-bar闭合）
                    last_match = matches[-1]
                    # 在其后插入
                    insert_pos = last_match.end()
                    content = content[:insert_pos] + '\n' + progress_html + '\n' + content[insert_pos:]
                    changes.append(f"添加进度条({num}单元)")
        
        # 策略B: 有 <header> 标签，在 </header> 后插入
        elif '<header' in content and '</header>' in content:
            header_end = content.find('</header>')
            if header_end != -1:
                insert_pos = header_end + len('</header>')
                content = content[:insert_pos] + '\n' + progress_html + '\n' + content[insert_pos:]
                changes.append(f"添加进度条({num}单元)")
        
        # 策略C: 有 <div id="app">，在其后插入
        elif 'id="app"' in content:
            pattern = r'(id="app"[^>]*>)'
            match = re.search(pattern, content)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + '\n' + progress_html + '\n' + content[insert_pos:]
                changes.append(f"添加进度条({num}单元)")
        
        # 策略D: 在第一个 <div> 容器后插入
        else:
            # 找第一个有意义的 div 开始（不是 corner 装饰元素）
            pattern = r'(<div[^&gt;]*class="[^"]*(?:container|main|content|wrapper)[^"]*"[^&gt;]*>)'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + '\n' + progress_html + '\n' + content[insert_pos:]
                changes.append(f"添加进度条({num}单元)")
    
    if content != original:
        original = content
    
    # 3. 添加/替换挑战按钮
    if '去挑战模式' not in content:
        # 策略A: 有 title-bar，在其中插入按钮
        if 'class="title-bar"' in content:
            # 检查是否已有挑战类按钮
            has_old_btn = '挑战' in content and 'href="index.html"' in content
            
            if has_old_btn:
                # 替换现有的挑战按钮为"去挑战模式"
                # 替换包含"挑战"和"index.html"的按钮/链接
                content = re.sub(
                    r'(<(?:a|button)[^&gt;]*href="index\.html"[^&gt;]*>)(?:.*?)挑战.*?(?:</a>|</button>)',
                    r'<a class="btn" href="index.html" style="' + CHALLENGE_BTN_STYLE + r'">🎮 去挑战模式</a>',
                    content,
                    flags=re.DOTALL
                )
                if '去挑战模式' in content:
                    changes.append("替换挑战按钮")
            else:
                # 在 title-bar 的闭合 </div> 前插入按钮
                pattern = r'(class="title-bar"[^>]*>.*?)(</div>)'
                matches = list(re.finditer(pattern, content, re.DOTALL))
                if matches:
                    last_match = matches[-1]
                    # 在最后一个 </div> 前插入按钮
                    insert_pos = last_match.start(2)
                    btn_html = '<div style="margin-top:12px;"><a class="btn" href="index.html" style="' + CHALLENGE_BTN_STYLE + r'">🎮 去挑战模式</a></div>'
                    content = content[:insert_pos] + btn_html + content[insert_pos:]
                    changes.append("添加挑战按钮")
        
        # 策略B: 有 <header>，在其中插入按钮
        elif '<header' in content and '</header>' in content:
            header_end = content.find('</header>')
            if header_end != -1:
                # 在 header 闭合前插入
                insert_pos = header_end
                btn_html = '<div style="text-align:center;margin-top:16px;"><a class="btn" href="index.html" style="' + CHALLENGE_BTN_STYLE + r'">🎮 去挑战模式</a></div>'
                content = content[:insert_pos] + btn_html + content[insert_pos:]
                changes.append("添加挑战按钮(header)")
        
        # 策略C: 在 <div id="app"> 后插入
        elif 'id="app"' in content:
            # 如果有进度条刚插入，在进度条后插入；否则在 app 后插入
            if '<div class="progress-bar"' in content:
                pb_end = content.find('</div>\n', content.find('<div class="progress-bar"'))
                if pb_end != -1:
                    insert_pos = pb_end + len('</div>\n')
                    btn_html = '<div style="text-align:center;margin-bottom:24px;"><a class="btn" href="index.html" style="' + CHALLENGE_BTN_STYLE + r'">🎮 去挑战模式</a></div>\n'
                    content = content[:insert_pos] + btn_html + content[insert_pos:]
                    changes.append("添加挑战按钮")
            else:
                pattern = r'(id="app"[^>]*>)'
                match = re.search(pattern, content)
                if match:
                    insert_pos = match.end()
                    btn_html = '<div style="text-align:center;margin-bottom:24px;"><a class="btn" href="index.html" style="' + CHALLENGE_BTN_STYLE + r'">🎮 去挑战模式</a></div>\n'
                    content = content[:insert_pos] + btn_html + content[insert_pos:]
                    changes.append("添加挑战按钮")
    
    if changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return changes

def main():
    # 处理所有 tutorial.html 文件
    subjects = [
        ('junior-physics/courseware-physics', '物理'),
        ('junior-math/courseware-math', '数学'),
    ]
    
    total_changed = 0
    for subdir, name in subjects:
        base = os.path.join(BASE_DIR, subdir)
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            if 'tutorial.html' in files:
                filepath = os.path.join(root, 'tutorial.html')
                changes = fix_file(filepath)
                if changes:
                    rel = filepath.replace(BASE_DIR + '/', '')
                    print(f"✓ {rel}: {', '.join(changes)}")
                    total_changed += 1
    
    print(f"\n共修改 {total_changed} 个文件")

if __name__ == '__main__':
    main()
