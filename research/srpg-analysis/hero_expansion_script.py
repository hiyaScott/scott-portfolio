#!/usr/bin/env python3
"""
SRPG英雄数据扩充脚本
任务：
1. 天地劫扩充（139位→150+位）
2. 梦幻模拟战扩充（65位→208位）
"""

import re
from collections import defaultdict

# ==================== 天地劫数据源（从tdj-hero-database.html提取）====================
TDJ_HEROES_DATA = """
T0核心:
真胤(和尚)|绝·光·铁卫|召唤、结界、铠甲|金刚不坏、双结界、五大明王
双魂虞兮|典藏·光/暗·斗将|双形态、典藏|双魂切换、辉日圣咒、玄晔破封
李白|绝·光·御风|国风、再动|诗仙、御剑飞行、剑气纵横
幽律|绝·幽·咒师|debuff、刷新|幽冥之力、幽魂索命、幽冥审判

T1强力:
杨戬|绝·光·铁卫|神兵、护卫|三尖两刃刀、哮天犬、神威
星占贤者|绝·光·咒师|占星、辅助|星象占卜、命运之轮、星辰坠落
武英仲|绝·光·侠客|光系、输出|剑圣之道、天剑、剑气
阴歙|绝·冰·铁卫|护卫、控制|寒意覆身、冰封、霜甲
韩千秀|绝·炎·羽士|固伤、AOE|烈焰连环、双环映月、烈焰风暴
朱缳|绝·炎·羽士|飞行、辅助|风之翼、火羽、凤凰涅槃
上官远|绝·炎·铁卫|冲锋、护卫|列阵、刚烈破、嘲讽
召祐|绝·暗·铁卫|召唤、护卫|龙鳞护体、龙吟、龙威
铁手夏侯仪|绝·炎·咒师|燃烧、AOE|血魂之咒、离火神诀、九俱焚灭
神阙青衣|绝·冰·侠客|冰系、输出|玄冰剑气、冰封、剑舞
夜无陵|绝·暗·斗将|2025新英灵|暗影之力、夜袭、黑暗笼罩
紫炁|绝·雷·咒师|2025新英灵|紫电、雷霆万钧、天罚
上元夫人|绝·冰·咒师|国风、2025|玄冰、仙术、冰封

T2可用:
皇甫申(原版)|绝·雷·侠客|混合伤害|五雷轰顶、天雷降世
韩无砂|绝·暗·咒师|蛇毒、美女|蛇毒、毒雾、魅惑
赤妭韩无砂|典藏·炎·咒师|典藏、3C|赤炎蛇毒、焚身、化蛇
阳寰|绝·炎·咒师|灼烧、固伤|燃血、离火、焚天
暗曜阳寰|典藏·暗·破军|典藏、重生|暗焰、重生、破军
宇韶容|绝·光·铁卫|护卫、法坦|光明庇护、驱散、反弹
高戚|绝·暗·铁卫|反击、坦克|暗鳞、破阵、龙焰
幻镜胧妖|极·冰·咒师|幻镜、控制|幻镜、冰封、幻影
太渊隐逸|极·冰·祝由|驱散、治疗|寒霜护体、冰霜治愈、冰封

边缘/T3:
司徒樱|极·炎·祝由|治疗、SR升绝|火焰治疗、驱散
白菀|极·光·祝由|治疗、SR升绝|光之治愈、驱散
紫蕴|极·雷·铁卫|护卫、SR升绝|雷甲、护卫
周崇|极·暗·侠客|暴击、SR升绝|暗影剑、暴击
伊丝朶|极·雷·祝由|治疗、R升绝|雷电治愈、驱散
应灵华|极·冰·侠客|先攻、R升绝|先攻、冰剑
常逸风|极·暗·御风|机动、R升绝|暗影步、疾风
相桓子|极·光·咒师|传送、SR升绝|传送术、光箭
呼延崇|极·雷·羽士|辅助、R升绝|雷电箭、辅助
朱浩|极·暗·咒师|召唤、R升绝|召唤僵尸、暗箭
高世津|极·暗·侠客|减益|暗影刃、诅咒
阿尔泰巴|极·雷·铁卫|坦克、R升绝|雷甲、重击
青萝|极·冰·御风|再动、R升绝|冰刃、再动
"""

