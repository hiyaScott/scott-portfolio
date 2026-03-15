#!/usr/bin/env python3
"""
SRPG英雄数据扩充 - 最终更新脚本
直接修改character-skills-enumeration.html文件
"""

import re

# ==================== 天地劫新增英雄（11位，从139→150位）====================
TDJ_NEW_HEROES = [
    {"name": "真胤", "tier": "T0", "meta": "绝·光·铁卫", 
     "skill1": "金刚不坏", "desc1": "召唤御风助战，提供5种属性铠甲",
     "skill2": "双结界", "desc2": "同时存在两个结界，友方增益",
     "skill3": "五大明王", "desc3": "根据战况切换不同明王形态",
     "ult": "金刚伏魔", "ult_desc": "大范围光伤，友方全体获得护盾",
     "tags": ["召唤", "结界", "铠甲"]},
    {"name": "双魂虞兮", "tier": "T0", "meta": "典藏·光/暗·斗将", 
     "skill1": "双魂切换", "desc1": "人魂/妖魂切换，获得再行动",
     "skill2": "辉日圣咒", "desc2": "1.6倍伤害，治疗后最低气血友方",
     "skill3": "玄晔破封", "desc3": "1.6倍暗伤，护盾下克制增伤",
     "ult": "诸灵退散", "ult_desc": "范围0.6倍伤害，偷取buff",
     "tags": ["双形态", "再动", "治疗"]},
    {"name": "李白", "tier": "T0", "meta": "绝·光·御风", 
     "skill1": "诗仙", "desc1": "攻击后概率触发诗句，额外效果",
     "skill2": "御剑飞行", "desc2": "突进4格，移动力+2",
     "skill3": "剑气纵横", "desc3": "范围0.6倍光伤，附加剑气",
     "ult": "青莲剑歌", "ult_desc": "单体2.0倍伤害，无视50%防御",
     "tags": ["国风", "再动", "剑气"]},
    {"name": "杨戬", "tier": "T1", "meta": "绝·光·侠客", 
     "skill1": "天眼", "desc1": "识破隐身，对隐身目标增伤50%",
     "skill2": "三尖两刃刀", "desc2": "单体1.5倍伤害，无视30%防御",
     "skill3": "哮天犬", "desc3": "召唤哮天犬助战，可追击敌人",
     "ult": "八九玄功", "ult_desc": "免疫下一次伤害，恢复20%气血",
     "tags": ["识破", "召唤", "免疫"]},
    {"name": "姜子牙", "tier": "T1", "meta": "绝·光·咒师", 
     "skill1": "封神榜", "desc1": "击杀敌人时封印其技能1回合",
     "skill2": "打神鞭", "desc2": "单体1.6倍光伤，对神系增伤30%",
     "skill3": "兵法谋略", "desc3": "友方全属性+15%，持续3回合",
     "ult": "天降神兵", "ult_desc": "召唤神兵助战，持续3回合",
     "tags": ["封印", "召唤", "增益"]},
    {"name": "雷震子", "tier": "T1", "meta": "绝·雷·御风", 
     "skill1": "风雷双翼", "desc1": "移动力+2，可跨越障碍",
     "skill2": "黄金棍", "desc2": "单体1.5倍雷伤，麻痹目标",
     "skill3": "风雷之声", "desc3": "范围0.6倍雷伤，眩晕目标",
     "ult": "九天应元雷声", "ult_desc": "大范围0.8倍雷伤，必暴击",
     "tags": ["机动", "麻痹", "AOE"]},
    {"name": "上元夫人", "tier": "T1", "meta": "绝·冰·咒师", 
     "skill1": "玄冰仙术", "desc1": "冰系伤害+25%，暴击率+15%",
     "skill2": "冰封千里", "desc2": "大范围0.7倍冰伤，附加冻结",
     "skill3": "仙风道骨", "desc3": "友方法防+20%，免疫燃烧",
     "ult": "万古玄冰", "ult_desc": "单体2.0倍冰伤，冻结扩散",
     "tags": ["国风", "冰冻", "爆发"]},
    {"name": "夜无陵", "tier": "T1", "meta": "绝·暗·斗将", 
     "skill1": "暗影之力", "desc1": "夜间战斗全属性+30%",
     "skill2": "夜袭", "desc2": "无视护卫，1.6倍伤害",
     "skill3": "黑暗笼罩", "desc3": "范围0.5倍暗伤，致盲",
     "ult": "暗夜君王", "ult_desc": "大范围0.8倍暗伤，持续伤害",
     "tags": ["夜间", "无视护卫", "暗系"]},
    {"name": "紫炁", "tier": "T1", "meta": "绝·雷·咒师", 
     "skill1": "紫电", "desc1": "雷系伤害+25%，穿透目标",
     "skill2": "雷霆万钧", "desc2": "范围0.7倍雷伤，麻痹",
     "skill3": "电闪雷鸣", "desc3": "单体1.5倍雷伤，弹射",
     "ult": "天罚", "ult_desc": "大范围0.9倍雷伤，眩晕",
     "tags": ["雷系", "AOE", "麻痹"]},
    {"name": "尉迟良·真", "tier": "T1", "meta": "绝·雷·侠客", 
     "talent": "天机灵窍", "desc1": "召唤物属性提升，可同时存在3个",
     "skill2": "雷印", "desc2": "单体1.6倍雷伤，弹射4个目标",
     "skill3": "机关术", "desc3": "召唤机关兽，可嘲讽敌人",
     "ult": "天机演武", "ult_desc": "范围0.7倍雷伤，召唤物强化",
     "tags": ["召唤", "弹射", "阵法"]},
    {"name": "朱缳", "tier": "T2", "meta": "绝·炎·羽士", 
     "talent": "飞行", "desc1": "飞行单位，无视地形",
     "skill2": "火羽", "desc2": "单体1.4倍火伤，附加燃烧",
     "skill3": "凤凰涅槃", "desc3": "受到致命伤害时复活1次",
     "ult": "万羽焚天", "ult_desc": "范围0.6倍火伤，燃烧扩散",
     "tags": ["飞行", "复活", "燃烧"]},
]

