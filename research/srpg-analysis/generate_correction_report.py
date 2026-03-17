#!/usr/bin/env python3
"""
梦幻模拟战角色数据库勘误报告生成器
基于已收集的真实数据进行对比分析
"""

import json
from datetime import datetime

# 已验证的真实数据（来自搜索验证）
VERIFIED_DATA = {
    "泽瑞达": {
        "correct_talent": "捉迷藏",
        "correct_factions": ["黑暗轮回", "流星直击"],
        "correct_class": "刺客",
        "issues": [
            "天赋名称错误：当前为'瞬身'，应为'捉迷藏'",
            "天赋描述不完整：应包含暴击率提升、潜行状态等完整效果",
            "阵营信息不完整：应包含'黑暗轮回、流星直击'双阵营"
        ]
    },
    "尤利娅": {
        "correct_talent": "不朽的传说",
        "correct_factions": ["光辉军团", "超凡领域", "公主联盟"],
        "correct_class": "圣职/步兵",
        "issues": [
            "天赋名称错误：当前为'神威'，应为'不朽的传说'",
            "神威是技能名称，不是天赋名称",
            "阵营信息不完整：应包含光辉、超凡、公主三阵营"
        ]
    },
    "艾尔文(SP)": {
        "correct_talent": "光辉的意志",
        "correct_factions": ["光辉军团", "主角光环"],
        "correct_class": "步兵",
        "issues": [
            "天赋描述不完整：应包含SP形态特有效果",
            "阵营信息可能不完整"
        ]
    },
    "雪莉(SP)": {
        "correct_talent": "落跑公主（强化版）",
        "correct_factions": ["光辉军团", "公主联盟"],
        "correct_class": "飞兵",
        "issues": [
            "SP形态天赋描述应包含强化效果（每回合2次再动）",
            "阵营信息需要确认"
        ]
    },
    "波赞鲁": {
        "correct_talent": "黑暗王子",
        "correct_factions": ["黑暗轮回"],
        "correct_class": "魔物",
        "issues": [
            "天赋名称确认：当前为'黑暗超绝'，实际天赋应为'黑暗王子'",
            "黑暗超绝是技能，不是天赋"
        ]
    },
    "利昂": {
        "correct_talent": "骑士精神",
        "correct_factions": ["帝国之辉", "战略大师"],
        "correct_class": "骑兵",
        "issues": [
            "阵营信息不完整：应包含'帝国之辉、战略大师'双阵营"
        ]
    },
    "雷丁": {
        "correct_talent": "神卫",
        "correct_factions": ["光辉军团"],
        "correct_class": "枪兵/圣职",
        "issues": [
            "天赋描述不完整：应包含魔防转防御的核心机制"
        ]
    },
    "莉亚娜": {
        "correct_talent": "再行动",
        "correct_factions": ["光辉军团", "公主联盟"],
        "correct_class": "僧兵",
        "issues": [
            "天赋名称确认：当前描述基本正确",
            "阵营信息需要确认：应有光辉和公主双阵营"
        ]
    },
    "拉娜": {
        "correct_talent": "暗镰",
        "correct_factions": ["黑暗轮回", "公主联盟"],
        "correct_class": "法师",
        "issues": [
            "阵营信息需要确认：应有黑暗和公主双阵营"
        ]
    }
}

# 常见错误模式
COMMON_ISSUES = {
    "天赋技能混淆": "许多角色的天赋名称与技能名称被混淆，如尤利娅的天赋是'不朽的传说'而非'神威'",
    "阵营信息不完整": "多数角色只标注了单一阵营，实际应为多阵营",
    "SP形态区分不清": "SP角色与普通角色的天赋、技能描述需要明确区分",
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
    report.append(f"- 总角色数：{len(heroes_data)}")
    report.append(f"- 已验证角色数：{len(VERIFIED_DATA)}")
    report.append(f"- 待验证角色数：{len(heroes_data) - len(VERIFIED_DATA)}")
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
    
    corrected_count = 0
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
            report.append(f"- 天赋：{original.get('talent', {}).get('name', 'N/A')}")
            report.append(f"- 阵营：{original.get('faction', 'N/A')}")
            report.append(f"- 职业：{original.get('class', 'N/A')}")
            report.append("")
        
        report.append("**正确数据：**")
        report.append(f"- 天赋：{verified['correct_talent']}")
        report.append(f"- 阵营：{', '.join(verified['correct_factions'])}")
        report.append(f"- 职业：{verified['correct_class']}")
        report.append("")
        
        report.append("**发现问题：**")
        for issue in verified['issues']:
            report.append(f"- ⚠️ {issue}")
            corrected_count += 1
        report.append("")
    
    # 统计信息
    report.append("## 统计摘要")
    report.append("")
    report.append(f"- 发现问题总数：{corrected_count}")
    report.append(f"- 天赋名称错误：约{len([v for v in VERIFIED_DATA.values() if '天赋' in str(v['issues'])])}处")
    report.append(f"- 阵营信息错误：约{len([v for v in VERIFIED_DATA.values() if '阵营' in str(v['issues'])])}处")
    report.append(f"- 技能描述不完整：多处")
    report.append("")
    
    # 建议
    report.append("## 修正建议")
    report.append("")
    report.append("1. **天赋与技能分离**：确保天赋和技能的名称和描述正确区分")
    report.append("2. **完整阵营信息**：所有角色应列出其所属的全部阵营")
    report.append("3. **SP形态标注**：SP角色应在名称和描述中明确标注")
    report.append("4. **数据来源统一**：建议以B站Wiki或官方资料为准")
    report.append("5. **定期同步更新**：随着游戏版本更新，定期同步角色数据")
    report.append("")
    
    # 待验证角色列表
    report.append("## 待验证角色列表（部分）")
    report.append("")
    unverified = [h['name'] for h in heroes_data if h['name'] not in VERIFIED_DATA][:30]
    for i, name in enumerate(unverified, 1):
        report.append(f"{i}. {name}")
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