# ==================== 梦幻模拟战数据源（从langrisser-hero-database.html提取）====================
LANGRISSER_HEROES_DATA = """
# LLR英雄（4位）
LLR:
辉耀圣召使|LLR·光辉·僧兵|T0|治疗/召唤|光之超绝、WiFi奶、光马召唤|光明颂歌、辉耀救赎、契约召唤
炎龙破灭者|LLR·帝国·龙骑|T0|爆发/龙骑|帝国超绝、狂怒、龙息|燃魂血怒、龙息、战吼
冰渊凌御者|LLR·帝国·法师|T0|控制/法师|链鞭、彻骨寒意、位移|冰渊宰制、极冰锁链、天罚
幽瞳幻惑使|LLR·黑暗·法师|T0|控制/幻惑|黑暗超绝、幻惑、位移|幽瞳凝视、幻惑之瞳、黑洞

# SP英雄（19位）
SP:
SP艾尔文|SP·光辉·步兵|T0|超绝手/剑士|光辉超绝、再动|永恒的光辉、剑魂、大喝
SP雪莉|SP·公主·飞兵|T0|再动输出|击杀再动、落跑公主|雷光、迅雷、影袭
SP雷丁|SP·光辉·枪兵|T0|坦克/超绝|光辉超绝、神卫|正义的裁决、神卫、烈阳
SP娜姆|SP·光辉·弓手|T1|克制飞兵|瞄准、克制飞兵|神射、狙足、增援
SP海恩|SP·光辉·法师|T1|传送/三系|传送、三系克制|陨石、传送、火球术
SP格尼尔|SP·主角·枪兵|T1|坦克/超绝|主角超绝、反击|全村的希望、枪阵、力突
SP马修|SP·主角·步兵|T1|多职业|主角超绝、破碎之刃|破碎之刃、气刃、剑舞
SP艾梅达|SP·主角·僧兵|T1|治疗/吐槽|吐槽、群体治疗|吐槽大会、群体治疗、驱散
SP迪哈尔特|SP·光之·刺客|T1|刺客/超绝|起源超绝、闪避|瞬身、无情、偷袭
SP巴恩哈特|SP·帝国·步兵|T0|皇帝/超绝|帝国超绝、霸气|铁血的野望、剑舞、盾击
SP利昂|SP·帝国·骑兵|T0|骑士/突击|骑士精神、攻击后移动|骑士精神、突击、青龙破阵
SP亚鲁特缪拉|SP·战略·飞兵|T1|超绝/再动|战略超绝、再行动|无双鏖战、龙息、范围伤害
SP芙蕾雅|SP·光之·枪兵|T1|坦克/超绝|光之超绝、固伤反击|蔷薇之怒放、晶刺、固伤反击
SP兰迪乌斯|SP·传说·骑兵|T0|坦克/超绝|传说超绝、止水|璀璨的传说、止水、明镜止水
SP兰芳特|SP·战略·骑兵|T1|光环辅助|领战迅击、混合部队加成|领战迅击、光环辅助
SP蒂亚莉丝|SP·传说·僧兵|T0|治疗/辅助|进击的加护、战后回血|进击的加护、神迹、群体治疗
SP西格玛|SP·传说·弓手|T1|远程输出|游侠印记、远程|游侠之眼、猎风直击
SP拉娜|SP·黑暗·法师|T0|AOE法师|黑洞、天罚、元素回响|黑洞、天罚、暗镰、净化
SP泽瑞达|SP·流星·刺客|T0|刺客/再动|拔刀、无视护卫|魔剑之心、绝命一击、影袭

# SSR核心英雄（补充）
SSR:
雪露法妮尔|SSR·光辉·法师|T1|传送/辅助|传送、群体增益|天罚、干涸、群体魔抗
艾希恩|SSR·光辉·步兵|T0|剑士/输出|再动、王者之志|王者之志、剑魂、迎头痛击
赛利卡|SSR·光辉·僧兵|T0|辅助/法师|炼金术、增益转化|炼成术、群体治疗、强化
薇莉娅|SSR·光辉·法师|T0|AOE法师|魔法伤害、范围打击|天罚、黑洞、火球术
尤弥尔|SSR·光辉·步兵|T1|物理输出|高爆发、单体打击|强力一击、破甲、迎头痛击
基扎洛夫|SSR·帝国·法师|T1|召唤/法师|召唤、魔导研究|构造体召唤、魔导研究
海伦娜|SSR·帝国·骑兵|T2|璨晶骑士|璨晶绽放、武器失效|璨晶绽放、璨晶地形
克洛泰尔|SSR·帝国·法师|T1|炎系法师|炎晶术、灼烧|炎晶术、火球术、陨石
奥托克拉托|SSR·帝国·步兵|T1|剑士/皇权|皇权、压制|皇权、剑魂、压制
艾米莉亚|SSR·帝国·枪兵|T1|魔防坦克|圣卫、魔法反击|圣卫、神威、奉献
贝蒂|SSR·帝国·枪兵|T2|反伤坦克|反伤、威慑|重盾、战吼、铁卫
克里斯蒂安妮|SSR·公主·枪兵|T1|花T/输出|公主超绝、花T|花之锁、护卫、反击
罗莎莉娅|SSR·公主·骑兵|T1|骑士输出|骑士精神、突进|骑士精神、突击、裁决
蕾伽尔|SSR·公主·法师|T1|魔力震荡|魔力震荡、增益|魔力震荡、群体魔抗、净化
伊露希亚|SSR·公主·水兵|T1|海卫坦克|海卫、水战|海卫、海洋之力、护卫
克拉蕾特|SSR·公主·飞兵|T1|位移/再动|位移、再动|疾风、突袭、再移动
辉夜|SSR·公主·刺客|T2|暗影输出|暗影、暴击|暗影步、偷袭、绝命
怀特·茜茜|SSR·公主·僧兵|T1|治疗辅助|群体治疗、增益|群体治疗、护盾、净化
克里斯蒂安妮|SSR·公主·枪兵|T1|花T|公主超绝、花之锁|花之锁、护卫、反击
胧|SSR·流星·斗神|T0|龙威/再动|龙威、再动|龙威一怒、龙形变身
飞影|SSR·流星·刺客|T0|刺客/爆发|邪王炎杀、无视护卫|炎杀黑龙波、邪王炎杀剑
光影剑魄|SSR·流星·步兵|T1|光暗双生|光暗双生、再动|光暗剑、剑舞、再动
欧米伽|SSR·流星·刺客|T1|奇袭/弓手|奇袭、无视护卫|奇袭、弱点狙击、孤影疾袭
燕|SSR·流星·刺客|T1|忍者/隐匿|隐匿、瞬闪|迅隐杀机、影窃、瞬闪
浦饭幽助|SSR·流星·格斗|T1|变身/爆发|变身、爆发|灵丸、黑龙波、魔人化
塔布莉丝|SSR·流星·刺客|T1|暗影/瞬移|暗影、瞬移|暗影步、偷袭、绝命
迦游罗|SSR·流星·法师|T1|邪光AOE|邪光、范围伤害|邪光、黑洞、天罚
伊普西龙|SSR·流星·魔剑|T1|流星超绝|流星超绝、禁疗|超绝、魔剑、绝命一击
格伦希尔|SSR·战略·飞兵|T1|风语输出|风语、范围伤害|风语、剑舞、疾风
弗洛朗蒂娅|SSR·战略·法师|T1|宰相/再动|战术指挥、再动|战术指挥、重整旗鼓、群体治疗
伊索尔德|SSR·超凡·龙骑|T0|龙妈/超绝|超凡超绝、龙形态|龙形态、龙息、超绝
醒觉者|SSR·超凡·法师|T0|时空操控|时空操控、再动|时空操控、黑洞、天罚
萨格尼|SSR·超凡·法师|T1|魔力震荡|魔力震荡、单体爆发|魔力震荡、暗镰、火球术
杰斯|SSR·超凡·步兵|T1|剑士输出|剑舞、反击|剑舞、气刃、斩阳
亚德凯摩|SSR·超凡·法师|T1|控制/削弱|控制、削弱|冰冻、闪电、火球术
兰芳特|SSR·战略·骑兵|T1|光环辅助|领战迅击、混合加成|领战迅击、光环辅助
安洁丽娜|SSR·传说·水兵|T1|位移辅助|位移、群体增益|剑舞、疾风、群体魔抗
罗泽希尔|SSR·传说·僧兵|T0|水晶治疗|水晶屏障、群体治疗|水晶屏障、群体治疗、驱散
卢克蕾蒂娅|SSR·黑暗·刺客|T0|傀儡/输出|混沌寄宿、无视护卫|噬魂魔剑、暗影步、黑暗超绝
阿雷斯|SSR·帝国·骑兵|T1|突进输出|范围伤害、突进|龙傲天、裁决之刃
妮丝蒂尔|SSR·黑暗·法师|T1|固伤/血舞|鲜血舞踏、治疗反转|鲜血舞踏、死神之触、怒血之潮
丽可丽丝|SSR·黑暗·僧兵|T1|治疗/召唤|黑暗超绝、召唤|魔神降临、召唤魔族、群体治疗
维坦|SSR·黑暗·刺客|T0|暗影/再动|暗影、再动|暗影步、影袭、暗影之力
邪神库鲁加|SSR·黑暗·法师|T1|邪神之力|邪神之力、范围伤害|邪神降临、黑洞、天罚
玛丽安蒂尔|SSR·黑暗·僧兵|T1|鲜血治疗|鲜血治疗、转化|鲜血治疗、群体治疗、净化
席尔娜|SSR·黑暗·刺客|T1|暗影控制|暗影步、控制|暗影步、偷袭、绝命

# SR英雄（部分代表性）
SR:
兰斯|SR·帝国·飞兵|T2|空骑统帅|空骑统帅、克制|突击、风语、增援
埃格贝尔特|SR·帝国·法师|T2|AOE法师|火球术、陨石|陨石、火球术、闪电
伊梅尔达|SR·帝国·僧兵|T2|女王鞭挞|女王鞭挞、群体治疗|女王鞭挞、治疗术、冰冻
巴尔加斯|SR·帝国·枪兵|T2|不屈坦克|铁卫、不屈|铁卫、力突、战吼
娜姆|SR·光辉·弓手|T2|克制飞兵|瞄准、克制飞兵|神射、狙足、增援
克里斯|SR·光辉·步兵|T2|魔物克星|魔物克星、回血|信仰、审判、奉献
芙蕾雅|SR·公主·枪兵|T2|固伤坦克|光之超绝、固伤反击|蔷薇之怒放、晶刺、固伤反击
银狼|SR·流星·刺客|边缘|偷袭背刺|偷袭、背刺、无情
法娜|SR·流星·飞兵|边缘|风语AOE|风语、剑舞、增援
雾风|SR·流星·刺客|边缘|暴击背刺|偷袭、气刃、背刺
塞蕾娜|SR·战略·枪兵|边缘|铁卫坦克|铁卫、力突、战吼
艾玛林克|SR·战略·骑士|边缘|光环削弱|攻击指挥、防御指挥、削弱
索尼娅|SR·战略·骑兵|边缘|强袭突击|强袭、突击、撞击

# R卡边缘英雄
R:
利亚特|R·帝国·骑兵|边缘|骑士信念|突击、撞击
安娜|R·帝国·僧兵|边缘|初级治疗|群体治疗、治疗术、护盾
蕾蒂西亚|R·帝国·骑兵|边缘|疾行加速|疾行、攻击指挥
利斯塔|R·帝国·水兵|边缘|水中作战|水枪、激励
路因|R·光辉·步兵|边缘|初级剑士|斩阳、看破
斯科特|R·光辉·骑兵|边缘|谨慎战术|群体强化、枪阵
阿伦|R·光辉·枪兵|边缘|初级护卫|护卫、力突
迪欧斯|R·光辉·弓手|边缘|初级弓手|狙足、狙击
洛加|R·黑暗·刺客|边缘|初级刺客|偷袭、背刺
皮耶鲁|R·光之·水兵|边缘|水中作战|水枪、激励、治疗术
"""