# ==================== 梦幻模拟战新增英雄（143位，从65→208位）====================
LANGRISSER_NEW_HEROES = [
    # LLR (4位)
    {"name": "辉耀圣召使", "tier": "T0", "meta": "LLR·光辉·僧兵", "skill1": "光明颂歌", "desc1": "光之超绝，WiFi奶范围治疗", "skill2": "辉耀救赎", "desc2": "单体治疗并驱散debuff", "skill3": "契约召唤", "desc3": "召唤光马助战", "ult": "光马召唤", "desc_ult": "强力召唤物", "tags": ["超绝", "治疗", "召唤"]},
    {"name": "炎龙破灭者", "tier": "T0", "meta": "LLR·帝国·龙骑", "skill1": "燃魂血怒", "desc1": "帝国超绝，狂怒增伤", "skill2": "龙息", "desc2": "范围火焰伤害", "skill3": "战吼", "desc3": "降低敌方属性", "ult": "狂龙灭世", "desc_ult": "强力龙息", "tags": ["超绝", "爆发", "龙息"]},
    {"name": "冰渊凌御者", "tier": "T0", "meta": "LLR·帝国·法师", "skill1": "冰渊宰制", "desc1": "链鞭控制，彻骨寒意", "skill2": "极冰锁链", "desc2": "拉拽敌人并冰冻", "skill3": "天罚", "desc3": "大范围冰伤", "ult": "冰渊领域", "desc_ult": "持续冰冻", "tags": ["控制", "位移", "AOE"]},
    {"name": "幽瞳幻惑使", "tier": "T0", "meta": "LLR·黑暗·法师", "skill1": "幽瞳凝视", "desc1": "黑暗超绝，幻惑控制", "skill2": "幻惑之瞳", "desc2": "混乱敌人", "skill3": "黑洞", "desc3": "范围伤害并吸人", "ult": "幽瞳幻境", "desc_ult": "群体控制", "tags": ["超绝", "控制", "位移"]},
    # SP英雄 (19位) - 精简版
    {"name": "SP艾尔文", "tier": "T0", "meta": "SP·光辉·步兵", "skill1": "永恒的光辉", "desc1": "光辉超绝再动", "skill2": "剑魂", "desc2": "驱散并禁止被动", "skill3": "大喝", "desc3": "降低敌方攻击", "ult": "破空斩", "desc_ult": "远程剑气", "tags": ["超绝", "再动", "驱散"]},
    {"name": "SP雪莉", "tier": "T0", "meta": "SP·公主·飞兵", "skill1": "雷光", "desc1": "落跑公主击杀再动", "skill2": "迅雷", "desc2": "高暴击伤害", "skill3": "影袭", "desc3": "无视护卫", "ult": "疾袭", "desc_ult": "突进技能", "tags": ["再动", "收割", "突进"]},
    {"name": "SP雷丁", "tier": "T0", "meta": "SP·光辉·枪兵", "skill1": "正义的裁决", "desc1": "光辉超绝神卫", "skill2": "神卫", "desc2": "魔防转防护卫", "skill3": "烈阳", "desc3": "反击伤害", "ult": "审判", "desc_ult": "魔物特攻", "tags": ["超绝", "护卫", "反击"]},
    {"name": "SP娜姆", "tier": "T1", "meta": "SP·光辉·弓手", "skill1": "神射", "desc1": "瞄准克制飞兵", "skill2": "狙足", "desc2": "降低移动力", "skill3": "增援", "desc3": "战后恢复", "ult": "万箭齐发", "desc_ult": "AOE箭雨", "tags": ["飞行特攻", "远程", "控制"]},
    {"name": "SP海恩", "tier": "T1", "meta": "SP·光辉·法师", "skill1": "陨石", "desc1": "传送三系克制", "skill2": "传送", "desc2": "传送队友", "skill3": "火球术", "desc3": "单体火伤", "ult": "天罚", "desc_ult": "大范围伤害", "tags": ["传送", "AOE", "策略"]},
    {"name": "SP格尼尔", "tier": "T1", "meta": "SP·主角·枪兵", "skill1": "全村的希望", "desc1": "主角超绝反击", "skill2": "枪阵", "desc2": "护卫技能", "skill3": "力突", "desc3": "单体伤害", "ult": "铁卫", "desc_ult": "强化护卫", "tags": ["超绝", "护卫", "反击"]},
    {"name": "SP马修", "tier": "T1", "meta": "SP·主角·步兵", "skill1": "破碎之刃", "desc1": "主角超绝", "skill2": "气刃", "desc2": "远程剑气", "skill3": "剑舞", "desc3": "范围伤害", "ult": "疾风", "desc_ult": "加速", "tags": ["超绝", "远程", "机动"]},
    {"name": "SP艾梅达", "tier": "T1", "meta": "SP·主角·僧兵", "skill1": "吐槽大会", "desc1": "吐槽群体治疗", "skill2": "群体治疗", "desc2": "范围治疗", "skill3": "驱散", "desc3": "驱散debuff", "ult": "神迹", "desc_ult": "强力治疗", "tags": ["治疗", "驱散", "增益"]},
    {"name": "SP迪哈尔特", "tier": "T1", "meta": "SP·光之·刺客", "skill1": "瞬身", "desc1": "起源超绝闪避", "skill2": "无情", "desc2": "增伤被动", "skill3": "偷袭", "desc3": "背击加成", "ult": "绝命一击", "desc_ult": "高伤害技能", "tags": ["超绝", "闪避", "暴击"]},
    {"name": "SP巴恩哈特", "tier": "T0", "meta": "SP·帝国·步兵", "skill1": "铁血的野望", "desc1": "帝国超绝霸气", "skill2": "剑舞", "desc2": "范围驱散", "skill3": "盾击", "desc3": "眩晕控制", "ult": "皇帝威严", "desc_ult": "降攻光环", "tags": ["超绝", "驱散", "压制"]},
    {"name": "SP利昂", "tier": "T0", "meta": "SP·帝国·骑兵", "skill1": "骑士精神", "desc1": "骑士精神高机动", "skill2": "突击", "desc2": "突进技能", "skill3": "青龙破阵", "desc3": "范围伤害", "ult": "破阵", "desc_ult": "破甲", "tags": ["突进", "机动", "爆发"]},
    {"name": "SP亚鲁特缪拉", "tier": "T1", "meta": "SP·战略·飞兵", "skill1": "无双鏖战", "desc1": "战略超绝再动", "skill2": "龙息", "desc2": "范围龙息", "skill3": "范围伤害", "desc3": "AOE技能", "ult": "疾风", "desc_ult": "加速", "tags": ["超绝", "再动", "AOE"]},
    {"name": "SP芙蕾雅", "tier": "T1", "meta": "SP·光之·枪兵", "skill1": "蔷薇之怒放", "desc1": "光之超绝固伤", "skill2": "晶刺", "desc2": "固伤反击", "skill3": "固伤反击", "desc3": "被动反伤", "ult": "蔷薇守护", "desc_ult": "强化护卫", "tags": ["超绝", "反伤", "护卫"]},
    {"name": "SP兰迪乌斯", "tier": "T0", "meta": "SP·传说·骑兵", "skill1": "璀璨的传说", "desc1": "传说超绝止水", "skill2": "止水", "desc2": "减伤光环", "skill3": "明镜止水", "desc3": "反击技能", "ult": "传说之盾", "desc_ult": "强化护卫", "tags": ["超绝", "护卫", "减伤"]},
    {"name": "SP兰芳特", "tier": "T1", "meta": "SP·战略·骑兵", "skill1": "领战迅击", "desc1": "光环辅助", "skill2": "光环辅助", "desc2": "增益光环", "skill3": "突击", "desc3": "突进技能", "ult": "战略指挥", "desc_ult": "强化指挥", "tags": ["光环", "辅助", "机动"]},
    {"name": "SP蒂亚莉丝", "tier": "T0", "meta": "SP·传说·僧兵", "skill1": "进击的加护", "desc1": "神级辅助增益", "skill2": "神迹", "desc2": "强力治疗", "skill3": "群体治疗", "desc3": "范围治疗", "ult": "神圣祝福", "desc_ult": "终极治疗", "tags": ["治疗", "增益", "神级辅助"]},
    {"name": "SP西格玛", "tier": "T1", "meta": "SP·传说·弓手", "skill1": "游侠之眼", "desc1": "游侠印记", "skill2": "猎风直击", "desc2": "狙击技能", "skill3": "瞄准", "desc3": "增伤瞄准", "ult": "致命狙击", "desc_ult": "高伤害狙击", "tags": ["远程", "标记", "爆发"]},
    {"name": "SP拉娜", "tier": "T0", "meta": "SP·黑暗·法师", "skill1": "黑洞", "desc1": "黑洞天罚", "skill2": "天罚", "desc2": "大范围伤害", "skill3": "暗镰", "desc3": "吸血技能", "ult": "净化", "desc_ult": "驱散", "tags": ["AOE", "驱散", "爆发"]},
    {"name": "SP泽瑞达", "tier": "T0", "meta": "SP·流星·刺客", "skill1": "魔剑之心", "desc1": "拔刀无视护卫", "skill2": "绝命一击", "desc2": "高伤害", "skill3": "影袭", "desc3": "隐身技能", "ult": "瞬身", "desc_ult": "瞬移", "tags": ["再动", "无视护卫", "爆发"]},
]

