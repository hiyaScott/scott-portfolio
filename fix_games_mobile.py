#!/usr/bin/env python3
"""
为游戏页面添加移动端响应式CSS
"""

import os
import re
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace/portfolio-blog")

# 需要添加媒体查询的游戏页面（从之前的分析结果）
GAMES_TO_FIX = [
    "games/bot-coder/index.html",
    "games/card-alchemist/index.html",
    "games/chain-reaction/index.html",
    "games/chroma-blaster/index.html",
    "games/circuit-connect/index.html",
    "games/gravity-flip/index.html",
    "games/gravity-slingshot/index.html",
    "games/grid-dominion/index.html",
    "games/magnetic-snap/index.html",
    "games/memory-maze/index.html",
    "games/minesweeper/index.html",
    "games/mirror-maze/index.html",
    "games/neon-defense/index.html",
    "games/quantum-split/index.html",
    "games/rhythm-parkour/index.html",
    "games/shadow-puzzle/index.html",
    "games/sonic-maze/index.html",
    "games/thermal-expansion/index.html",
    "games/time-rewind/index.html",
    "games/time-slice/index.html",
    "games/wave-warrior/index.html",
    "games/who-is-spy/index.html",
    "games/word-alchemy/index.html",
]

# 标准移动端CSS模板
MOBILE_CSS_TEMPLATE = '''
        /* 移动端适配 */
        @media (max-width: 768px) {
            body {
                font-size: 16px;
            }
            .back-btn, a[href*="index.html"] {
                padding: 12px 18px;
                font-size: 16px;
                min-height: 44px;
                min-width: 44px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
            }
            h1 { font-size: 24px; }
            h2 { font-size: 20px; }
            h3 { font-size: 18px; }
            button, .btn, input[type="button"] {
                min-height: 44px;
                min-width: 44px;
                font-size: 16px;
            }
        }
        @media (max-width: 480px) {
            body {
                font-size: 16px;
                padding: 10px;
            }
            .back-btn, a[href*="index.html"] {
                padding: 10px 14px;
                font-size: 14px;
            }
            h1 { font-size: 20px; }
            h2 { font-size: 18px; }
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
    print("开始为游戏页面添加移动端CSS...\n")
    
    fixed = 0
    skipped = 0
    failed = 0
    
    for game_path in GAMES_TO_FIX:
        filepath = WORKSPACE / game_path
        if not filepath.exists():
            print(f"❌ 文件不存在: {game_path}")
            failed += 1
            continue
        
        success, msg = add_mobile_css(filepath)
        status = "✅" if success else "❌"
        print(f"{status} {game_path}: {msg}")
        
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