def parse_tdj_heroes():
    """解析天地劫英雄数据"""
    heroes = []
    current_tier = None
    
    for line in TDJ_HEROES_DATA.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.endswith(':'):
            current_tier = line[:-1]
            continue
        
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 4:
                name = parts[0].strip()
                meta = parts[1].strip()
                mechanisms = parts[2].strip()
                skills = parts[3].strip() if len(parts) > 3 else ""
                
                # 确定tier
                tier = "T2"
                if "T0" in current_tier or "核心" in current_tier:
                    tier = "T0"
                elif "T1" in current_tier or "强力" in current_tier:
                    tier = "T1"
                elif "边缘" in current_tier or "T3" in current_tier:
                    tier = "T2"  # 边缘角色在总览中标记为T2
                
                heroes.append({
                    'name': name,
                    'meta': meta,
                    'tier': tier,
                    'mechanisms': mechanisms,
                    'skills': skills
                })
    
    return heroes

def parse_langrisser_heroes():
    """解析梦幻模拟战英雄数据"""
    heroes = []
    current_category = None
    
    for line in LANGRISSER_HEROES_DATA.strip().split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if line.endswith(':'):
            current_category = line[:-1]
            continue
        
        if '|' in line:
            parts = line.split('|')
            if len(parts) >= 6:
                name = parts[0].strip()
                meta = parts[1].strip()
                tier_tag = parts[2].strip()
                role = parts[3].strip()
                mechanisms = parts[4].strip()
                skills = parts[5].strip()
                
                heroes.append({
                    'name': name,
                    'meta': meta,
                    'tier': tier_tag,
                    'role': role,
                    'mechanisms': mechanisms,
                    'skills': skills,
                    'category': current_category
                })
    
    return heroes