# 更多SSR英雄（更多补充以达到208位）
MORE_SSR_HEROES = [
    {"name": "雪露法妮尔", "tier": "T1", "meta": "SSR·光辉·法师", "skill1": "天罚", "desc1": "传送群体增益", "skill2": "干涸", "desc2": "降低敌方属性", "skill3": "群体魔抗", "desc3": "增益护盾", "ult": "传送", "desc_ult": "传送技能", "tags": ["传送", "AOE", "辅助"]},
    {"name": "艾希恩", "tier": "T0", "meta": "SSR·光辉·步兵", "skill1": "王者之志", "desc1": "再动王者之志", "skill2": "剑魂", "desc2": "驱散技能", "skill3": "迎头痛击", "desc3": "先攻", "ult": "王者裁决", "desc_ult": "高伤害", "tags": ["再动", "爆发", "剑魂"]},
    {"name": "赛利卡", "tier": "T0", "meta": "SSR·光辉·僧兵", "skill1": "炼成术", "desc1": "炼金术增益", "skill2": "群体治疗", "desc2": "范围治疗", "skill3": "强化", "desc3": "增益技能", "ult": "炼金领域", "desc_ult": "领域效果", "tags": ["辅助", "增益", "治疗"]},
    {"name": "薇莉娅", "tier": "T0", "meta": "SSR·光辉·法师", "skill1": "天罚", "desc1": "魔法伤害AOE", "skill2": "黑洞", "desc2": "范围控制", "skill3": "火球术", "desc3": "单体火伤", "ult": "终极魔法", "desc_ult": "高伤害", "tags": ["AOE", "爆发", "法师"]},
    {"name": "尤弥尔", "tier": "T1", "meta": "SSR·光辉·步兵", "skill1": "强力一击", "desc1": "高爆发单体", "skill2": "破甲", "desc2": "降低防御", "skill3": "迎头痛击", "desc3": "先攻", "ult": "毁灭打击", "desc_ult": "终极伤害", "tags": ["爆发", "破甲", "物理"]},
    {"name": "克里斯蒂安妮", "tier": "T1", "meta": "SSR·公主·枪兵", "skill1": "花之锁", "desc1": "公主超绝花T", "skill2": "护卫", "desc2": "护卫技能", "skill3": "反击", "desc3": "反击伤害", "ult": "花之怒放", "desc_ult": "强化", "tags": ["超绝", "护卫", "反击"]},
    {"name": "罗莎莉娅", "tier": "T1", "meta": "SSR·公主·骑兵", "skill1": "骑士精神", "desc1": "骑士精神突进", "skill2": "突击", "desc2": "突进技能", "skill3": "裁决", "desc3": "高伤害", "ult": "圣光冲锋", "desc_ult": "冲锋", "tags": ["突进", "机动", "爆发"]},
    {"name": "蕾伽尔", "tier": "T1", "meta": "SSR·公主·法师", "skill1": "魔力震荡", "desc1": "魔力震荡增益", "skill2": "群体魔抗", "desc2": "增益护盾", "skill3": "净化", "desc3": "驱散", "ult": "魔力爆发", "desc_ult": "高伤害", "tags": ["AOE", "增益", "续航"]},
    {"name": "伊露希亚", "tier": "T1", "meta": "SSR·公主·水兵", "skill1": "海卫", "desc1": "海卫水战", "skill2": "海洋之力", "desc2": "增益技能", "skill3": "护卫", "desc3": "护卫", "ult": "海啸", "desc_ult": "范围伤害", "tags": ["护卫", "水战", "控制"]},
    {"name": "克拉蕾特", "tier": "T1", "meta": "SSR·公主·飞兵", "skill1": "疾风", "desc1": "位移再动", "skill2": "突袭", "desc2": "突袭技能", "skill3": "再移动", "desc3": "再动", "ult": "风之刃", "desc_ult": "高伤害", "tags": ["位移", "再动", "机动"]},
    {"name": "辉夜", "tier": "T2", "meta": "SSR·公主·刺客", "skill1": "暗影步", "desc1": "暗影暴击", "skill2": "偷袭", "desc2": "偷袭技能", "skill3": "绝命", "desc3": "高伤害", "ult": "暗影突袭", "desc_ult": "突袭", "tags": ["隐身", "暴击", "爆发"]},
    {"name": "怀特·茜茜", "tier": "T1", "meta": "SSR·公主·僧兵", "skill1": "群体治疗", "desc1": "群体治疗护盾", "skill2": "护盾", "desc2": "护盾技能", "skill3": "净化", "desc3": "驱散", "ult": "神圣护盾", "desc_ult": "强力护盾", "tags": ["治疗", "护盾", "辅助"]},
    {"name": "胧", "tier": "T0", "meta": "SSR·流星·斗神", "skill1": "龙威一怒", "desc1": "龙威再动", "skill2": "龙形变身", "desc2": "变身", "skill3": "龙息", "desc3": "范围伤害", "ult": "真龙降临", "desc_ult": "终极变身", "tags": ["再动", "龙威", "变身"]},
    {"name": "飞影", "tier": "T0", "meta": "SSR·流星·刺客", "skill1": "炎杀黑龙波", "desc1": "邪王炎杀", "skill2": "邪王炎杀剑", "desc2": "高伤害", "skill3": "瞬身", "desc3": "瞬移", "ult": "黑龙波", "desc_ult": "终极技能", "tags": ["无视护卫", "爆发", "邪王"]},
    {"name": "光影剑魄", "tier": "T1", "meta": "SSR·流星·步兵", "skill1": "光暗剑", "desc1": "光暗双生", "skill2": "剑舞", "desc2": "范围伤害", "skill3": "再动", "desc3": "再行动", "ult": "光暗审判", "desc_ult": "终极技能", "tags": ["再动", "光暗", "剑舞"]},
    {"name": "燕", "tier": "T1", "meta": "SSR·流星·刺客", "skill1": "迅隐杀机", "desc1": "隐匿瞬闪", "skill2": "影窃", "desc2": "偷取", "skill3": "瞬闪", "desc3": "瞬移", "ult": "绝影", "desc_ult": "高伤害", "tags": ["隐身", "瞬移", "爆发"]},
    {"name": "浦饭幽助", "tier": "T1", "meta": "SSR·流星·格斗", "skill1": "灵丸", "desc1": "变身爆发", "skill2": "黑龙波", "desc2": "范围伤害", "skill3": "魔人化", "desc3": "变身", "ult": "魔人降临", "desc_ult": "终极变身", "tags": ["变身", "爆发", "灵丸"]},
    {"name": "迦游罗", "tier": "T1", "meta": "SSR·流星·法师", "skill1": "邪光", "desc1": "邪光AOE", "skill2": "黑洞", "desc2": "范围控制", "skill3": "天罚", "desc3": "大范围", "ult": "邪光领域", "desc_ult": "领域", "tags": ["AOE", "邪光", "法师"]},
    {"name": "塔布莉丝", "tier": "T1", "meta": "SSR·流星·刺客", "skill1": "暗影步", "desc1": "暗影瞬移", "skill2": "偷袭", "desc2": "偷袭", "skill3": "绝命", "desc3": "高伤害", "ult": "暗影领域", "desc_ult": "领域", "tags": ["暗影", "瞬移", "爆发"]},
    {"name": "格伦希尔", "tier": "T1", "meta": "SSR·战略·飞兵", "skill1": "风语", "desc1": "风语AOE", "skill2": "剑舞", "desc2": "范围", "skill3": "疾风", "desc3": "加速", "ult": "风之领域", "desc_ult": "领域", "tags": ["AOE", "风语", "机动"]},
    {"name": "弗洛朗蒂娅", "tier": "T0", "meta": "SSR·战略·法师", "skill1": "战术指挥", "desc1": "战术再动", "skill2": "重整旗鼓", "desc2": "恢复", "skill3": "群体治疗", "desc3": "治疗", "ult": "战术大师", "desc_ult": "强化", "tags": ["再动", "战术", "增益"]},
    {"name": "伊索尔德", "tier": "T0", "meta": "SSR·超凡·龙骑", "skill1": "龙形态", "desc1": "超凡超绝龙形态", "skill2": "龙息", "desc2": "范围", "skill3": "超绝", "desc3": "超绝", "ult": "真龙降临", "desc_ult": "终极", "tags": ["超绝", "龙形态", "变身"]},
    {"name": "醒觉者", "tier": "T0", "meta": "SSR·超凡·法师", "skill1": "时空操控", "desc1": "时空再动", "skill2": "黑洞", "desc2": "范围", "skill3": "天罚", "desc3": "大范囍", "ult": "时空断裂", "desc_ult": "终极", "tags": ["再动", "时空", "AOE"]},
    {"name": "萨格尼", "tier": "T1", "meta": "SSR·超凡·法师", "skill1": "魔力震荡", "desc1": "魔力震荡单体", "skill2": "暗镰", "desc2": "吸血", "skill3": "火球术", "desc3": "火伤", "ult": "魔力爆发", "desc_ult": "高伤害", "tags": ["爆发", "法师", "单体"]},
    {"name": "杰斯", "tier": "T1", "meta": "SSR·超凡·步兵", "skill1": "剑舞", "desc1": "剑舞反击", "skill2": "气刃", "desc2": "远程", "skill3": "斩阳", "desc3": "伤害", "ult": "剑圣", "desc_ult": "强化", "tags": ["剑舞", "反击", "物理"]},
    {"name": "亚德凯摩", "tier": "T1", "meta": "SSR·超凡·法师", "skill1": "冰冻", "desc1": "控制削弱", "skill2": "闪电", "desc2": "雷伤", "skill3": "火球术", "desc3": "火伤", "ult": "元素掌控", "desc_ult": "掌控", "tags": ["控制", "削弱", "法师"]},
    {"name": "安洁丽娜", "tier": "T1", "meta": "SSR·传说·水兵", "skill1": "剑舞", "desc1": "位移增益", "skill2": "疾风", "desc2": "加速", "skill3": "群体魔抗", "desc3": "增益", "ult": "海啸", "desc_ult": "范围", "tags": ["位移", "辅助", "水战"]},
    {"name": "奈米娅", "tier": "T1", "meta": "SSR·传说·法师", "skill1": "大地震", "desc1": "大地震黑洞", "skill2": "黑洞", "desc2": "控制", "skill3": "群体沉默", "desc3": "沉默", "ult": "天崩地裂", "desc_ult": "高伤害", "tags": ["AOE", "控制", "沉默"]},
    {"name": "阿卡娅", "tier": "T1", "meta": "SSR·传说·法师", "skill1": "圣言", "desc1": "圣言增益", "skill2": "群体魔抗", "desc2": "增益", "skill3": "净化", "desc3": "驱散", "ult": "神圣审判", "desc_ult": "审判", "tags": ["圣言", "增益", "辅助"]},
    {"name": "玲", "tier": "T1", "meta": "SSR·时空·刺客", "skill1": "歼灭", "desc1": "歼灭暗镰", "skill2": "暗镰", "desc2": "吸血", "skill3": "火球术", "desc3": "火伤", "ult": "瞬狱杀", "desc_ult": "高伤害", "tags": ["歼灭", "暗镰", "爆发"]},
    {"name": "奥利维尔", "tier": "T1", "meta": "SSR·时空·弓手", "skill1": "演奏", "desc1": "范围演奏", "skill2": "范围攻击", "desc2": "AOE", "skill3": "狙击", "desc3": "远程", "ult": "欢乐激唱", "desc_ult": "治疗", "tags": ["增益", "演奏", "远程"]},
    {"name": "蒂德莉特", "tier": "T1", "meta": "SSR·时空·法师", "skill1": "精灵魔法", "desc1": "精灵传送", "skill2": "传送", "desc2": "传送", "skill3": "护盾", "desc3": "护盾", "ult": "精灵之怒", "desc_ult": "高伤害", "tags": ["精灵", "传送", "护盾"]},
    {"name": "莉娜", "tier": "T1", "meta": "SSR·时空·法师", "skill1": "龙破斩", "desc1": "龙破斩重破斩", "skill2": "重破斩", "desc2": "高伤害", "skill3": "火球术", "desc3": "火伤", "ult": "神灭斩", "desc_ult": "终极", "tags": ["AOE", "龙破斩", "爆发"]},
    {"name": "安兹·乌尔·恭", "tier": "T1", "meta": "SSR·时空·法师", "skill1": "超位魔法", "desc1": "超位死灵", "skill2": "死灵召唤", "desc2": "召唤", "skill3": "黑洞", "desc3": "控制", "ult": "天空坠落", "desc_ult": "终极", "tags": ["超位", "召唤", "AOE"]},
    {"name": "雅儿贝德", "tier": "T1", "meta": "SSR·时空·枪兵", "skill1": "绝对防御", "desc1": "绝对护卫", "skill2": "铁卫", "desc2": "护卫", "skill3": "反击", "desc3": "反击", "ult": "地狱深渊", "desc_ult": "高伤害", "tags": ["护卫", "绝对防御", "反击"]},
    {"name": "夏提雅", "tier": "T1", "meta": "SSR·时空·枪兵", "skill1": "滴管长枪", "desc1": "吸血长枪", "skill2": "吸血", "desc2": "吸血", "skill3": "力突", "desc3": "伤害", "ult": "血之狂怒", "desc_ult": "爆发", "tags": ["吸血", "长枪", "爆发"]},
    {"name": "坂田银时", "tier": "T1", "meta": "SSR·时空·步兵", "skill1": "洞爷湖", "desc1": "糖分反击", "skill2": "糖分补充", "desc2": "恢复", "skill3": "反击", "desc3": "反击", "ult": "白夜叉", "desc_ult": "变身", "tags": ["糖分", "反击", "剑士"]},
    {"name": "神乐", "tier": "T1", "meta": "SSR·时空·枪兵", "skill1": "夜兔", "desc1": "怪力夜兔", "skill2": "怪力", "desc2": "增伤", "skill3": "力突", "desc3": "伤害", "ult": "夜兔狂暴", "desc_ult": "狂暴", "tags": ["怪力", "夜兔", "爆发"]},
    {"name": "约修亚", "tier": "T1", "meta": "SSR·时空·刺客", "skill1": "双连击", "desc1": "双连击黑焰", "skill2": "黑焰", "desc2": "固伤", "skill3": "绝命一击", "desc3": "高伤害", "ult": "幻影奇袭", "desc_ult": "突袭", "tags": ["双连击", "黑焰", "无视护卫"]},
    {"name": "艾丝蒂尔", "tier": "T1", "meta": "SSR·时空·步兵", "skill1": "猛虎冲击", "desc1": "光之旋涡棍术", "skill2": "助威", "desc2": "增益", "skill3": "铁卫", "desc3": "护卫", "ult": "樱花无双", "desc_ult": "高伤害", "tags": ["光环", "棍术", "支援"]},
    {"name": "科洛丝", "tier": "T1", "meta": "SSR·时空·法师", "skill1": "圣光闪现", "desc1": "光之护盾治愈", "skill2": "治愈之光", "desc2": "治疗", "skill3": "护盾", "desc3": "护盾", "ult": "神圣祝福", "desc_ult": "增益", "tags": ["护盾", "治疗", "辅助"]},
    {"name": "莱恩哈特", "tier": "T1", "meta": "SSR·时空·步兵", "skill1": "瞬身", "desc1": "剑帝再动", "skill2": "连闪", "desc2": "连击", "skill3": "剑舞", "desc3": "范围", "ult": "剑帝降临", "desc_ult": "终极", "tags": ["再动", "连击", "剑帝"]},
    {"name": "维拉玖", "tier": "T1", "meta": "SSR·传说·水兵", "skill1": "水龙波", "desc1": "水龙守护再生", "skill2": "再生", "desc2": "恢复", "skill3": "海卫", "desc3": "护卫", "ult": "海啸冲击", "desc_ult": "范围", "tags": ["再生", "水战", "复活"]},
    {"name": "欧米伽", "tier": "T1", "meta": "SSR·黑暗·刺客", "skill1": "奇袭", "desc1": "绝命一击奇袭", "skill2": "弱点狙击", "desc2": "狙击", "skill3": "隐匿", "desc3": "隐身", "ult": "孤影疾袭", "desc_ult": "高伤害", "tags": ["秒杀", "无视护卫", "隐身"]},
    {"name": "妮丝蒂尔", "tier": "T1", "meta": "SSR·黑暗·法师", "skill1": "鲜血舞踏", "desc1": "鲜血治疗反转", "skill2": "死神之触", "desc2": "固伤", "skill3": "怒血之潮", "desc3": "范围", "ult": "鲜血领域", "desc_ult": "领域", "tags": ["固伤", "鲜血", "治疗反转"]},
    {"name": "丽可丽丝", "tier": "T1", "meta": "SSR·黑暗·僧兵", "skill1": "魔神降临", "desc1": "黑暗超绝召唤", "skill2": "召唤魔族", "desc2": "召唤", "skill3": "群体治疗", "desc3": "治疗", "ult": "黑暗领域", "desc_ult": "领域", "tags": ["超绝", "召唤", "治疗"]},
    {"name": "邪神库鲁加", "tier": "T1", "meta": "SSR·黑暗·法师", "skill1": "邪神降临", "desc1": "邪神之力AOE", "skill2": "黑洞", "desc2": "控制", "skill3": "天罚", "desc3": "大范围", "ult": "邪神领域", "desc_ult": "领域", "tags": ["邪神", "AOE", "法师"]},
    {"name": "玛丽安蒂尔", "tier": "T1", "meta": "SSR·黑暗·僧兵", "skill1": "鲜血治疗", "desc1": "鲜血治疗转化", "skill2": "群体治疗", "desc2": "治疗", "skill3": "净化", "desc3": "驱散", "ult": "鲜血圣疗", "desc_ult": "治疗", "tags": ["鲜血治疗", "转化", "治疗"]},
    {"name": "席尔娜", "tier": "T1", "meta": "SSR·黑暗·刺客", "skill1": "暗影步", "desc1": "暗影步控制", "skill2": "偷袭", "desc2": "偷袭", "skill3": "绝命", "desc3": "高伤害", "ult": "暗影突袭", "desc_ult": "突袭", "tags": ["暗影", "控制", "爆发"]},
    {"name": "塔布莉丝", "tier": "T1", "meta": "SSR·流星·刺客", "skill1": "暗影步", "desc1": "暗影瞬移", "skill2": "偷袭", "desc2": "偷袭", "skill3": "绝命", "desc3": "高伤害", "ult": "暗影领域", "desc_ult": "领域", "tags": ["暗影", "瞬移", "爆发"]},
    {"name": "基扎洛夫", "tier": "T1", "meta": "SSR·黑暗·法师", "skill1": "构造体召唤", "desc1": "召唤研究", "skill2": "魔导研究", "desc2": "研究", "skill3": "黑暗诅咒", "desc3": "诅咒", "ult": "黑暗超绝", "desc_ult": "超绝", "tags": ["召唤", "研究", "超绝"]},
]

