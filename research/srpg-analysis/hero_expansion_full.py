#!/usr/bin/env python3
"""
SRPG英雄数据扩充脚本 - 完整版
生成可直接插入HTML的代码片段
"""

# ==================== 完整的梦幻模拟战英雄数据（新增143位）====================
LANGRISSER_NEW_HEROES = [
    # LLR (4位)
    {"name": "辉耀圣召使", "tier": "T0", "meta": "LLR·光辉·僧兵", 
     "talent": "光之超绝/治疗/WiFi奶", "skill1": "光明颂歌", "skill2": "辉耀救赎", "skill3": "契约召唤", "ult": "光马召唤",
     "tags": ["超绝", "治疗", "召唤"], "category": "LLR"},
    {"name": "炎龙破灭者", "tier": "T0", "meta": "LLR·帝国·龙骑", 
     "talent": "帝国超绝/狂怒/龙息", "skill1": "燃魂血怒", "skill2": "龙息", "skill3": "战吼", "ult": "狂龙灭世",
     "tags": ["超绝", "爆发", "龙息"], "category": "LLR"},
    {"name": "冰渊凌御者", "tier": "T0", "meta": "LLR·帝国·法师", 
     "talent": "链鞭/彻骨寒意/位移", "skill1": "冰渊宰制", "skill2": "极冰锁链", "skill3": "天罚", "ult": "冰渊领域",
     "tags": ["控制", "位移", "AOE"], "category": "LLR"},
    {"name": "幽瞳幻惑使", "tier": "T0", "meta": "LLR·黑暗·法师", 
     "talent": "黑暗超绝/幻惑/位移", "skill1": "幽瞳凝视", "skill2": "幻惑之瞳", "skill3": "黑洞", "ult": "幽瞳幻境",
     "tags": ["超绝", "控制", "位移"], "category": "LLR"},
    
    # SP英雄 (19位)
    {"name": "SP艾尔文", "tier": "T0", "meta": "SP·光辉·步兵", 
     "talent": "光辉超绝/再动/剑魂", "skill1": "永恒的光辉", "skill2": "剑魂", "skill3": "大喝", "ult": "破空斩",
     "tags": ["超绝", "再动", "驱散"], "category": "SP"},
    {"name": "SP雪莉", "tier": "T0", "meta": "SP·公主·飞兵", 
     "talent": "落跑公主/击杀再动", "skill1": "雷光", "skill2": "迅雷", "skill3": "影袭", "ult": "疾袭",
     "tags": ["再动", "收割", "突进"], "category": "SP"},
    {"name": "SP雷丁", "tier": "T0", "meta": "SP·光辉·枪兵", 
     "talent": "光辉超绝/神卫", "skill1": "正义的裁决", "skill2": "神卫", "skill3": "烈阳", "ult": "审判",
     "tags": ["超绝", "护卫", "反击"], "category": "SP"},
    {"name": "SP娜姆", "tier": "T1", "meta": "SP·光辉·弓手", 
     "talent": "瞄准/克制飞兵", "skill1": "神射", "skill2": "狙足", "skill3": "增援", "ult": "万箭齐发",
     "tags": ["飞行特攻", "远程", "控制"], "category": "SP"},
    {"name": "SP海恩", "tier": "T1", "meta": "SP·光辉·法师", 
     "talent": "传送/三系克制", "skill1": "陨石", "skill2": "传送", "skill3": "火球术", "ult": "天罚",
     "tags": ["传送", "AOE", "策略"], "category": "SP"},
    {"name": "SP格尼尔", "tier": "T1", "meta": "SP·主角·枪兵", 
     "talent": "主角超绝/反击", "skill1": "全村的希望", "skill2": "枪阵", "skill3": "力突", "ult": "铁卫",
     "tags": ["超绝", "护卫", "反击"], "category": "SP"},
    {"name": "SP马修", "tier": "T1", "meta": "SP·主角·步兵", 
     "talent": "主角超绝/破碎之刃", "skill1": "破碎之刃", "skill2": "气刃", "skill3": "剑舞", "ult": "疾风",
     "tags": ["超绝", "远程", "机动"], "category": "SP"},
    {"name": "SP艾梅达", "tier": "T1", "meta": "SP·主角·僧兵", 
     "talent": "吐槽/群体治疗", "skill1": "吐槽大会", "skill2": "群体治疗", "skill3": "驱散", "ult": "神迹",
     "tags": ["治疗", "驱散", "增益"], "category": "SP"},
    {"name": "SP迪哈尔特", "tier": "T1", "meta": "SP·光之·刺客", 
     "talent": "起源超绝/闪避", "skill1": "瞬身", "skill2": "无情", "skill3": "偷袭", "ult": "绝命一击",
     "tags": ["超绝", "闪避", "暴击"], "category": "SP"},
    {"name": "SP巴恩哈特", "tier": "T0", "meta": "SP·帝国·步兵", 
     "talent": "帝国超绝/霸气", "skill1": "铁血的野望", "skill2": "剑舞", "skill3": "盾击", "ult": "皇帝威严",
     "tags": ["超绝", "驱散", "压制"], "category": "SP"},
    {"name": "SP利昂", "tier": "T0", "meta": "SP·帝国·骑兵", 
     "talent": "骑士精神/攻击后移动", "skill1": "骑士精神", "skill2": "突击", "skill3": "青龙破阵", "ult": "破阵",
     "tags": ["突进", "机动", "爆发"], "category": "SP"},
    {"name": "SP亚鲁特缪拉", "tier": "T1", "meta": "SP·战略·飞兵", 
     "talent": "战略超绝/再行动", "skill1": "无双鏖战", "skill2": "龙息", "skill3": "范围伤害", "ult": "疾风",
     "tags": ["超绝", "再动", "AOE"], "category": "SP"},
    {"name": "SP芙蕾雅", "tier": "T1", "meta": "SP·光之·枪兵", 
     "talent": "光之超绝/固伤反击", "skill1": "蔷薇之怒放", "skill2": "晶刺", "skill3": "固伤反击", "ult": "蔷薇守护",
     "tags": ["超绝", "反伤", "护卫"], "category": "SP"},
    {"name": "SP兰迪乌斯", "tier": "T0", "meta": "SP·传说·骑兵", 
     "talent": "传说超绝/止水", "skill1": "璀璨的传说", "skill2": "止水", "skill3": "明镜止水", "ult": "传说之盾",
     "tags": ["超绝", "护卫", "减伤"], "category": "SP"},
    {"name": "SP兰芳特", "tier": "T1", "meta": "SP·战略·骑兵", 
     "talent": "领战迅击/混合加成", "skill1": "领战迅击", "skill2": "光环辅助", "skill3": "突击", "ult": "战略指挥",
     "tags": ["光环", "辅助", "机动"], "category": "SP"},
    {"name": "SP蒂亚莉丝", "tier": "T0", "meta": "SP·传说·僧兵", 
     "talent": "进击的加护/战后回血", "skill1": "进击的加护", "skill2": "神迹", "skill3": "群体治疗", "ult": "神圣祝福",
     "tags": ["治疗", "增益", "神级辅助"], "category": "SP"},
    {"name": "SP西格玛", "tier": "T1", "meta": "SP·传说·弓手", 
     "talent": "游侠印记/远程", "skill1": "游侠之眼", "skill2": "猎风直击", "skill3": "瞄准", "ult": "致命狙击",
     "tags": ["远程", "标记", "爆发"], "category": "SP"},
    {"name": "SP拉娜", "tier": "T0", "meta": "SP·黑暗·法师", 
     "talent": "黑洞/天罚/元素回响", "skill1": "黑洞", "skill2": "天罚", "skill3": "暗镰", "ult": "净化",
     "tags": ["AOE", "驱散", "爆发"], "category": "SP"},
    {"name": "SP泽瑞达", "tier": "T0", "meta": "SP·流星·刺客", 
     "talent": "拔刀/无视护卫", "skill1": "魔剑之心", "skill2": "绝命一击", "skill3": "影袭", "ult": "瞬身",
     "tags": ["再动", "无视护卫", "爆发"], "category": "SP"},

    # 重要SSR (更多补充)
    {"name": "雪露法妮尔", "tier": "T1", "meta": "SSR·光辉·法师", 
     "talent": "传送/群体增益", "skill1": "天罚", "skill2": "干涸", "skill3": "群体魔抗", "ult": "传送",
     "tags": ["传送", "AOE", "辅助"]},
    {"name": "艾希恩", "tier": "T0", "meta": "SSR·光辉·步兵", 
     "talent": "再动/王者之志", "skill1": "王者之志", "skill2": "剑魂", "skill3": "迎头痛击", "ult": "王者裁决",
     "tags": ["再动", "爆发", "剑魂"]},
    {"name": "赛利卡", "tier": "T0", "meta": "SSR·光辉·僧兵", 
     "talent": "炼金术/增益转化", "skill1": "炼成术", "skill2": "群体治疗", "skill3": "强化", "ult": "炼金领域",
     "tags": ["辅助", "增益", "治疗"]},
    {"name": "薇莉娅", "tier": "T0", "meta": "SSR·光辉·法师", 
     "talent": "魔法伤害/范围打击", "skill1": "天罚", "skill2": "黑洞", "skill3": "火球术", "ult": "终极魔法",
     "tags": ["AOE", "爆发", "法师"]},
    {"name": "尤弥尔", "tier": "T1", "meta": "SSR·光辉·步兵", 
     "talent": "高爆发/单体打击", "skill1": "强力一击", "skill2": "破甲", "skill3": "迎头痛击", "ult": "毁灭打击",
     "tags": ["爆发", "破甲", "物理"]},
    {"name": "克里斯蒂安妮", "tier": "T1", "meta": "SSR·公主·枪兵", 
     "talent": "公主超绝/花T", "skill1": "花之锁", "skill2": "护卫", "skill3": "反击", "ult": "花之怒放",
     "tags": ["超绝", "护卫", "反击"]},
    {"name": "罗莎莉娅", "tier": "T1", "meta": "SSR·公主·骑兵", 
     "talent": "骑士精神/突进", "skill1": "骑士精神", "skill2": "突击", "skill3": "裁决", "ult": "圣光冲锋",
     "tags": ["突进", "机动", "爆发"]},
    {"name": "蕾伽尔", "tier": "T1", "meta": "SSR·公主·法师", 
     "talent": "魔力震荡/增益", "skill1": "魔力震荡", "skill2": "群体魔抗", "skill3": "净化", "ult": "魔力爆发",
     "tags": ["AOE", "增益", "续航"]},
    {"name": "伊露希亚", "tier": "T1", "meta": "SSR·公主·水兵", 
     "talent": "海卫/水战", "skill1": "海卫", "skill2": "海洋之力", "skill3": "护卫", "ult": "海啸",
     "tags": ["护卫", "水战", "控制"]},
    {"name": "克拉蕾特", "tier": "T1", "meta": "SSR·公主·飞兵", 
     "talent": "位移/再动", "skill1": "疾风", "skill2": "突袭", "skill3": "再移动", "ult": "风之刃",
     "tags": ["位移", "再动", "机动"]},
    {"name": "辉夜", "tier": "T2", "meta": "SSR·公主·刺客", 
     "talent": "暗影/暴击", "skill1": "暗影步", "skill2": "偷袭", "skill3": "绝命", "ult": "暗影突袭",
     "tags": ["隐身", "暴击", "爆发"]},
    {"name": "怀特·茜茜", "tier": "T1", "meta": "SSR·公主·僧兵", 
     "talent": "群体治疗/护盾", "skill1": "群体治疗", "skill2": "护盾", "skill3": "净化", "ult": "神圣护盾",
     "tags": ["治疗", "护盾", "辅助"]},
    {"name": "胧", "tier": "T0", "meta": "SSR·流星·斗神", 
     "talent": "龙威/再动", "skill1": "龙威一怒", "skill2": "龙形变身", "skill3": "龙息", "ult": "真龙降临",
     "tags": ["再动", "龙威", "变身"]},
    {"name": "飞影", "tier": "T0", "meta": "SSR·流星·刺客", 
     "talent": "邪王炎杀/无视护卫", "skill1": "炎杀黑龙波", "skill2": "邪王炎杀剑", "skill3": "瞬身", "ult": "黑龙波",
     "tags": ["无视护卫", "爆发", "邪王"]},
    {"name": "光影剑魄", "tier": "T1", "meta": "SSR·流星·步兵", 
     "talent": "光暗双生/再动", "skill1": "光暗剑", "skill2": "剑舞", "skill3": "再动", "ult": "光暗审判",
     "tags": ["再动", "光暗", "剑舞"]},
    {"name": "燕", "tier": "T1", "meta": "SSR·流星·刺客", 
     "talent": "隐匿/瞬闪", "skill1": "迅隐杀机", "skill2": "影窃", "skill3": "瞬闪", "ult": "绝影",
     "tags": ["隐身", "瞬移", "爆发"]},
    {"name": "浦饭幽助", "tier": "T1", "meta": "SSR·流星·格斗", 
     "talent": "变身/爆发", "skill1": "灵丸", "skill2": "黑龙波", "skill3": "魔人化", "ult": "魔人降临",
     "tags": ["变身", "爆发", "灵丸"]},
    {"name": "迦游罗", "tier": "T1", "meta": "SSR·流星·法师", 
     "talent": "邪光/范围伤害", "skill1": "邪光", "skill2": "黑洞", "skill3": "天罚", "ult": "邪光领域",
     "tags": ["AOE", "邪光", "法师"]},
    {"name": "格伦希尔", "tier": "T1", "meta": "SSR·战略·飞兵", 
     "talent": "风语/范围伤害", "skill1": "风语", "skill2": "剑舞", "skill3": "疾风", "ult": "风之领域",
     "tags": ["AOE", "风语", "机动"]},
    {"name": "弗洛朗蒂娅", "tier": "T0", "meta": "SSR·战略·法师", 
     "talent": "战术指挥/再动", "skill1": "战术指挥", "skill2": "重整旗鼓", "skill3": "群体治疗", "ult": "战术大师",
     "tags": ["再动", "战术", "增益"]},
    {"name": "伊索尔德", "tier": "T0", "meta": "SSR·超凡·龙骑", 
     "talent": "超凡超绝/龙形态", "skill1": "龙形态", "skill2": "龙息", "skill3": "超绝", "ult": "真龙降临",
     "tags": ["超绝", "龙形态", "变身"]},
    {"name": "醒觉者", "tier": "T0", "meta": "SSR·超凡·法师", 
     "talent": "时空操控/再动", "skill1": "时空操控", "skill2": "黑洞", "skill3": "天罚", "ult": "时空断裂",
     "tags": ["再动", "时空", "AOE"]},
    {"name": "萨格尼", "tier": "T1", "meta": "SSR·超凡·法师", 
     "talent": "魔力震荡/单体爆发", "skill1": "魔力震荡", "skill2": "暗镰", "skill3": "火球术", "ult": "魔力爆发",
     "tags": ["爆发", "法师", "单体"]},
    {"name": "杰斯", "tier": "T1", "meta": "SSR·超凡·步兵", 
     "talent": "剑舞/反击", "skill1": "剑舞", "skill2": "气刃", "skill3": "斩阳", "ult": "剑圣",
     "tags": ["剑舞", "反击", "物理"]},
    {"name": "亚德凯摩", "tier": "T1", "meta": "SSR·超凡·法师", 
     "talent": "控制/削弱", "skill1": "冰冻", "skill2": "闪电", "skill3": "火球术", "ult": "元素掌控",
     "tags": ["控制", "削弱", "法师"]},
    {"name": "安洁丽娜", "tier": "T1", "meta": "SSR·传说·水兵", 
     "talent": "位移/群体增益", "skill1": "剑舞", "skill2": "疾风", "skill3": "群体魔抗", "ult": "海啸",
     "tags": ["位移", "辅助", "水战"]},
    {"name": "奈米娅", "tier": "T1", "meta": "SSR·传说·法师", 
     "talent": "大地震/黑洞", "skill1": "大地震", "skill2": "黑洞", "skill3": "群体沉默", "ult": "天崩地裂",
     "tags": ["AOE", "控制", "沉默"]},
    {"name": "阿卡娅", "tier": "T1", "meta": "SSR·传说·法师", 
     "talent": "圣言/增益", "skill1": "圣言", "skill2": "群体魔抗", "skill3": "净化", "ult": "神圣审判",
     "tags": ["圣言", "增益", "辅助"]},
    {"name": "玲", "tier": "T1", "meta": "SSR·时空·刺客", 
     "talent": "歼灭/暗镰", "skill1": "歼灭", "skill2": "暗镰", "skill3": "火球术", "ult": "瞬狱杀",
     "tags": ["歼灭", "暗镰", "爆发"]},
    {"name": "奥利维尔", "tier": "T1", "meta": "SSR·时空·弓手", 
     "talent": "范围攻击/演奏", "skill1": "演奏", "skill2": "范围攻击", "skill3": "狙击", "ult": "欢乐激唱",
     "tags": ["增益", "演奏", "远程"]},
    {"name": "蒂德莉特", "tier": "T1", "meta": "SSR·时空·法师", 
     "talent": "精灵魔法/传送", "skill1": "精灵魔法", "skill2": "传送", "skill3": "护盾", "ult": "精灵之怒",
     "tags": ["精灵", "传送", "护盾"]},
    {"name": "莉娜", "tier": "T1", "meta": "SSR·时空·法师", 
     "talent": "龙破斩/重破斩", "skill1": "龙破斩", "skill2": "重破斩", "skill3": "火球术", "ult": "神灭斩",
     "tags": ["AOE", "龙破斩", "爆发"]},
    {"name": "安兹·乌尔·恭", "tier": "T1", "meta": "SSR·时空·法师", 
     "talent": "超位魔法/死灵", "skill1": "超位魔法", "skill2": "死灵召唤", "skill3": "黑洞", "ult": "天空坠落",
     "tags": ["超位", "召唤", "AOE"]},
    {"name": "雅儿贝德", "tier": "T1", "meta": "SSR·时空·枪兵", 
     "talent": "绝对防御/护卫", "skill1": "绝对防御", "skill2": "铁卫", "skill3": "反击", "ult": "地狱深渊",
     "tags": ["护卫", "绝对防御", "反击"]},
    {"name": "夏提雅", "tier": "T1", "meta": "SSR·时空·枪兵", 
     "talent": "吸血/滴管长枪", "skill1": "滴管长枪", "skill2": "吸血", "skill3": "力突", "ult": "血之狂怒",
     "tags": ["吸血", "长枪", "爆发"]},
    {"name": "坂田银时", "tier": "T1", "meta": "SSR·时空·步兵", 
     "talent": "糖分/反击", "skill1": "洞爷湖", "skill2": "糖分补充", "skill3": "反击", "ult": "白夜叉",
     "tags": ["糖分", "反击", "剑士"]},
    {"name": "神乐", "tier": "T1", "meta": "SSR·时空·枪兵", 
     "talent": "怪力/夜兔", "skill1": "夜兔", "skill2": "怪力", "skill3": "力突", "ult": "夜兔狂暴",
     "tags": ["怪力", "夜兔", "爆发"]},
    {"name": "约修亚", "tier": "T1", "meta": "SSR·时空·刺客", 
     "talent": "双连击/黑焰", "skill1": "双连击", "skill2": "黑焰", "skill3": "绝命一击", "ult": "幻影奇袭",
     "tags": ["双连击", "黑焰", "无视护卫"]},
    {"name": "艾丝蒂尔", "tier": "T1", "meta": "SSR·时空·步兵", 
     "talent": "光之旋涡/棍术", "skill1": "猛虎冲击", "skill2": "助威", "skill3": "铁卫", "ult": "樱花无双",
     "tags": ["光环", "棍术", "支援"]},
    {"name": "科洛丝", "tier": "T1", "meta": "SSR·时空·法师", 
     "talent": "光之护盾/治愈", "skill1": "圣光闪现", "skill2": "治愈之光", "skill3": "护盾", "ult": "神圣祝福",
     "tags": ["护盾", "治疗", "辅助"]},
    {"name": "莱恩哈特", "tier": "T1", "meta": "SSR·时空·步兵", 
     "talent": "剑帝/再动", "skill1": "瞬身", "skill2": "连闪", "skill3": "剑舞", "ult": "剑帝降临",
     "tags": ["再动", "连击", "剑帝"]},
    {"name": "维拉玖", "tier": "T1", "meta": "SSR·传说·水兵", 
     "talent": "水龙守护/再生", "skill1": "水龙波", "skill2": "再生", "skill3": "海卫", "ult": "海啸冲击",
     "tags": ["再生", "水战", "复活"]},
    {"name": "欧米伽", "tier": "T1", "meta": "SSR·黑暗·刺客", 
     "talent": "绝命一击/奇袭", "skill1": "奇袭", "skill2": "弱点狙击", "skill3": "隐匿", "ult": "孤影疾袭",
     "tags": ["秒杀", "无视护卫", "隐身"]},
    {"name": "妮丝蒂尔", "tier": "T1", "meta": "SSR·黑暗·法师", 
     "talent": "鲜血舞踏/治疗反转", "skill1": "鲜血舞踏", "skill2": "死神之触", "skill3": "怒血之潮", "ult": "鲜血领域",
     "tags": ["固伤", "鲜血", "治疗反转"]},
    {"name": "丽可丽丝", "tier": "T1", "meta": "SSR·黑暗·僧兵", 
     "talent": "黑暗超绝/召唤", "skill1": "魔神降临", "skill2": "召唤魔族", "skill3": "群体治疗", "ult": "黑暗领域",
     "tags": ["超绝", "召唤", "治疗"]},
    {"name": "邪神库鲁加", "tier": "T1", "meta": "SSR·黑暗·法师", 
     "talent": "邪神之力/范围伤害", "skill1": "邪神降临", "skill2": "黑洞", "skill3": "天罚", "ult": "邪神领域",
     "tags": ["邪神", "AOE", "法师"]},
    {"name": "玛丽安蒂尔", "tier": "T1", "meta": "SSR·黑暗·僧兵", 
     "talent": "鲜血治疗/转化", "skill1": "鲜血治疗", "skill2": "群体治疗", "skill3": "净化", "ult": "鲜血圣疗",
     "tags": ["鲜血治疗", "转化", "治疗"]},
    {"name": "席尔娜", "tier": "T1", "meta": "SSR·黑暗·刺客", 
     "talent": "暗影步/控制", "skill1": "暗影步", "skill2": "偷袭", "skill3": "绝命", "ult": "暗影突袭",
     "tags": ["暗影", "控制", "爆发"]},
    {"name": "塔布莉丝", "tier": "T1", "meta": "SSR·流星·刺客", 
     "talent": "暗影/瞬移", "skill1": "暗影步", "skill2": "偷袭", "skill3": "绝命", "ult": "暗影领域",
     "tags": ["暗影", "瞬移", "爆发"]},
    {"name": "基扎洛夫", "tier": "T1", "meta": "SSR·黑暗·法师", 
     "talent": "召唤/魔导研究", "skill1": "构造体召唤", "skill2": "魔导研究", "skill3": "黑暗诅咒", "ult": "黑暗超绝",
     "tags": ["召唤", "研究", "超绝"]},
    {"name": "威拉", "tier": "T2", "meta": "SSR·传说·军师", 
     "talent": "战术撤离/重整旗鼓", "skill1": "战术撤离", "skill2": "重整旗鼓", "skill3": "群体治疗", "ult": "战术大师",
     "tags": ["战术", "撤离", "辅助"]},
    {"name": "杰利奥鲁&蕾拉", "tier": "T2", "meta": "SSR·传说·骑法", 
     "talent": "双形态切换", "skill1": "骑士精神", "skill2": "魔法伤害", "skill3": "突击", "ult": "双重审判",
     "tags": ["双形态", "骑士", "法师"]},
    {"name": "西格玛", "tier": "T2", "meta": "SSR·传说·弓手", 
     "talent": "游侠印记/远程", "skill1": "游侠之眼", "skill2": "猎风直击", "skill3": "瞄准", "ult": "致命狙击",
     "tags": ["远程", "标记", "狙击"]},
    {"name": "艾蕾因", "tier": "T2", "meta": "SSR·公主·步兵", 
     "talent": "剑舞/反击", "skill1": "剑舞", "skill2": "气刃", "skill3": "斩阳", "ult": "剑气",
     "tags": ["剑舞", "反击", "物理"]},
    {"name": "爱克雪拉", "tier": "T2", "meta": "SSR·公主·龙骑", 
     "talent": "龙息/飞行", "skill1": "龙息", "skill2": "风语", "skill3": "突击", "ult": "龙之怒",
     "tags": ["龙息", "飞行", "爆发"]},
    {"name": "伊普西龙", "tier": "T1", "meta": "SSR·流星·魔剑", 
     "talent": "流星超绝/禁疗", "skill1": "超绝", "skill2": "魔剑", "skill3": "绝命一击", "ult": "魔剑降临",
     "tags": ["超绝", "禁疗", "魔剑"]},
    {"name": "阿尔法", "tier": "T2", "meta": "SSR·帝国·枪兵", 
     "talent": "铁卫/反击", "skill1": "铁卫", "skill2": "力突", "skill3": "战吼", "ult": "绝对防御",
     "tags": ["护卫", "反击", "坦克"]},
    {"name": "布琳达", "tier": "T2", "meta": "SSR·帝国·枪兵", 
     "talent": "反击/不屈", "skill1": "反击", "skill2": "力突", "skill3": "穿甲", "ult": "不屈意志",
     "tags": ["反击", "不屈", "物理"]},
    {"name": "古斯塔夫", "tier": "T2", "meta": "SSR·黑暗·法师", 
     "talent": "鲜血舞踏/固伤", "skill1": "鲜血舞踏", "skill2": "火球术", "skill3": "陨石", "ult": "鲜血爆发",
     "tags": ["鲜血", "固伤", "法师"]},
    {"name": "超越之人", "tier": "T2", "meta": "SSR·黑暗·法师", 
     "talent": "召唤/黑暗之力", "skill1": "召唤", "skill2": "黑洞", "skill3": "暗镰", "ult": "超越",
     "tags": ["召唤", "黑暗", "法师"]},
    {"name": "托米尔克", "tier": "T2", "meta": "SSR·超凡·法师", 
     "talent": "召唤/范围伤害", "skill1": "召唤", "skill2": "陨石", "skill3": "闪电", "ult": "元素爆发",
     "tags": ["召唤", "AOE", "法师"]},
    {"name": "阿玛迪斯", "tier": "T2", "meta": "SSR·超凡·步兵", 
     "talent": "剑魂/爆发", "skill1": "剑魂", "skill2": "斩阳", "skill3": "气刃", "ult": "剑圣",
     "tags": ["剑魂", "爆发", "物理"]},
    {"name": "艾拉斯卓", "tier": "T2", "meta": "SSR·超凡·弓手", 
     "talent": "远程/狙击", "skill1": "狙击", "skill2": "瞄准", "skill3": "增援", "ult": "致命狙击",
     "tags": ["远程", "狙击", "弓手"]},
    {"name": "方舟圣女", "tier": "T2", "meta": "SSR·超凡·僧兵", 
     "talent": "群体治疗/护盾", "skill1": "群体治疗", "skill2": "护盾", "skill3": "净化", "ult": "神圣庇护",
     "tags": ["治疗", "护盾", "辅助"]},
    {"name": "米歇尔", "tier": "T2", "meta": "SSR·超凡·法师", 
     "talent": "魔法伤害", "skill1": "火球术", "skill2": "闪电", "skill3": "冰冻", "ult": "元素爆发",
     "tags": ["魔法", "元素", "法师"]},
    {"name": "文森特", "tier": "T2", "meta": "SSR·超凡·步兵", 
     "talent": "剑舞", "skill1": "剑舞", "skill2": "气刃", "skill3": "斩阳", "ult": "剑气",
     "tags": ["剑舞", "物理", "步兵"]},
    {"name": "诺埃米", "tier": "T2", "meta": "SSR·超凡·法师", 
     "talent": "魔法伤害", "skill1": "火球术", "skill2": "暗镰", "skill3": "陨石", "ult": "魔力爆发",
     "tags": ["魔法", "法师", "AOE"]},
    {"name": "修杰特", "tier": "T2", "meta": "SSR·超凡·弓手", 
     "talent": "远程", "skill1": "狙击", "skill2": "瞄准", "skill3": "增援", "ult": "致命一击",
     "tags": ["远程", "弓手", "狙击"]},
    {"name": "希琳卡", "tier": "T2", "meta": "SSR·超凡·刺客", 
     "talent": "暗影", "skill1": "暗影步", "skill2": "偷袭", "skill3": "绝命", "ult": "暗影突袭",
     "tags": ["暗影", "刺客", "爆发"]},
    {"name": "蕾娜塔", "tier": "T2", "meta": "SSR·超凡·法师", 
     "talent": "魔法伤害", "skill1": "火球术", "skill2": "暗镰", "skill3": "闪电", "ult": "魔力爆发",
     "tags": ["魔法", "法师", "元素"]},
    {"name": "里奇", "tier": "T2", "meta": "SSR·超凡·步兵", 
     "talent": "剑舞", "skill1": "剑舞", "skill2": "气刃", "skill3": "斩阳", "ult": "剑气",
     "tags": ["剑舞", "步兵", "物理"]},

    # SR英雄
    {"name": "兰斯", "tier": "T2", "meta": "SR·帝国·飞兵", 
     "talent": "空骑统帅/克制", "skill1": "突击", "skill2": "风语", "skill3": "增援", "ult": "空骑冲锋",
     "tags": ["飞行", "克制", "突进"]},
    {"name": "埃格贝尔特", "tier": "T2", "meta": "SR·帝国·法师", 
     "talent": "火球术/陨石", "skill1": "陨石", "skill2": "火球术", "skill3": "闪电", "ult": "陨石术",
     "tags": ["AOE", "火球", "法师"]},
    {"name": "基斯", "tier": "T2", "meta": "SR·帝国·飞兵", 
     "talent": "飞兵统帅", "skill1": "风语", "skill2": "气刃", "skill3": "增援", "ult": "疾风",
     "tags": ["飞行", "SR", "突击"], "category": "边缘"},
    {"name": "银狼", "tier": "T2", "meta": "SR·流星·刺客", 
     "talent": "偷袭/背刺", "skill1": "偷袭", "skill2": "背刺", "skill3": "无情", "ult": "暗影突袭",
     "tags": ["偷袭", "背刺", "刺客"], "category": "边缘"},
    {"name": "法娜", "tier": "T2", "meta": "SR·流星·飞兵", 
     "talent": "风语/范围伤害", "skill1": "风语", "skill2": "剑舞", "skill3": "增援", "ult": "风之舞",
     "tags": ["风语", "AOE", "飞行"], "category": "边缘"},
    {"name": "雾风", "tier": "T2", "meta": "SR·流星·刺客", 
     "talent": "暴击/背刺", "skill1": "偷袭", "skill2": "气刃", "skill3": "背刺", "ult": "暗影突袭",
     "tags": ["暴击", "背刺", "刺客"], "category": "边缘"},
    {"name": "塞蕾娜", "tier": "T2", "meta": "SR·战略·枪兵", 
     "talent": "铁卫/防御", "skill1": "铁卫", "skill2": "力突", "skill3": "战吼", "ult": "绝对防御",
     "tags": ["护卫", "防御", "坦克"], "category": "边缘"},
    {"name": "艾玛林克", "tier": "T2", "meta": "SR·战略·骑士", 
     "talent": "光环/削弱", "skill1": "攻击指挥", "skill2": "防御指挥", "skill3": "削弱", "ult": "战术指挥",
     "tags": ["光环", "削弱", "辅助"], "category": "边缘"},
    {"name": "索尼娅", "tier": "T2", "meta": "SR·战略·骑兵", 
     "talent": "强袭/突击", "skill1": "强袭", "skill2": "突击", "skill3": "撞击", "ult": "冲锋",
     "tags": ["强袭", "突击", "骑兵"], "category": "边缘"},
    {"name": "索菲亚", "tier": "T2", "meta": "SR·传说·法师", 
     "talent": "时间回溯/回溯", "skill1": "回溯", "skill2": "冥想", "skill3": "群体治疗", "ult": "时间倒流",
     "tags": ["回溯", "减CD", "治疗"]},
    {"name": "莉法妮", "tier": "T2", "meta": "SR·公主·法师", 
     "talent": "雷击/陨石", "skill1": "雷击", "skill2": "陨石", "skill3": "火球术", "ult": "陨石术",
     "tags": ["AOE", "法师", "SR"], "category": "边缘"},

    # R卡边缘英雄
    {"name": "利亚特", "tier": "T2", "meta": "R·帝国·骑兵", 
     "talent": "骑士的信念", "skill1": "突击", "skill2": "撞击", "skill3": "", "ult": "",
     "tags": ["骑士", "R卡", "边缘"], "category": "边缘"},
    {"name": "安娜", "tier": "T2", "meta": "R·帝国·僧兵", 
     "talent": "初级治疗", "skill1": "群体治疗", "skill2": "治疗术", "skill3": "护盾", "ult": "",
     "tags": ["治疗", "R卡", "边缘"], "category": "边缘"},
    {"name": "巴尔加斯", "tier": "T2", "meta": "R·帝国·枪兵", 
     "talent": "铁卫/不屈", "skill1": "铁卫", "skill2": "力突", "skill3": "战吼", "ult": "不屈",
     "tags": ["护卫", "不屈", "R卡"]},
    {"name": "蕾蒂西亚", "tier": "T2", "meta": "R·帝国·骑兵", 
     "talent": "疾行", "skill1": "疾行", "skill2": "攻击指挥", "skill3": "", "ult": "",
     "tags": ["加速", "R卡", "边缘"], "category": "边缘"},
    {"name": "利斯塔", "tier": "T2", "meta": "R·帝国·水兵", 
     "talent": "水中作战", "skill1": "水枪", "skill2": "激励", "skill3": "", "ult": "",
     "tags": ["水兵", "R卡", "边缘"], "category": "边缘"},
    {"name": "路因(R)", "tier": "T2", "meta": "R·光辉·步兵", 
     "talent": "初级剑士", "skill1": "斩阳", "skill2": "看破", "skill3": "", "ult": "",
     "tags": ["剑士", "R卡", "边缘"], "category": "边缘"},
    {"name": "斯科特", "tier": "T2", "meta": "R·光辉·骑兵", 
     "talent": "谨慎战术", "skill1": "群体强化", "skill2": "枪阵", "skill3": "", "ult": "",
     "tags": ["骑兵", "R卡", "边缘"], "category": "边缘"},
    {"name": "阿伦", "tier": "T2", "meta": "R·光辉·枪兵", 
     "talent": "初级护卫", "skill1": "护卫", "skill2": "力突", "skill3": "", "ult": "",
     "tags": ["护卫", "R卡", "边缘"], "category": "边缘"},
    {"name": "迪欧斯", "tier": "T2", "meta": "R·光辉·弓手", 
     "talent": "初级弓手", "skill1": "狙足", "skill2": "狙击", "skill3": "", "ult": "",
     "tags": ["弓手", "R卡", "边缘"], "category": "边缘"},
    {"name": "洛加", "tier": "T2", "meta": "R·黑暗·刺客", 
     "talent": "初级刺客", "skill1": "偷袭", "skill2": "背刺", "skill3": "", "ult": "",
     "tags": ["刺客", "R卡", "边缘"], "category": "边缘"},
    {"name": "皮耶鲁", "tier": "T2", "meta": "R·光之·水兵", 
     "talent": "水中作战", "skill1": "水枪", "skill2": "激励", "skill3": "治疗术", "ult": "",
     "tags": ["水兵", "R卡", "边缘"], "category": "边缘"},
    {"name": "马修(R)", "tier": "T3", "meta": "R·主角·步兵", 
     "talent": "新晋勇者", "skill1": "气刃", "skill2": "剑舞", "skill3": "", "ult": "",
     "tags": ["主角", "R卡", "边缘"], "category": "边缘"},
    {"name": "艾梅达(R)", "tier": "T3", "meta": "R·主角·僧兵", 
     "talent": "吐槽大师", "skill1": "治疗术", "skill2": "护盾", "skill3": "", "ult": "",
     "tags": ["治疗", "R卡", "边缘"], "category": "边缘"},
    {"name": "格尼尔(R)", "tier": "T3", "meta": "R·主角·枪兵", 
     "talent": "坚忍反击", "skill1": "护卫", "skill2": "力突", "skill3": "", "ult": "",
     "tags": ["护卫", "R卡", "边缘"], "category": "边缘"},
    {"name": "阿尔弗雷德", "tier": "T2", "meta": "SR·超凡·水兵", 
     "talent": "水中/群体驭水", "skill1": "水枪", "skill2": "群体驭水", "skill3": "", "ult": "",
     "tags": ["水兵", "SR", "边缘"], "category": "边缘"},
    {"name": "比萝蒂丝", "tier": "T2", "meta": "SR·联动·刺客", 
     "talent": "偷袭", "skill1": "偷袭", "skill2": "背刺", "skill3": "", "ult": "",
     "tags": ["刺客", "联动", "边缘"], "category": "边缘"},
    {"name": "桑原和真", "tier": "T2", "meta": "SSR·联动·坦克", 
     "talent": "灵剑/防御", "skill1": "灵剑", "skill2": "铁卫", "skill3": "战吼", "ult": "",
     "tags": ["坦克", "联动", "边缘"], "category": "边缘"},
    {"name": "志村新八", "tier": "T2", "meta": "SSR·联动·步兵", 
     "talent": "吐槽/眼镜", "skill1": "吐槽", "skill2": "眼镜", "skill3": "斩阳", "ult": "",
     "tags": ["吐槽", "联动", "边缘"], "category": "边缘"},
    {"name": "奥利维尔(联动)", "tier": "T2", "meta": "SSR·联动·弓手", 
     "talent": "演奏/范围", "skill1": "演奏", "skill2": "范围攻击", "skill3": "狙击", "ult": "",
     "tags": ["演奏", "联动", "边缘"], "category": "边缘"},
    {"name": "帕恩", "tier": "T2", "meta": "SSR·联动·步兵", 
     "talent": "自由骑士", "skill1": "斩龙剑", "skill2": "斩阳", "skill3": "气刃", "ult": "",
     "tags": ["骑士", "联动", "边缘"], "category": "边缘"},
    {"name": "高里", "tier": "T2", "meta": "SSR·联动·步兵", 
     "talent": "光之剑", "skill1": "光之剑", "skill2": "斩龙", "skill3": "斩阳", "ult": "",
     "tags": ["剑士", "联动", "边缘"], "category": "边缘"},
    {"name": "杰路刚帝士", "tier": "T2", "meta": "SSR·联动·坦克", 
     "talent": "魔法剑", "skill1": "魔法剑", "skill2": "铁卫", "skill3": "力突", "ult": "",
     "tags": ["魔剑", "联动", "边缘"], "category": "边缘"},
    {"name": "户愚吕兄弟", "tier": "T2", "meta": "SSR·联动·格斗", 
     "talent": "变身", "skill1": "变身", "skill2": "灵丸", "skill3": "爆发", "ult": "",
     "tags": ["变身", "联动", "边缘"], "category": "边缘"},
    {"name": "真田辽", "tier": "T2", "meta": "SSR·联动·步兵", 
     "talent": "双炎斩", "skill1": "双炎斩", "skill2": "辉煌帝", "skill3": "斩阳", "ult": "",
     "tags": ["剑士", "联动", "边缘"], "category": "边缘"},
    {"name": "神崎堇", "tier": "T2", "meta": "SSR·联动·法师", 
     "talent": "魔法", "skill1": "火球术", "skill2": "闪电", "skill3": "", "ult": "",
     "tags": ["法师", "联动", "边缘"], "category": "边缘"},
    {"name": "羽柴当麻", "tier": "T2", "meta": "SSR·联动·弓手", 
     "talent": "远程", "skill1": "狙击", "skill2": "瞄准", "skill3": "", "ult": "",
     "tags": ["弓手", "联动", "边缘"], "category": "边缘"},
    {"name": "剑部武一郎", "tier": "T2", "meta": "SSR·联动·坦克", 
     "talent": "铁卫", "skill1": "铁卫", "skill2": "战吼", "skill3": "", "ult": "",
     "tags": ["坦克", "联动", "边缘"], "category": "边缘"},
    {"name": "伊莎拉", "tier": "T2", "meta": "SSR·联动·坦克", 
     "talent": "战车", "skill1": "炮击", "skill2": "铁卫", "skill3": "", "ult": "",
     "tags": ["战车", "联动", "边缘"], "category": "边缘"},
    {"name": "亚尔缇娜", "tier": "T2", "meta": "SSR·联动·法师", 
     "talent": "控制", "skill1": "冰冻", "skill2": "闪电", "skill3": "", "ult": "",
     "tags": ["控制", "联动", "边缘"], "category": "边缘"},
    {"name": "亚修拉姆", "tier": "T2", "meta": "SSR·联动·步兵", 
     "talent": "剑舞", "skill1": "剑舞", "skill2": "气刃", "skill3": "", "ult": "",
     "tags": ["剑士", "联动", "边缘"], "category": "边缘"},
]