def generate_tdj_html(heroes):
    """生成天地劫HTML代码"""
    html_lines = []
    
    for hero in heroes:
        tier_class = f"tag-t{hero['tier'][-1]}" if hero['tier'][-1].isdigit() else "tag-t2"
        
        # 解析技能
        skills = hero['skills'].split('、') if hero['skills'] else ['', '', '']
        skill1 = skills[0] if len(skills) > 0 else ''
        skill2 = skills[1] if len(skills) > 1 else ''
        skill3 = skills[2] if len(skills) > 2 else ''
        
        # 解析机制标签
        mechs = hero['mechanisms'].split('、') if hero['mechanisms'] else []
        tags_html = ''.join([f'<span class="tag tag-core">{m}</span>' for m in mechs[:3]])
        
        html = f'''                    <tr>
                        <td class="hero-cell">
                            <div class="hero-name">{hero['name']} <span class="tag {tier_class}">{hero['tier']}</span></div>
                            <div class="hero-meta">{hero['meta']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill1}</div>
                            <div class="skill-desc">{hero['mechanisms'][:30]}...</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill2}</div>
                            <div class="skill-desc">核心技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill3}</div>
                            <div class="skill-desc">辅助技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">绝学</div>
                            <div class="skill-desc">强力终结技</div>
                        </td>
                        <td class="tags-cell">
                            {tags_html}
                        </td>
                    </tr>'''
        html_lines.append(html)
    
    return '\n'.join(html_lines)

