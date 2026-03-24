#!/usr/bin/env python3
"""
为kimi-claw技能页面添加移动端响应式CSS
"""

import os
import re
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace/portfolio-blog")

# 需要添加媒体查询的kimi-claw页面
KIMI_PAGES_TO_FIX = [
    'kimi-claw/ai-shortfilm/index.html',
    'kimi-claw/ascii-art/index.html',
    'kimi-claw/ascii-art/shrimp-jetton-preview.html',
    'kimi-claw/ascii-art/shrimp-logo.html',
    'kimi-claw/audio-design/index.html',
    'kimi-claw/bambu-3dprint/index.html',
    'kimi-claw/coding-dev/index.html',
    'kimi-claw/cross-border-ecommerce/index.html',
    'kimi-claw/data-analysis/index.html',
    'kimi-claw/deploy-sentinel/index.html',
    'kimi-claw/doc-processing/index.html',
    'kimi-claw/docs-engineering/index.html',
    'kimi-claw/game-design/index.html',
    'kimi-claw/github-automation/index.html',
    'kimi-claw/index.html',
    'kimi-claw/math-olympiad/index.html',
    'kimi-claw/media-processing/index.html',
    'kimi-claw/openviking/index.html',
    'kimi-claw/qa/index.html',
    'kimi-claw/screenwriting/index.html',
    'kimi-claw/skill-creator/index.html',
    'kimi-claw/task-scheduler/index.html',
    'kimi-claw/three-kingdoms/characters.html',
    'kimi-claw/three-kingdoms/index.html',
]

# 标准移动端CSS模板（针对内容页面）
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
            h3 { font-size: 18px; }
            p, li, td, th {
                font-size: 16px;
                line-height: 1.6;
            }
            a, button, .btn, [role="button"] {
                min-height: 44px;
                min-width: 44px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            }
            img, video, iframe {
                max-width: 100%;
                height: auto;
            }
            table {
                display: block;
                overflow-x: auto;
                white-space: nowrap;
            }
            pre, code {
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 14px;
            }
        }
        @media (max-width: 480px) {
            body {
                font-size: 16px;
                padding: 5px;
            }
            .container, main, section {
                padding: 10px;
            }
            h1 { font-size: 20px; }
            h2 { font-size: 18px; }
            h3 { font-size: 16px; }
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
    print("开始为kimi-claw页面添加移动端CSS...\n")
    
    fixed = 0
    skipped = 0
    failed = 0
    
    for page_path in KIMI_PAGES_TO_FIX:
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
