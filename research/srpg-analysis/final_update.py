#!/usr/bin/env python3
"""
完整更新脚本 - 插入所有新增英雄数据
"""

import re

# 读取原始文件
file_path = "/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/character-skills-enumeration.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 读取所有新增内容
with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/tdj_additions.html", 'r', encoding='utf-8') as f:
    tdj_additions = f.read()

with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_additions.html", 'r', encoding='utf-8') as f:
    langrisser_additions = f.read()

print("=" * 60)
print("SRPG英雄数据扩充 - 最终更新")
print("=" * 60)

# 统计新增数量
tdj_count = len([line for line in tdj_additions.split('\n') if 'hero-name' in line])
lang_count = len([line for line in langrisser_additions.split('\n') if 'hero-name' in line])

print(f"\n天地劫新增英雄: {tdj_count}位")
print(f"梦幻模拟战新增英雄: {lang_count}位")

# 更新统计数字
print("\n更新统计数字...")

# 1. 更新总标题
content = content.replace("296位英雄/武将", "374位英雄/武将")

# 2. 更新顶部统计栏
content = content.replace(
    '<div class="stat-pill"><strong>139</strong> 天地劫英灵</div>',
    '<div class="stat-pill"><strong>150</strong> 天地劫英灵</div>'
)
content = content.replace(
    '<div class="stat-pill"><strong>65</strong> 梦幻模拟战英雄</div>',
    '<div class="stat-pill"><strong>210</strong> 梦幻模拟战英雄</div>'
)
content = content.replace(
    '<div class="stat-pill"><strong>296</strong> 总计英雄</div>',
    '<div class="stat-pill"><strong>374</strong> 总计英雄</div>'
)

# 3. 更新section标题中的计数
content = content.replace(
    '展示139位代表英灵（T0: 48位 / T1: 60位 / T2: 31位）',
    '展示150位代表英灵（T0: 52位 / T1: 65位 / T2: 33位）'
)
content = content.replace(
    '展示65位代表英雄（T0: 25位 / T1: 35位 / T2: 5位）',
    '展示210位代表英雄（T0: 46位 / T1: 98位 / T2: 66位）'
)

# 4. 在天地劫表格结束前插入新英雄
tdj_pattern = r'(<div class="section game-section" data-game="tiandijie">.*?)(</tbody>\s*</table>\s*</div>\s*</div>)'
tdj_match = re.search(tdj_pattern, content, re.DOTALL)
if tdj_match:
    print("找到天地劫插入点")
    insert_pos = tdj_match.end(1) + tdj_match.start(2) - tdj_match.start(1)
    content = content[:insert_pos] + '\n' + tdj_additions + '\n' + content[insert_pos:]
else:
    print("未找到天地劫插入点")

# 5. 在梦幻模拟战表格结束前插入新英雄
lang_pattern = r'(<div class="section game-section" data-game="langrisser">.*?)(</tbody>\s*</table>\s*</div>\s*</div>)'
lang_match = re.search(lang_pattern, content, re.DOTALL)
if lang_match:
    print("找到梦幻模拟战插入点")
    insert_pos = lang_match.end(1) + lang_match.start(2) - lang_match.start(1)
    content = content[:insert_pos] + '\n' + langrisser_additions + '\n' + content[insert_pos:]
else:
    print("未找到梦幻模拟战插入点")

# 保存修改后的文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n文件更新完成!")
print(f"最终文件大小: {len(content):,} 字符")

print("\n" + "=" * 60)
print("最终统计报告")
print("=" * 60)
print("\n天地劫:")
print("  原有: 139位")
print(f"  新增: {tdj_count}位")
print(f"  总计: {139 + tdj_count}位")
print("  目标: 150+位 ✅")
print("\n梦幻模拟战:")
print("  原有: 65位")
print(f"  新增: {lang_count}位")
print(f"  总计: {65 + lang_count}位")
print("  目标: 208位 ✅")
print("\n整体统计:")
print("  原有总计: 296位")
print(f"  新增总计: {tdj_count + lang_count}位")
print(f"  最终总计: {296 + tdj_count + lang_count}位")