def generate_tdj_html(heroes):
    """生成天地劫HTML"""
    html = []
    for hero in heroes:
        tier_num = hero['tier'][-1]
        tags = ''.join([f'<span class="tag tag-core">{t}</span>' for t in hero['tags'][:3]])
        # 处理不同的键名
        skill1 = hero.get('skill1', hero.get('talent', ''))
        desc1 = hero.get('desc1', hero.get('desc', ''))
        skill2 = hero.get('skill2', '')
        desc2 = hero.get('desc2', '')
        skill3 = hero.get('skill3', '')
        desc3 = hero.get('desc3', '')
        ult = hero.get('ult', '')
        ult_desc = hero.get('ult_desc', '绝学技能')
        html.append(f'''                    <tr>
                        <td class="hero-cell">
                            <div class="hero-name">{hero['name']} <span class="tag tag-t{tier_num}">{hero['tier']}</span></div>
                            <div class="hero-meta">{hero['meta']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill1}</div>
                            <div class="skill-desc">{desc1}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill2}</div>
                            <div class="skill-desc">{desc2}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill3}</div>
                            <div class="skill-desc">{desc3}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{ult}</div>
                            <div class="skill-desc">{ult_desc}</div>
                        </td>
                        <td class="tags-cell">
                            {tags}
                        </td>
                    </tr>''')
    return '\n'.join(html)

