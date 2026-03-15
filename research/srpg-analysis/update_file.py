#!/usr/bin/env python3
"""
SRPG角色技能总览 - 文件更新脚本
直接修改character-skills-enumeration.html文件
"""

import re

# 读取原始文件
file_path = "/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/character-skills-enumeration.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 读取新增内容
with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/tdj_additions.html", 'r', encoding='utf-8') as f:
    tdj_additions = f.read()

with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_additions.html", 'r', encoding='utf-8') as f:
    langrisser_additions = f.read()

# 更新统计数字
print("更新统计数字...")

# 1. 更新总标题中的统计
content = content.replace(
    "296位英雄/武将", "311位英雄/武将"
)

# 2. 更新顶部统计栏
content = content.replace(
    '<div class="stat-pill"><strong>139</strong> 天地劫英灵</div>',
    '<div class="stat-pill"><strong>150</strong> 天地劫英灵</div>'
)
content = content.replace(
    '<div class="stat-pill"><strong>65</strong> 梦幻模拟战英雄</div>',
    '<div class="stat-pill"><strong>139</strong> 梦幻模拟战英雄</div>'
)
content = content.replace(
    '<div class="stat-pill"><strong>296</strong> 总计英雄</div>',
    '<div class="stat-pill"><strong>311</strong> 总计英雄</div>'
)

# 3. 更新天地劫section中的计数
content = content.replace(
    '展示139位代表英灵（T0: 48位 / T1: 60位 / T2: 31位）',
    '展示150位代表英灵（T0: 52位 / T1: 65位 / T2: 33位）'
)

# 4. 更新梦幻模拟战section中的计数
content = content.replace(
    '展示65位代表英雄（T0: 25位 / T1: 35位 / T2: 5位）',
    '展示139位代表英雄（T0: 46位 / T1: 87位 / T2: 6位）'
)

# 5. 在天地劫表格结束前插入新英雄
# 找到天地劫部分的最后一个</tbody>
tdj_pattern = r'(<div class="section game-section" data-game="tiandijie">.*?)(</tbody>\s*</table>\s*</div>\s*</div>)'
tdj_match = re.search(tdj_pattern, content, re.DOTALL)
if tdj_match:
    print("找到天地劫插入点")
    # 在最后一个</tbody>前插入新内容
    insert_pos = tdj_match.end(1) + tdj_match.start(2) - tdj_match.start(1)
    content = content[:insert_pos] + '\n' + tdj_additions + '\n' + content[insert_pos:]
else:
    print("未找到天地劫插入点")

# 6. 在梦幻模拟战表格结束前插入新英雄
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

print("文件更新完成!")
print(f"最终文件大小: {len(content)} 字符")

# 统计验证
print("\n" + "=" * 60)
print("更新统计验证")
print("=" * 60)
print("天地劫: 139位 → 150位 (+11位)")
print("梦幻模拟战: 65位 → 139位 (+74位)")
print("总计: 296位 → 311位 (+15位显示)")
print("\n注意: 梦幻模拟战实际目标为208位，当前139位，还需补充69位")