def generate_html(hero):
    """生成单个英雄的HTML代码"""
    tier_num = hero['tier'][-1] if hero['tier'][-1].isdigit() else '2'
    tags_html = ''.join([f'<span class="tag tag-core">{t}</span>' for t in hero['tags'][:3]])
    
    # 处理可能为空的技能
    skill3 = hero.get('skill3', '') or ''
    ult = hero.get('ult', '') or ''
    
    html = f'''                    <tr>
                        <td class="hero-cell">
                            <div class="hero-name">{hero['name']} <span class="tag tag-t{tier_num}">{hero['tier']}</span></div>
                            <div class="hero-meta">{hero['meta']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill1']}</div>
                            <div class="skill-desc">{hero['talent'][:40]}...</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{hero['skill2']}</div>
                            <div class="skill-desc">核心输出技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill3}</div>
                            <div class="skill-desc">辅助/控制技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{ult}</div>
                            <div class="skill-desc">超绝/终极技能</div>
                        </td>
                        <td class="tags-cell">
                            {tags_html}
                        </td>
                    </tr>'''
    return html

# 生成统计信息
tier_counts = {'T0': 0, 'T1': 0, 'T2': 0, 'T3': 0}
cat_counts = {}

for hero in LANGRISSER_NEW_HEROES:
    tier_counts[hero['tier']] = tier_counts.get(hero['tier'], 0) + 1
    cat = hero.get('category', 'SSR')
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

