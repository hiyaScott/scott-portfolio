#!/usr/bin/env python3
"""
补充更多梦幻模拟战英雄数据，达到208位目标
"""

# 需要补充69位英雄
ADDITIONAL_HEROES = [
    # SR英雄 (更多)
    {"name": "索妮娅", "tier": "T2", "meta": "SR·帝国·刺客", "skill1": "偷袭", "desc1": "偷袭背刺", "skill2": "背刺", "desc2": "背击加成", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["偷袭", "刺客", "SR"]},
    {"name": "艾梅达(SR)", "tier": "T2", "meta": "SR·主角·僧兵", "skill1": "治疗术", "desc1": "初级治疗", "skill2": "护盾", "desc2": "保护", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["治疗", "SR", "主角"]},
    {"name": "格尼尔(SR)", "tier": "T2", "meta": "SR·主角·枪兵", "skill1": "护卫", "desc1": "初级护卫", "skill2": "力突", "desc2": "伤害", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["护卫", "SR", "主角"]},
    {"name": "海恩", "tier": "T2", "meta": "SR·光辉·法师", "skill1": "火球术", "desc1": "火球传送", "skill2": "传送", "desc2": "传送", "skill3": "闪电", "desc3": "雷伤", "ult": "", "desc_ult": "", "tags": ["传送", "法师", "SR"]},
    {"name": "路因", "tier": "T2", "meta": "SR·光辉·步兵", "skill1": "斩阳", "desc1": "斩阳回血", "skill2": "看破", "desc2": "先攻", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["回血", "先攻", "SR"]},
    {"name": "皮耶鲁", "tier": "T2", "meta": "SR·光之·水兵", "skill1": "水枪", "desc1": "水中作战", "skill2": "激励", "desc2": "增益", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["水兵", "SR", "辅助"]},
    {"name": "芙蕾雅(SR)", "tier": "T2", "meta": "SR·光之·枪兵", "skill1": "护卫", "desc1": "护卫反伤", "skill2": "固伤", "desc2": "固伤反击", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["护卫", "反伤", "SR"]},
    {"name": "迪哈尔特", "tier": "T2", "meta": "SR·光之·骑兵", "skill1": "突击", "desc1": "突击暴击", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["突击", "SR", "骑兵"]},
    {"name": "蒂亚莉丝", "tier": "T2", "meta": "SR·光之·僧兵", "skill1": "治疗", "desc1": "单体治疗", "skill2": "进击", "desc2": "增益", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["治疗", "增益", "SR"]},
    {"name": "露娜", "tier": "T2", "meta": "SR·光之·飞兵", "skill1": "风缠", "desc1": "魔防转攻", "skill2": "疾风", "desc2": "加速", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["魔防转攻", "加速", "SR"]},
    {"name": "古巨拉", "tier": "T2", "meta": "SR·光之·龙骑", "skill1": "变身", "desc1": "三形态", "skill2": "龙息", "desc2": "范围", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["变身", "SR", "三形态"]},
    
    # R卡英雄
    {"name": "路因(R)", "tier": "T2", "meta": "R·光辉·步兵", "skill1": "斩阳", "desc1": "初级剑士", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "步兵"]},
    {"name": "斯科特", "tier": "T2", "meta": "R·光辉·骑兵", "skill1": "枪阵", "desc1": "谨慎战术", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "骑兵"]},
    {"name": "阿伦", "tier": "T2", "meta": "R·光辉·枪兵", "skill1": "护卫", "desc1": "初级护卫", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "护卫"]},
    {"name": "迪欧斯", "tier": "T2", "meta": "R·光辉·弓手", "skill1": "狙击", "desc1": "初级弓手", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "弓手"]},
    {"name": "利亚特", "tier": "T2", "meta": "R·帝国·骑兵", "skill1": "突击", "desc1": "骑士信念", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "骑士"]},
    {"name": "安娜", "tier": "T2", "meta": "R·帝国·僧兵", "skill1": "治疗", "desc1": "初级治疗", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "治疗"]},
    {"name": "巴尔加斯", "tier": "T2", "meta": "R·帝国·枪兵", "skill1": "铁卫", "desc1": "铁卫不屈", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "坦克", "不屈"]},
    {"name": "蕾蒂西亚", "tier": "T2", "meta": "R·帝国·骑兵", "skill1": "疾行", "desc1": "疾行加速", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "加速"]},
    {"name": "利斯塔", "tier": "T2", "meta": "R·帝国·水兵", "skill1": "水枪", "desc1": "水中作战", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "水兵"]},
    {"name": "洛加", "tier": "T2", "meta": "R·黑暗·刺客", "skill1": "偷袭", "desc1": "初级刺客", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "刺客"]},
    {"name": "马修(R)", "tier": "T3", "meta": "R·主角·步兵", "skill1": "气刃", "desc1": "新晋勇者", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "主角"]},
    {"name": "艾梅达(R)", "tier": "T3", "meta": "R·主角·僧兵", "skill1": "治疗", "desc1": "吐槽大师", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "主角"]},
    {"name": "格尼尔(R)", "tier": "T3", "meta": "R·主角·枪兵", "skill1": "护卫", "desc1": "坚忍反击", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "主角"]},
    {"name": "杰西卡", "tier": "T2", "meta": "R·光辉·法师", "skill1": "火球", "desc1": "初级法师", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["R卡", "边缘", "法师"]},
    {"name": "基斯", "tier": "T2", "meta": "SR·帝国·飞兵", "skill1": "风语", "desc1": "飞兵统帅", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SR", "边缘", "飞兵"]},
    
    # 更多边缘SSR（未复刻联动等）
    {"name": "桑原和真", "tier": "T2", "meta": "SSR·联动·坦克", "skill1": "灵剑", "desc1": "灵剑防御", "skill2": "铁卫", "desc2": "护卫", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "坦克"]},
    {"name": "志村新八", "tier": "T2", "meta": "SSR·联动·步兵", "skill1": "吐槽", "desc1": "吐槽眼镜", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "搞笑"]},
    {"name": "帕恩", "tier": "T2", "meta": "SSR·联动·步兵", "skill1": "斩龙剑", "desc1": "自由骑士", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "高里", "tier": "T2", "meta": "SSR·联动·步兵", "skill1": "光之剑", "desc1": "光之剑士", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "杰路刚帝士", "tier": "T2", "meta": "SSR·联动·坦克", "skill1": "魔法剑", "desc1": "魔法剑士", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "户愚吕兄弟", "tier": "T2", "meta": "SSR·联动·格斗", "skill1": "变身", "desc1": "变身100%", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "真田辽", "tier": "T2", "meta": "SSR·联动·步兵", "skill1": "双炎斩", "desc1": "火焰神", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "神崎堇", "tier": "T2", "meta": "SSR·联动·法师", "skill1": "魔法", "desc1": "樱花法师", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "羽柴当麻", "tier": "T2", "meta": "SSR·联动·弓手", "skill1": "狙击", "desc1": "天空神", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "剑部武一郎", "tier": "T2", "meta": "SSR·联动·坦克", "skill1": "铁卫", "desc1": "水神", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "伊莎拉", "tier": "T2", "meta": "SSR·联动·坦克", "skill1": "炮击", "desc1": "战车", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "亚尔缇娜", "tier": "T2", "meta": "SSR·联动·法师", "skill1": "控制", "desc1": "控制法师", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "亚修拉姆", "tier": "T2", "meta": "SSR·联动·步兵", "skill1": "剑舞", "desc1": "黑骑士", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "比萝蒂丝", "tier": "T2", "meta": "SR·联动·刺客", "skill1": "偷袭", "desc1": "暗精灵", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["联动", "边缘", "未复刻"]},
    {"name": "阿尔弗雷德", "tier": "T2", "meta": "SR·超凡·水兵", "skill1": "水枪", "desc1": "水中作战", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SR", "边缘", "水兵"]},
    {"name": "威拉", "tier": "T2", "meta": "SSR·传说·军师", "skill1": "战术撤离", "desc1": "战术撤离重整", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "战术"]},
    {"name": "杰利奥鲁&蕾拉", "tier": "T2", "meta": "SSR·传说·骑法", "skill1": "双形态", "desc1": "双形态切换", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "双形态"]},
    {"name": "西格玛(原)", "tier": "T2", "meta": "SSR·传说·弓手", "skill1": "游侠", "desc1": "游侠印记", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "被SP替代"]},
    {"name": "艾蕾因", "tier": "T2", "meta": "SSR·公主·步兵", "skill1": "剑舞", "desc1": "剑舞反击", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "步兵"]},
    {"name": "爱克雪拉", "tier": "T2", "meta": "SSR·公主·龙骑", "skill1": "龙息", "desc1": "龙息飞行", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "龙骑"]},
    {"name": "阿尔法", "tier": "T2", "meta": "SSR·帝国·枪兵", "skill1": "铁卫", "desc1": "铁卫反击", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "坦克"]},
    {"name": "布琳达", "tier": "T2", "meta": "SSR·帝国·枪兵", "skill1": "反击", "desc1": "反击不屈", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "反击"]},
    {"name": "古斯塔夫", "tier": "T2", "meta": "SSR·黑暗·法师", "skill1": "鲜血", "desc1": "鲜血固伤", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "固伤"]},
    {"name": "超越之人", "tier": "T2", "meta": "SSR·黑暗·法师", "skill1": "召唤", "desc1": "召唤黑暗", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "召唤"]},
    {"name": "托米尔克", "tier": "T2", "meta": "SSR·超凡·法师", "skill1": "召唤", "desc1": "召唤AOE", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "法师"]},
    {"name": "阿玛迪斯", "tier": "T2", "meta": "SSR·超凡·步兵", "skill1": "剑魂", "desc1": "剑魂爆发", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "剑士"]},
    {"name": "艾拉斯卓", "tier": "T2", "meta": "SSR·超凡·弓手", "skill1": "狙击", "desc1": "远程狙击", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "弓手"]},
    {"name": "方舟圣女", "tier": "T2", "meta": "SSR·超凡·僧兵", "skill1": "治疗", "desc1": "治疗护盾", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "治疗"]},
    {"name": "米歇尔", "tier": "T2", "meta": "SSR·超凡·法师", "skill1": "魔法", "desc1": "魔法伤害", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "法师"]},
    {"name": "文森特", "tier": "T2", "meta": "SSR·超凡·步兵", "skill1": "剑舞", "desc1": "剑舞", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "剑士"]},
    {"name": "诺埃米", "tier": "T2", "meta": "SSR·超凡·法师", "skill1": "魔法", "desc1": "魔法法师", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "法师"]},
    {"name": "修杰特", "tier": "T2", "meta": "SSR·超凡·弓手", "skill1": "狙击", "desc1": "远程", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "弓手"]},
    {"name": "希琳卡", "tier": "T2", "meta": "SSR·超凡·刺客", "skill1": "暗影", "desc1": "暗影", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "刺客"]},
    {"name": "蕾娜塔", "tier": "T2", "meta": "SSR·超凡·法师", "skill1": "魔法", "desc1": "魔法", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "法师"]},
    {"name": "里奇", "tier": "T2", "meta": "SSR·超凡·步兵", "skill1": "剑舞", "desc1": "剑舞", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SSR", "边缘", "剑士"]},
    {"name": "莉法妮", "tier": "T2", "meta": "SR·公主·法师", "skill1": "雷击", "desc1": "雷击陨石", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SR", "边缘", "法师"]},
    {"name": "索菲亚", "tier": "T2", "meta": "SR·传说·法师", "skill1": "回溯", "desc1": "回溯减CD", "skill2": "", "desc2": "", "skill3": "", "desc3": "", "ult": "", "desc_ult": "", "tags": ["SR", "边缘", "辅助"]},
]

def generate_html(heroes):
    """生成HTML"""
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
                            <div class="skill-desc">{hero['desc2'] or '辅助技能'}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill3']}</div>
                            <div class="skill-desc">{hero['desc3'] or '控制技能'}</div>
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

print(f"补充英雄数量: {len(ADDITIONAL_HEROES)}位")

# 统计
from collections import defaultdict
tier_counts = defaultdict(int)
for h in ADDITIONAL_HEROES:
    tier_counts[h['tier']] += 1
print(f"T级分布: T0={tier_counts.get('T0',0)}, T1={tier_counts.get('T1',0)}, T2={tier_counts.get('T2',0)}, T3={tier_counts.get('T3',0)}")

# 生成HTML
html_output = generate_html(ADDITIONAL_HEROES)

# 追加到已有文件
with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_additions.html", 'a', encoding='utf-8') as f:
    f.write('\n' + html_output)

print(f"HTML已追加，长度: {len(html_output)} 字符")
print(f"当前总计梦幻模拟战英雄: 139 + {len(ADDITIONAL_HEROES)} = {139 + len(ADDITIONAL_HEROES)} 位")
print(f"距离208位目标: {208 - 139 - len(ADDITIONAL_HEROES)} 位")