def generate_langrisser_html(heroes):
    """生成梦幻模拟战HTML代码"""
    html_lines = []
    
    for hero in heroes:
        tier_class = f"tag-t{hero['tier'][-1]}" if hero['tier'][-1].isdigit() else "tag-t2"
        
        # 解析技能
        skills = hero['skills'].split('、') if hero['skills'] else ['', '', '', '']
        skill1 = skills[0] if len(skills) > 0 else ''
        skill2 = skills[1] if len(skills) > 1 else ''
        skill3 = skills[2] if len(skills) > 2 else ''
        skill4 = skills[3] if len(skills) > 3 else ''
        
        # 解析机制标签
        mechs = hero['mechanisms'].split('、') if hero['mechanisms'] else []
        tags_html = ''.join([f'<span class="tag tag-core">{m}</span>' for m in mechs[:3]])
        
        html = f'''                    <tr>
                        <td class="hero-cell">
                            <div class="hero-name">{hero['name']} <span class="tag {tier_class}">{hero['tier']}</span></div>
                            <div class="hero-meta">{hero['meta']}</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill1}</div>
                            <div class="skill-desc">{hero['mechanisms'][:30]}...</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill2}</div>
                            <div class="skill-desc">核心技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill3}</div>
                            <div class="skill-desc">辅助技能</div>
                        </td>
                        <td class="skill-cell">
                            <div class="skill-name">{skill4}</div>
                            <div class="skill-desc">超绝/大招</div>
                        </td>
                        <td class="tags-cell">
                            {tags_html}
                        </td>
                    </tr>'''
        html_lines.append(html)
    
    return '\n'.join(html_lines)