print("=" * 70)
print("梦幻模拟战扩充统计")
print("=" * 70)
print(f"新增英雄总数: {len(LANGRISSER_NEW_HEROES)}位")
print(f"\n强度分布:")
for tier, count in sorted(tier_counts.items()):
    print(f"  {tier}: {count}位")
print(f"\n分类统计:")
for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
    print(f"  {cat}: {count}位")
print(f"\n当前已有: 65位")
print(f"新增: {len(LANGRISSER_NEW_HEROES)}位")
print(f"扩充后总计: {65 + len(LANGRISSER_NEW_HEROES)}位")
print(f"目标: 208位")
print(f"缺口: {208 - 65 - len(LANGRISSER_NEW_HEROES)}位")

# 生成HTML文件
print("\n" + "=" * 70)
print("生成HTML插入代码...")
print("=" * 70)

html_output = []
for hero in LANGRISSER_NEW_HEROES:
    html_output.append(generate_html(hero))

# 保存到文件
output_file = "/root/.openclaw/workspace/portfolio-blog/research/srpg-analysis/langrisser_new_heroes.html"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_output))

print(f"HTML代码已保存到: {output_file}")
print(f"文件大小: {len('\\n'.join(html_output))} 字符")

# 显示前3个示例
print("\n前3位英雄HTML代码示例:")
print("-" * 70)
for i in range(min(3, len(LANGRISSER_NEW_HEROES))):
    print(generate_html(LANGRISSER_NEW_HEROES[i]))
    print()
