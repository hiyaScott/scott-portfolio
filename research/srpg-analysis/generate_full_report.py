#!/usr/bin/env python3
"""
梦幻模拟战角色数据库勘误报告生成器（完整版）
基于已收集的真实数据进行对比分析
"""

import json
from datetime import datetime

# 已验证的真实数据（来自搜索验证）
VERIFIED_DATA = {
    "泽瑞达": {
        "correct_talent": "捉迷藏",
        "correct_factions": ["黑暗轮回", "流星直击"],
        "correct_class": "刺客/魔物",
        "talent_desc": "暴击率提升(10%,13%,16%,20%)。行动结束时如处于危险范围外，进入潜行状态：暴击率、暴击伤害提升(15%,20%,25%,30%)，遭受伤害降低(15%,20%,25%,30%)，移动力提升(1,2,3,4)",
        "issues": [
            "❌ 天赋名称错误：当前为'瞬身'，应为'捉迷藏'",
            "❌ 天赋描述严重不完整：缺失潜行状态的核心机制",
            "❌ 阵营信息不完整：应包含'黑暗轮回、流星直击'双阵营",
            "❌ 职业信息不完整：应有刺客和魔物双职业线"
        ]
    },
    "尤利娅": {
        "correct_talent": "不朽的传说",
        "correct_factions": ["光辉军团", "超凡领域", "公主联盟"],
        "correct_class": "圣职/步兵",
        "talent_desc": "部队生命高于(95%,90%,80%,70%)时：伤害提升(10%,15%,20%,30%)，无法被一击致命（每场战斗最多触发1,2,2,3次），进入战斗后有(40%,60%,80%,100%)概率恢复生命，恢复量为部队造成伤害的30%",
        "issues": [
            "❌ 天赋名称错误：当前为'神威'，应为'不朽的传说'",
            "⚠️ 神威是技能名称，不是天赋名称（天赋技能混淆）",
            "❌ 阵营信息不完整：应包含光辉、超凡、公主三阵营",
            "❌ 天赋描述缺失核心机制：复活次数、触发条件等"
        ]
    },
    "艾尔文": {
        "correct_talent": "勇者的意志",
        "correct_factions": ["主角光环", "光辉军团", "帝国之辉"],
        "correct_class": "步兵/枪兵/骑兵",
        "talent_desc": "主动攻击进入战斗时，伤害提升(10%,13%,16%,20%)。战斗后有(40%,60%,80%,100%)概率恢复生命，恢复量为英雄造成伤害的30%",
        "sp_talent": "光龙的意志",
        "sp_talent_desc": "SP形态专属天赋，具有不屈和先攻效果",
        "issues": [
            "❌ 天赋名称错误：当前为'光辉的意志'，应为'勇者的意志'",
            "❌ 天赋描述不完整：缺少概率和星级成长信息",
            "❌ 阵营信息严重缺失：应包含主角、光辉、帝国三阵营",
            "⚠️ SP形态天赋混淆：应明确区分原版和SP版天赋"
        ]
    },
    "艾尔文(SP)": {
        "correct_talent": "光龙的意志",
        "correct_factions": ["主角光环", "光辉军团", "帝国之辉"],
        "correct_class": "步兵/枪兵/骑兵",
        "talent_desc": "SP形态专属天赋，主动攻击进入战斗时伤害提升，具有不屈（免死）和先攻机制",
        "issues": [
            "❌ SP天赋描述严重缺失：未体现不屈、先攻等核心机制",
            "⚠️ SP形态应与原版艾尔文明确区分"
        ]
    },
    "雪莉": {
        "correct_talent": "落跑公主",
        "correct_factions": ["光辉军团", "公主联盟"],
        "correct_class": "飞兵/刺客",
        "talent_desc": "周围2格没有友军时，遭受所有伤害降低(10%,15%,20%,25%)。击杀敌军后，可以额外行动1次（再行动效果需要间隔2回合才可以再次触发）",
        "issues": [
            "⚠️ 天赋描述基本正确但缺少星级成长数值",
            "⚠️ 阵营信息基本正确（光辉、公主）",
            "⚠️ 普通版每回合最多触发1次再动，应明确标注"
        ]
    },
    "雪莉(SP)": {
        "correct_talent": "落跑公主（强化版）",
        "correct_factions": ["光辉军团", "公主联盟", "流星直击"],
        "correct_class": "飞兵",
        "talent_desc": "SP强化版：周围2格没有友军时减伤，击杀敌人后额外行动1次（每回合最多触发2次），且攻击提升",
        "issues": [
            "⚠️ SP版每回合最多触发2次再动，当前描述为'最多2次'基本正确",
            "❌ SP版阵营信息缺失：应增加流星直击阵营",
            "⚠️ 应明确标注SP版与普通版的区别"
        ]
    },
    "波赞鲁": {
        "correct_talent": "千年的邪念",
        "correct_factions": ["黑暗轮回"],
        "correct_class": "魔物/法师",
        "talent_desc": "使用自身魔防的1.5倍替代智力。对敌军造成伤害后，(50%,60%,80%,100%)概率对其施加1个随机的弱化状态",
        "issues": [
            "❌ 天赋名称严重错误：当前为'黑暗超绝'，应为'千年的邪念'",
            "❌ 黑暗超绝是技能，不是天赋（天赋技能严重混淆）",
            "❌ 天赋描述完全错误：缺失魔防转智力的核心机制",
            "⚠️ 阵营信息基本正确：黑暗轮回"
        ]
    },
    "利昂": {
        "correct_talent": "骑士精神",
        "correct_factions": ["帝国之辉", "战略大师"],
        "correct_class": "骑兵",
        "talent_desc": "每移动1格，攻击提升(1%,2%,3%,4%)，防御提升(2%,3%,4%,5%)。攻击后还有一次移动的机会（再移动2,3,3,3格）",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "❌ 阵营信息不完整：应包含'帝国之辉、战略大师'双阵营",
            "⚠️ 天赋描述不完整：缺少再移动机制和星级成长"
        ]
    },
    "雷丁": {
        "correct_talent": "神卫",
        "correct_factions": ["光辉军团"],
        "correct_class": "枪兵/圣职",
        "talent_desc": "用魔防的1.6倍替代物防。可以替2格范围内的友军承受物理伤害。英雄生命100%时，遭受伤害降低(10%,13%,16%,20%)",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "⚠️ 天赋描述不完整：缺失魔防转防御的核心机制",
            "⚠️ 阵营信息基本正确"
        ]
    },
    "莉亚娜": {
        "correct_talent": "再行动",
        "correct_factions": ["光辉军团", "公主联盟"],
        "correct_class": "僧兵",
        "talent_desc": "行动结束时，使相邻(1,1,2,2)格内的1个友军再行动，且恢复其生命值（恢复量为自身智力的(1,1.5,2,2.5)倍），每间隔(6,5,4,3)回合触发1次",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "❌ 阵营信息不完整：应包含光辉、公主双阵营",
            "❌ 天赋描述缺失：再行动有CD间隔，不是无限使用"
        ]
    },
    "拉娜": {
        "correct_talent": "暗镰",
        "correct_factions": ["黑暗轮回", "公主联盟"],
        "correct_class": "法师",
        "talent_desc": "智力提升(10%,13%,16%,20%)。范围技能射程提升(0,0,1,1)。与生命值百分比低于自身的部队交战时，伤害提升(10%,13%,16%,20%)",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "❌ 阵营信息不完整：应包含黑暗、公主双阵营",
            "⚠️ 天赋描述不完整：缺失射程提升和增伤条件"
        ]
    },
    "露娜": {
        "correct_talent": "风之守护",
        "correct_factions": ["公主联盟", "战略大师"],
        "correct_class": "飞兵/弓兵",
        "talent_desc": "魔防提升(10%,13%,16%,20%)。周围(2,2,2,3)格范围内的友军遭受魔法伤害降低(10%,15%,20%,30%)",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "❌ 阵营信息不完整：应包含公主、战略双阵营",
            "⚠️ 天赋描述不完整：缺失星级成长数值"
        ]
    },
    "蒂亚丽丝": {
        "correct_talent": "治愈之光",
        "correct_factions": ["公主联盟"],
        "correct_class": "僧兵",
        "talent_desc": "行动结束时，使相邻1格内的友军受到伤害降低(10%,13%,16%,20%)，持续1回合；并在其行动结束时恢复生命（恢复量为自身智力的(1,1.5,2,2.5)倍）",
        "issues": [
            "⚠️ 天赋名称基本正确",
            "❌ 阵营信息严重缺失：应包含公主联盟",
            "⚠️ 天赋描述不完整：缺失星级成长数值"
        ]
    }
}