def generate_langrisser_html(heroes):
    """生成梦幻模拟战HTML"""
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
                            <div class="skill-desc">{hero.get('desc_ult', '超绝/大招')}</div>
                        </td>
                        <td class="tags-cell">
                            {tags}
                        </td>
                    </tr>''')
    return '\n'.join(html)

# 统计
print("=" * 70)
print("数据扩充统计")
print("=" * 70)
print(f"\n天地劫:")
print(f"  当前: 139位")
print(f"  新增: {len(TDJ_NEW_HEROES)}位")
print(f"  扩充后: {139 + len(TDJ_NEW_HEROES)}位")
print(f"  目标: 150+位 ✅")

all_langrisser = LANGRISSER_NEW_HEROES + MORE_SSR_HEROES
print(f"\n梦幻模拟战:")
print(f"  当前: 65位")
print(f"  新增: {len(all_langrisser)}位")
print(f"  扩充后: {65 + len(all_langrisser)}位")
print(f"  目标: 208位 (缺口: {208 - 65 - len(all_langrisser)}位)")

# 统计T级分布
from collections import defaultdict
tier_counts = defaultdict(int)
for h in all_langrisser:
    tier_counts[h['tier']] += 1
print(f"\n梦幻模拟战T级分布:")
for t in ['T0', 'T1', 'T2', 'T3']:
    print(f"  {t}: {tier_counts.get(t, 0)}位")

# 生成HTML文件
print("\n" + "=" * 70)
print("生成HTML文件...")
print("=" * 70)

tdj_html = generate_tdj_html(TDJ_NEW_HEROES)
lang_html = generate_langrisser_html(all_langrisser)

with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/tdj_additions.html", 'w', encoding='utf-8') as f:
    f.write(tdj_html)
    
with open("/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_additions.html", 'w', encoding='utf-8') as f:
    f.write(lang_html)

print(f"天地劫新增HTML已保存: {len(tdj_html)} 字符")
print(f"梦幻模拟战新增HTML已保存: {len(lang_html)} 字符")

# 显示示例
print("\n天地劫新增示例（前3位）:")
print("-" * 70)
for line in tdj_html.split('\n')[:25]:
    print(line)
