#!/usr/bin/env python3
"""
为archive和backups页面添加移动端响应式CSS
"""

import os
import re
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace/portfolio-blog")

# 剩余的archive和backups页面
PAGES_TO_FIX = [
    'archive/previews/preview-v4.html',
    'archive/status-monitor-old-versions/score-only.html',
    'archive/status-monitor-old-versions/simple.html',
    'archive/status-monitor-old-versions/test.html',
    'backups/status-monitor/backup-v5.34-20260318/deprecated-systems/index.html',
    'backups/status-monitor/backup-v5.34-20260318/legacy-versions/cognitive-status-split.html',
    'backups/status-monitor/backup-v5.34-20260318/whitepaper/whitepaper.html',
    'status-monitor/whitepaper.html',
]

# 简洁的移动端CSS模板
MOBILE_CSS_TEMPLATE = '''
        /* 移动端适配 */
        @media (max-width: 768px) {
            body {
                font-size: 16px;
                padding: 10px;
            }
            .container, main, section {
                max-width: 100%;
                padding: 15px;
            }
            h1 { font-size: 24px; }
            h2 { font-size: 20px; }
            p, li {
                font-size: 16px;
                line-height: 1.6;
            }
            a, button {
                min-height: 44px;
                min-width: 44px;
            }
            img {
                max-width: 100%;
                height: auto;
            }
        }
'''

def add_mobile_css(filepath):
    """为单个文件添加移动端CSS"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return False, f"读取失败: {e}"
    
    # 检查是否已有媒体查询
    if '@media' in content:
        return True, "已有媒体查询"
    
    # 查找</style>标签
    style_end_match = list(re.finditer(r'</style>', content, re.IGNORECASE))
    if not style_end_match:
        return False, "找不到</style>标签"
    
    # 在最后一个</style>前插入移动端CSS
    last_style_end = style_end_match[-1].start()
    new_content = content[:last_style_end] + MOBILE_CSS_TEMPLATE + content[last_style_end:]
    
    # 写回文件
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "已添加移动端CSS"
    except Exception as e:
        return False, f"写入失败: {e}"

def main():
    print("开始为archive/backups页面添加移动端CSS...\n")
    
    fixed = 0
    skipped = 0
    failed = 0
    
    for page_path in PAGES_TO_FIX:
        filepath = WORKSPACE / page_path
        if not filepath.exists():
            print(f"❌ 文件不存在: {page_path}")
            failed += 1
            continue
        
        success, msg = add_mobile_css(filepath)
        status = "✅" if success else "❌"
        print(f"{status} {page_path}: {msg}")
        
        if success and msg == "已添加移动端CSS":
            fixed += 1
        elif success:
            skipped += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"处理完成: 已修复 {fixed}, 跳过 {skipped}, 失败 {failed}")

if __name__ == "__main__":
    main()