# 常见错误模式统计
COMMON_ISSUES = {
    "天赋技能混淆": "多名角色的天赋名称与技能名称被混淆，如尤利娅的天赋是'不朽的传说'而非'神威'，波赞鲁的天赋是'千年的邪念'而非'黑暗超绝'",
    "阵营信息不完整": "多数角色只标注了单一阵营，实际应为多阵营。如艾尔文应有主角、光辉、帝国三阵营",
    "天赋描述缺失": "大量角色的天赋描述缺失星级成长数值和触发条件",
    "SP形态区分不清": "SP角色与普通角色的天赋、技能描述未明确区分",
    "超绝技能归属错误": "超绝是技能，不应作为天赋描述"
}


def generate_correction_report(heroes_data):
    """生成勘误报告"""
    
    report = []
    report.append("# 梦幻模拟战角色数据库勘误报告")
    report.append("")
    report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("## 概览")
    report.append("")
    report.append(f"- 数据库总角色数：{len(heroes_data)}")
    report.append(f"- 已验证角色数：{len(VERIFIED_DATA)}")
    report.append(f"- 待验证角色数：{len(heroes_data) - len(VERIFIED_DATA)}")
    report.append("")
    
    # 统计问题数量
    total_issues = 0
    critical_issues = 0
    for hero_data in VERIFIED_DATA.values():
        for issue in hero_data['issues']:
            total_issues += 1
            if issue.startswith("❌"):
                critical_issues += 1
    
    report.append(f"- 发现问题总数：{total_issues}")
    report.append(f"- 严重错误（需立即修正）：{critical_issues}")
    report.append(f"- 一般问题（建议优化）：{total_issues - critical_issues}")
    report.append("")
    
    # 常见错误模式
    report.append("## 常见错误模式")
    report.append("")
    for issue_type, description in COMMON_ISSUES.items():
        report.append(f"### {issue_type}")
        report.append(f"{description}")
        report.append("")
    
    # 已验证角色的详细勘误
    report.append("## 已验证角色勘误详情")
    report.append("")
    
    for hero_name, verified in VERIFIED_DATA.items():
        report.append(f"### {hero_name}")
        report.append("")
        
        # 查找原数据
        original = None
        for hero in heroes_data:
            if hero['name'] == hero_name:
                original = hero
                break
        
        if original:
            report.append("**原数据：**")
            report.append(f"```")
            report.append(f"天赋：{original.get('talent', {}).get('name', 'N/A')}")
            report.append(f"阵营：{original.get('faction', 'N/A')}")
            report.append(f"职业：{original.get('class', 'N/A')}")
            report.append(f"```")
            report.append("")
        
        report.append("**正确数据：**")
        report.append(f"```")
        report.append(f"天赋：{verified['correct_talent']}")
        report.append(f"阵营：{', '.join(verified['correct_factions'])}")
        report.append(f"职业：{verified['correct_class']}")
        if 'talent_desc' in verified:
            report.append(f"天赋描述：{verified['talent_desc']}")
        report.append(f"```")
        report.append("")
        
        report.append("**发现问题：**")
        for issue in verified['issues']:
            report.append(f"{issue}")
        report.append("")
        report.append("---")
        report.append("")
    
    # 统计摘要
    report.append("## 统计摘要")
    report.append("")
    report.append("### 按问题类型统计")
    report.append("")
    
    # 统计各类问题
    talent_issues = len([v for v in VERIFIED_DATA.values() if any('天赋' in i for i in v['issues'])])
    faction_issues = len([v for v in VERIFIED_DATA.values() if any('阵营' in i for i in v['issues'])])
    desc_issues = len([v for v in VERIFIED_DATA.values() if any('描述' in i for i in v['issues'])])
    
    report.append(f"- 天赋名称/描述错误：{talent_issues}位角色")
    report.append(f"- 阵营信息错误：{faction_issues}位角色")
    report.append(f"- 描述不完整：{desc_issues}位角色")
    report.append("")
    
    # 修正建议
    report.append("## 修正建议")
    report.append("")
    report.append("### 立即修正（严重错误）")
    report.append("1. **波赞鲁**：天赋名称'黑暗超绝'→'千年的邪念'（天赋技能严重混淆）")
    report.append("2. **泽瑞达**：天赋名称'瞬身'→'捉迷藏'")
    report.append("3. **尤利娅**：天赋名称'神威'→'不朽的传说'")
    report.append("4. **艾尔文**：天赋名称'光辉的意志'→'勇者的意志'")
    report.append("")
    report.append("### 建议优化")
    report.append("1. **阵营信息补全**：所有角色应列出其所属的全部阵营")
    report.append("2. **天赋描述完善**：补充星级成长数值和触发条件")
    report.append("3. **SP形态标注**：SP角色应在名称和描述中明确标注")
    report.append("4. **数据来源统一**：建议以B站Wiki或官方资料为准")
    report.append("")
    
    # 待验证角色列表
    report.append("## 待验证角色列表（前50位）")
    report.append("")
    unverified = [h['name'] for h in heroes_data if h['name'] not in VERIFIED_DATA][:50]
    for i, name in enumerate(unverified, 1):
        report.append(f"{i}. {name}")
    report.append("")
    
    # 参考数据来源
    report.append("## 参考数据来源")
    report.append("")
    report.append("- B站Wiki：https://wiki.biligame.com/langrisser")
    report.append("- 梦幻模拟战手游官方资料")
    report.append("- LevelOne攻略站")
    report.append("- 游戏内实际数据")
    report.append("")
    
    return "\n".join(report)


if __name__ == '__main__':
    # 读取提取的角色数据
    with open('/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_heroes.json', 'r', encoding='utf-8') as f:
        heroes = json.load(f)
    
    # 生成报告
    report = generate_correction_report(heroes)
    
    # 保存报告
    report_path = '/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser-corrections-report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"勘误报告已生成：{report_path}")
    print(f"总角色数：{len(heroes)}")
    print(f"已验证角色数：{len(VERIFIED_DATA)}")
    print(f"发现问题总数：{sum(len(v['issues']) for v in VERIFIED_DATA.values())}")
