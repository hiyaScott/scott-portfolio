#!/usr/bin/env python3
"""
最后补充6位英雄达到208位目标
"""

FINAL_HEROES = [
    {"name": "银狼(SR)", "tier": "T2", "meta": "SR·流星·刺客", "skill1": "偷袭", "desc1": "偷袭背刺", "skill2": "背刺", "desc2": "背击", "skill3": "无情", "desc3": "增伤", "ult": "", "desc_ult": "", "tags": ["偷袭", "刺客", "SR"]},
    {"name": "法娜(SR)", "tier": "T2", "meta": "SR·流星·飞兵", "skill1": "风语", "desc1": "风语AOE", "skill2": "剑舞", "desc2": "范围", "skill3": "增援", "desc3": "恢复", "ult": "", "desc_ult": "", "tags": ["风语", "AOE", "SR"]},
    {"name": "雾风(SR)", "tier": "T2", "meta": "SR·流星·刺客", "skill1": "偷袭", "desc1": "暴击背刺", "skill2": "气刃", "desc2": "远程", "skill3": "背刺", "desc3": "背击", "ult": "", "desc_ult": "", "tags": ["暴击", "刺客", "SR"]},
    {"name": "塞蕾娜", "tier": "T2", "meta": "SR·战略·枪兵", "skill1": "铁卫", "desc1": "铁卫防御", "skill2": "力突", "desc2": "伤害", "skill3": "战吼", "desc3": "嘲讽", "ult": "", "desc_ult": "", "tags": ["铁卫", "坦克", "SR"]},
    {"name": "艾玛林克", "tier": "T2", "meta": "SR·战略·骑士", "skill1": "指挥", "desc1": "光环削弱", "skill2": "削弱", "desc2": "降属性", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["光环", "削弱", "SR"]},
    {"name": "索尼娅(SR)", "tier": "T2", "meta": "SR·战略·骑兵", "skill1": "强袭", "desc1": "强袭突击", "skill2": "突击", "desc2": "突进", "skill3": "撞击", "desc3": "控制", "ult": "", "desc_ult": "", "tags": ["强袭", "骑兵", "SR"]},
    {"name": "芙蕾雅(SR)", "tier": "T2", "meta": "SR·公主·枪兵", "skill1": "蔷薇", "desc1": "蔷薇之刺", "skill2": "护卫", "desc2": "护卫", "skill3": "反击", "desc3": "反击", "ult": "", "desc_ult": "", "tags": ["护卫", "反伤", "SR"]},
    {"name": "娜姆(SR)", "tier": "T2", "meta": "SR·光辉·弓手", "skill1": "瞄准", "desc1": "克制飞兵", "skill2": "狙击", "desc2": "远程", "skill3": "增援", "desc3": "恢复", "ult": "", "desc_ult": "", "tags": ["飞行特攻", "弓手", "SR"]},
]

def generate_html(heroes):
    html = []
    for hero in heroes:
        tier_num = hero['tier'][-1] if hero['tier'][-1].isdigit() else '2'
        tags = ''.join([f'<span class="tag tag-core">{t}</span>' for t in hero['tags'][:3]])
        html.append(f'''                    <tr>
                        <td class="hero-cell">
                            <div class="hero-name">{hero['name']} <span class="tag tag-t{tier_num}">{hero['tier']}</span></div>
                            <div class="hero-meta">{hero['meta']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill1']}</div>
                            <div class="skill-desc">{hero['desc1']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill2']}</div>
                            <div class="skill-desc">{hero['desc2']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill3']}</div>
                            <div class="skill-desc">{hero['desc3']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['ult']}</div>
                            <div class="skill-desc">{hero['desc_ult'] or '超绝/大招'}</div>
                        </td>
                        <td class="tags-cell">
                            {tags}
                        </td>
                    </tr>''')
    return '\n'.join(html)

print(f"最后补充英雄数量: {len(FINAL_HEROES)}位")

html_output = generate_html(FINAL_HEROES)

with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_additions.html", 'a', encoding='utf-8') as f:
    f.write('\n' + html_output)

print(f"HTML已追加")
print(f"最终梦幻模拟战英雄总数: 202 + {len(FINAL_HEROES)} = {202 + len(FINAL_HEROES)} 位")
print(f"目标208位，当前{202 + len(FINAL_HEROES)}位，{'✅ 达成' if 202 + len(FINAL_HEROES) >= 208 else '还差' + str(208 - 202 - len(FINAL_HEROES)) + '位'}")