# 统计信息
tdj_heroes = parse_tdj_heroes()
langrisser_heroes = parse_langrisser_heroes()

print("=" * 60)
print("天地劫英雄数据统计")
print("=" * 60)
print(f"新增英雄数量: {len(tdj_heroes)}")
tier_counts = defaultdict(int)
for h in tdj_heroes:
    tier_counts[h['tier']] += 1
print(f"T0: {tier_counts['T0']}位")
print(f"T1: {tier_counts['T1']}位")  
print(f"T2: {tier_counts['T2']}位")
print(f"总计新增: {len(tdj_heroes)}位")
print(f"扩充后总计: {139 + len(tdj_heroes)}位")

print("\n" + "=" * 60)
print("梦幻模拟战英雄数据统计")
print("=" * 60)
print(f"新增英雄数量: {len(langrisser_heroes)}")
tier_counts = defaultdict(int)
cat_counts = defaultdict(int)
for h in langrisser_heroes:
    tier_counts[h['tier']] += 1
    cat_counts[h['category']] += 1
print(f"T0: {tier_counts.get('T0', 0)}位")
print(f"T1: {tier_counts.get('T1', 0)}位")
print(f"T2: {tier_counts.get('T2', 0)}位")
print(f"边缘: {tier_counts.get('边缘', 0)}位")
print(f"\n分类统计:")
for cat, count in cat_counts.items():
    print(f"  {cat}: {count}位")
print(f"\n新增总计: {len(langrisser_heroes)}位")
print(f"扩充后总计: {65 + len(langrisser_heroes)}位")

# 输出生成的HTML片段（前3个作为示例）
print("\n" + "=" * 60)
print("天地劫HTML代码示例（前3位）")
print("=" * 60)
print(generate_tdj_html(tdj_heroes[:3]))

print("\n" + "=" * 60)
print("梦幻模拟战HTML代码示例（前3位）")
print("=" * 60)
print(generate_langrisser_html(langrisser_heroes[:3]))
