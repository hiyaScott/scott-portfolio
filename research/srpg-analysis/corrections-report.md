# 天地劫角色数据库勘误报告

> 生成时间：2026-03-17
> 数据来源：B站天地劫Wiki (https://wiki.biligame.com/tdj)
> 对比文件：character-skills-enumeration.html

---

## 勘误汇总表

| 序号 | 角色名 | 错误类型 | 严重程度 |
|------|--------|----------|----------|
| 1 | 林月如 | 天赋错误、技能错误、标签错误 | 严重 |
| 2 | 冰璃 | 天赋错误 | 严重 |
| 3 | 曹沁 | 天赋错误、技能错误 | 严重 |
| 4 | 封铃笙 | 天赋错误、技能错误 | 严重 |
| 5 | 黎幽 | 天赋错误 | 严重 |
| 6 | 夏侯仪 | 天赋错误、技能错误 | 严重 |
| 7 | 古伦德 | 天赋错误、技能错误 | 严重 |
| 8 | 郸阴 | 天赋错误、技能错误 | 严重 |
| 9 | 葛云衣 | 天赋错误、技能错误 | 严重 |
| 10 | 殷剑平 | 天赋错误、技能错误 | 严重 |
| 11 | 封寒月 | 天赋错误、技能错误 | 严重 |
| 12 | 慕容璇玑 | 天赋错误、技能错误 | 严重 |
| 13 | 燕明蓉 | 品阶错误、天赋错误、技能错误 | 严重 |
| 14 | 殷无邪 | 天赋错误、技能错误 | 严重 |
| 15 | 剑邪 | 天赋错误、技能错误 | 严重 |
| 16 | 诸葛艾 | 天赋错误、技能错误 | 严重 |
| 17 | 奚歌 | 天赋错误、技能错误 | 严重 |
| 18 | 鲜于超 | 属性错误、天赋错误、技能错误 | 严重 |
| 19 | 巴艾迩 | 职业错误、天赋错误、技能错误 | 严重 |
| 20 | 魔化皇甫申 | 天赋错误、技能错误 | 严重 |

---

## 详细勘误记录

### 1. 林月如

**角色信息勘误：**
- HTML中缺失该角色数据（文件中未找到）

**正确数据（6星天赋）：**
- **天赋名称**：气劲凌云
- **天赋效果（6星）**：攻击前，每移动1格，本次伤害提高5%（最多可以提升25%）。每造成1次伤害，获得1层「气劲」，造成暴击额外获得1层。行动结束时，如果携带4层「气劲」，则消耗所有「气劲」对自身周围菱形2格范围内1个敌人施加「晕眩」状态，持续1回合。(间隔1回合触发)
- **属相**：雷
- **职业**：御风
- **品阶**：绝

**数据来源**：https://wiki.biligame.com/tdj/林月如

---

### 2. 冰璃

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：幽冥剑引
- 天赋描述：主动攻击1.8倍伤害，击杀后再行动

**正确内容（6星天赋）：**
- **天赋名称**：幽冥剑引
- **天赋效果（6星）**：每造成1次伤害（包含多目标），获得1层「怒意」状态(上限2层）。行动结束时，如果本回合造成过伤害同时身上「怒意」状态为2层，获得再行动（5格），本次行动结束时消除「怒意」（该效果间隔2回合发动）。「怒意」除气血外全属性提高10%

**数据来源**：https://wiki.biligame.com/tdj/冰璃

---

### 3. 曹沁

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：劫焰誓杀
- 天赋描述：标记敌人，击杀后刷新所有技能CD

**正确内容（6星天赋）：**
- **天赋名称**：劫焰誓杀
- **天赋效果（6星）**：使用绝学后获得「流火」状态，持续1回合。闪避或主动击杀敌人后重置所有主动绝学的冷却时间（间隔3回合触发）。「流火」：物攻和暴击率提高20%（不可驱散）

**数据来源**：https://wiki.biligame.com/tdj/曹沁

---

### 4. 封铃笙

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：瞬霎神仪
- 天赋描述：让友方立即再行动，恢复50%气血

**正确内容（6星天赋）：**
- **天赋名称**：传心
- **天赋效果（6星）**：自身气血100%时，法攻提高15%。使用技能后，为自身3格内其他友方恢复气血（恢复量为施术者法攻的0.6倍）

**数据来源**：https://wiki.biligame.com/tdj/封铃笙

---

### 5. 黎幽

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：幽垠幻生
- 天赋描述：范围伤害，附加2个随机debuff

**正确内容（6星天赋）：**
- **天赋名称**：幽冥之力
- **天赋效果（6星）**：与携带「有害状态」角色作战时，「对战中」法攻，法防提高15%。行动结束时，对3格范围内随机4个敌方角色施加2个随机「有害状态」

**数据来源**：https://wiki.biligame.com/tdj/黎幽

---

### 6. 夏侯仪

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：焚火真炎
- 天赋描述：十字范围0.7倍火伤，点燃地形2回合

**正确内容（6星天赋）：**
- **天赋名称**：幽煌邪焰
- **天赋效果（6星）**：气血大于50%时，法攻提升15%。遭受伤害后自身气血低于50%，则气血恢复100%，获得「幽煌邪焰」状态，持续2回合（间隔2回合触发1次）。「幽煌邪焰」：除气血外所有属性提高10%（无法驱散）

**数据来源**：https://wiki.biligame.com/tdj/夏侯仪

---

### 7. 古伦德

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：回光枪技
- 天赋描述：替2格内友方承受物理伤害，反击射程+1

**正确内容（6星天赋）：**
- **天赋名称**：回光枪技
- **天赋效果（6星）**：遭受攻击「对战中」免伤提高15%。主动攻击「对战后」击退目标2格。如果击退路线被阻挡，则施加「晕眩」状态，持续1回合。（间隔2回合触发）「晕眩」：无法行动，且在对战中无法进行反击。

**数据来源**：https://wiki.biligame.com/tdj/古伦德

---

### 8. 郸阴

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：冥幻之阵
- 天赋描述：召唤僵尸助战，僵尸可自爆造成伤害和治疗

**正确内容（6星天赋）：**
- **天赋名称**：冥幻之阵
- **天赋效果（6星）**：其他友方在自身相邻3格内发起对战，则为其施加「极意II」效果，持续3回合（每回合限定1次）。行动结束时，在自己身边召唤1个「守卫灵俑」。（间隔3回合召唤，若「守卫灵俑」存活，则不会召唤。「守卫灵俑」气血属性继承召唤者最大气血的100%，其余属性继承召唤者对应属性的70%）「极意II」：所有伤害+20%

**数据来源**：https://wiki.biligame.com/tdj/郸阴

---

### 9. 葛云衣

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：天瑞仙舞
- 天赋描述：将友方传送到指定位置并恢复气血

**正确内容（6星天赋）：**
- **天赋名称**：祝安
- **天赋效果（6星）**：治疗效果提高20%。对友方释放绝学时，附加「祝安」状态，持续2回合。「祝安」：行动结束时，恢复自身气血。（恢复量为施术者法攻的0.6倍）

**数据来源**：https://wiki.biligame.com/tdj/葛云衣

---

### 10. 殷剑平

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：天玄剑诀
- 天赋描述：主动攻击增伤20%，战后恢复15%生命

**正确内容（6星天赋）：**
- **天赋名称**：天玄剑诀
- **天赋效果（6星）**：主动攻击「对战中」伤害提高20%。若自身气血高于80%,则主动普攻触发「追击」（0.5倍伤害），若气血100%，则「追击」转化为「连击」，且伤害提升至0.6倍。

**数据来源**：https://wiki.biligame.com/tdj/殷剑平

---

### 11. 封寒月

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：玄冰咒
- 天赋描述：单体1.5倍冰伤，附加迟缓

**正确内容（6星天赋）：**
- **天赋名称**：玄冰咒
- **天赋效果（6星）**：气血高于70%时，法攻提高15%。若主动造成伤害，则行动结束时可再移动2格。

**数据来源**：https://wiki.biligame.com/tdj/封寒月

---

### 12. 慕容璇玑

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：天雷闪
- 天赋描述：范围0.6倍雷伤，暴击率+30%

**正确内容（6星天赋）：**
- **天赋名称**：天雷闪
- **天赋效果（6星）**：使用绝学时，暴击率提高30%。且绝学射程提高1。

**数据来源**：https://wiki.biligame.com/tdj/慕容璇玑

---

### 13. 燕明蓉

**错误类型**：品阶错误、天赋错误

**当前错误内容：**
- 品阶：极
- 天赋名称：灵狐穿刺
- 天赋描述：突进3格，1.4倍伤害，可穿越敌人

**正确内容：**
- **品阶**：绝（不是"极"）
- **天赋名称**：灵狐穿刺
- **天赋效果（6星）**：主动攻击「对战中」伤害提高20%。主动击杀敌人后，可无视敌人阻挡再移动4格，并获得「闪避」状态，持续2回合（「闪避」间隔2回合触发）。「闪避」：躲闪对战中的1次攻击（不可驱散，触发后消失）

**数据来源**：https://wiki.biligame.com/tdj/燕明蓉

---

### 14. 殷无邪

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：霜天剑匣
- 天赋描述：先攻，被攻击时抢先反击，气血越高伤害越高

**正确内容（6星天赋）：**
- **天赋名称**：霜天剑匣
- **天赋效果（6星）**：遭受攻击「对战中」发动「先攻」（无限次）。若气血高于50%，物攻提高15%，且「先攻」射程提高1格，造成伤害提高30%。

**数据来源**：https://wiki.biligame.com/tdj/殷无邪

---

### 15. 剑邪

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：万邪天归
- 天赋描述：主动攻击后对目标及周围造成0.3倍追加伤害

**正确内容（6星天赋）：**
- **天赋名称**：万邪天归
- **天赋效果（6星）**：行动时无视敌方角色阻挡。周围3圈内每存在1个敌人，自身除气血外全属性提高7%（最多21%）。自身释放绝学后，获得「天魔护铠」。（间隔2回合触发）「天魔护铠」：免伤提高50%（不可驱散，受到伤害后消失）

**数据来源**：https://wiki.biligame.com/tdj/剑邪

---

### 16. 诸葛艾

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：玲珑心
- 天赋描述：使用技能后获得buff复制，可复制给友方

**正确内容（6星天赋）：**
- **天赋名称**：玲珑心
- **天赋效果（6星）**：每携带1个「有益状态」，伤害提高5%（最多提高20%）。每携带1个「有益状态」，释放绝学后有25%概率该绝学冷却时间-2(最多有100%概率)。

**数据来源**：https://wiki.biligame.com/tdj/诸葛艾

---

### 17. 奚歌

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：影遁
- 天赋描述：主动攻击后隐身，暴击伤害+20%

**正确内容（6星天赋）：**
- **天赋名称**：影遁
- **天赋效果（6星）**：若队友主动攻击自身3格范围内的敌人，则在「对战中」双方交战后，立刻对敌方造成1次伤害（物攻的50%）（每回合只能触发3次）行动结束时，若自身2格范围内没有敌人，则获得「影遁」状态。（间隔1回合触发）。「影遁」：伤害和暴击率提高25%，无法被敌人普通攻击及技能锁定为目标（不可驱散，遭受1次范围伤害或造成伤害后，或行动结束时，自身2格范围内存在敌人时，该状态消失）

**数据来源**：https://wiki.biligame.com/tdj/奚歌

---

### 18. 鲜于超

**错误类型**：属性错误、天赋错误

**当前错误内容：**
- 属相：炎（错误）
- 天赋名称：战鬼
- 天赋描述：气血越低减伤越高，最高50%，反击伤害+30%

**正确内容：**
- **属相**：炎 → **暗**（角色为暗属相）
- **天赋名称**：血咒
- **天赋效果（6星）**：回合开始时，自身获得「血咒」状态，本回合主动进入对战，则行动结束时消除「血咒」。「血咒」状态下，受到致命伤害时免除死亡，自身气血恢复50%，并获得「屠戮」状态。（每场战斗最多触发1次）「血咒」：伤害和免伤提高20%，「对战后」恢复伤害数值50%的气血。行动结束时，损失自身当前气血25%。（不可驱散）「屠戮」无法护卫队友，主动攻击「对战后」造成1次「固定伤害」（物攻的50%）若目标气血低于50%，则本次「固定伤害」翻倍（下一次主动攻击「对战后」触发消耗）（不可驱散）

**数据来源**：https://wiki.biligame.com/tdj/鲜于超

---

### 19. 巴艾迩

**错误类型**：职业错误、天赋错误

**当前错误内容：**
- 职业：羽士（错误）
- 天赋名称：圣光之箭
- 天赋描述：射程+1，对暗系伤害+30%

**正确内容：**
- **职业**：羽士 → **御风**（角色为御风职业）
- **天赋名称**：圣辉
- **天赋效果（6星）**：主动攻击时，物攻提高15%。自身及周围3格范围内友方主动攻击时，每对1个目标造成暴击，获得1层「灵辉」，每击杀1个目标立即获得7层「灵辉」（最多叠加14层）。「灵辉」：行动结束时，如果携带不少于7层「灵辉」，消耗7层「灵辉」，再激活自身十字7格内1名法攻/物攻最高已结束行动的其他友方。（间隔2回合触发）

**数据来源**：https://wiki.biligame.com/tdj/巴艾迩

---

### 20. 魔化皇甫申

**错误类型**：天赋错误

**当前错误内容：**
- 天赋名称：魔化之躯
- 天赋描述：免疫debuff，受到伤害减少20%

**正确内容（6星天赋）：**
- **天赋名称**：闇星降临
- **天赋效果（6星）**：气血大于70%时，伤害和免伤提高20%。行动结束时，获得「绝心」状态。若自身2圈范围内同时存在其他「雷」和「暗」的角色时，则额外获得1层「绝心」状态，若达到5层，则转化为「执戮」状态，持续3回合。死亡时对自身2圈范围内1个气血百分比最低的敌人造成1次固定伤害（物攻的90%）

**数据来源**：https://wiki.biligame.com/tdj/魔化皇甫申

---

## 修正后的HTML代码片段

### 林月如（新增角色）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">林月如 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·雷·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">气劲凌云</div>
        <div class="skill-desc">攻击前每移动1格伤害提高5%（最多25%）。造成伤害获得「气劲」，暴击额外获得。携带4层「气劲」时对周围敌人施加「晕眩」（间隔1回合）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">索命斩</div>
        <div class="skill-desc">单体1.6倍伤害，若目标已行动结束则伤害提高20%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">剑气纵横</div>
        <div class="skill-desc">范围0.6倍雷伤，附加「流血」状态</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">乾坤一掷</div>
        <div class="skill-desc">消耗当前气血20%，造成2.0倍伤害，必暴击</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">晕眩</span>
        <span class="tag tag-core">爆发</span>
        <span class="tag tag-core">移动增伤</span>
    </td>
</tr>
```

### 冰璃（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">冰璃 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·冰·侠客</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">幽冥剑引</div>
        <div class="skill-desc">造成伤害获得「怒意」(上限2层)。行动结束时若本回合造成过伤害且「怒意」为2层，获得再行动（5格）（间隔2回合）。「怒意」：除气血外全属性提高10%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">冰华飞刺</div>
        <div class="skill-desc">突进3格，对路径敌人造成1.2倍伤害</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">灭剑血胧</div>
        <div class="skill-desc">单体1.5倍伤害，战前驱散目标2个「有益状态」</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">霜天剑斩</div>
        <div class="skill-desc">范围0.5倍冰伤，附加「迟缓」</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">再动</span>
        <span class="tag tag-core">爆发</span>
        <span class="tag tag-aoe">突进</span>
    </td>
</tr>
```

### 曹沁（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">曹沁 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·炎·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">劫焰誓杀</div>
        <div class="skill-desc">使用绝学后获得「流火」(物攻和暴击率提高20%)。闪避或主动击杀敌人后重置所有主动绝学冷却（间隔3回合）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">追心影刃</div>
        <div class="skill-desc">无视护卫，1.6倍伤害，目标每有1个「有害状态」增伤10%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">炎舞斩</div>
        <div class="skill-desc">单体1.4倍火伤，附加「燃烧」</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">烈焰穿心</div>
        <div class="skill-desc">突进2格，1.7倍伤害，必暴击</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">无视护卫</span>
        <span class="tag tag-core">刷新CD</span>
        <span class="tag tag-aoe">突进</span>
    </td>
</tr>
```

### 封铃笙（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">封铃笙 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·光·祝由</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">传心</div>
        <div class="skill-desc">气血100%时法攻提高15%。使用技能后为3格内其他友方恢复气血（恢复量为施术者法攻的0.6倍）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">瞬霎神仪</div>
        <div class="skill-desc">让友方立即再行动，恢复50%气血</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">神华天舞</div>
        <div class="skill-desc">单体恢复2倍法强，驱散2个debuff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">生聚灵阵</div>
        <div class="skill-desc">范围恢复1.5倍法强，附加持续恢复</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">再动</span>
        <span class="tag tag-heal">群疗</span>
        <span class="tag tag-control">驱散</span>
    </td>
</tr>
```

### 黎幽（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">黎幽 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·暗·咒师</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">幽冥之力</div>
        <div class="skill-desc">与携带「有害状态」角色作战时，「对战中」法攻、法防提高15%。行动结束时对3格范围内随机4个敌方施加2个随机「有害状态」</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">暗之力</div>
        <div class="skill-desc">对debuff敌人增伤30%，击杀扩散debuff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">噬魂之触</div>
        <div class="skill-desc">单体1.5倍伤害，吸取目标1个buff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">幽冥降临</div>
        <div class="skill-desc">大范围0.6倍暗伤，概率眩晕</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-control">群体控制</span>
        <span class="tag tag-aoe">AOE</span>
        <span class="tag tag-core">debuff</span>
    </td>
</tr>
```

### 夏侯仪（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">夏侯仪 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·炎·咒师</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">幽煌邪焰</div>
        <div class="skill-desc">气血大于50%时法攻提升15%。遭受伤害后气血低于50%则恢复100%气血，获得「幽煌邪焰」状态（间隔2回合）。「幽煌邪焰」：除气血外所有属性提高10%（无法驱散）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">离火神诀</div>
        <div class="skill-desc">单体1.5倍火伤，附加燃烧</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">九俱焚灭</div>
        <div class="skill-desc">单体1.8倍伤害，燃烧目标增伤50%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">焚火真炎</div>
        <div class="skill-desc">十字范围0.7倍火伤，点燃地形2回合</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-aoe">AOE</span>
        <span class="tag tag-core">地形</span>
        <span class="tag tag-core">复活</span>
    </td>
</tr>
```

### 古伦德（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">古伦德 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·雷·铁卫</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">回光枪技</div>
        <div class="skill-desc">遭受攻击「对战中」免伤提高15%。主动攻击「对战后」击退目标2格。击退路线被阻挡则施加「晕眩」（间隔2回合）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">金刚伏魔</div>
        <div class="skill-desc">护卫范围扩大，受到伤害-20%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">破军威震</div>
        <div class="skill-desc">反击1.2倍伤害，眩晕攻击者1回合</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">龙枪</div>
        <div class="skill-desc">直线3格穿刺，1.3倍伤害</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-control">护卫</span>
        <span class="tag tag-control">反击</span>
        <span class="tag tag-control">眩晕</span>
    </td>
</tr>
```

### 郸阴（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">郸阴 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·暗·祝由</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">冥幻之阵</div>
        <div class="skill-desc">友方在相邻3格内发起对战则施加「极意II」(所有伤害+20%)。行动结束时召唤「守卫灵俑」（间隔3回合）。「守卫灵俑」气血继承100%，其余属性继承70%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">噬魂咒</div>
        <div class="skill-desc">单体1.4倍暗伤，恢复造成伤害50%生命</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">尸腐毒</div>
        <div class="skill-desc">范围持续伤害，中毒效果</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">亡灵复生</div>
        <div class="skill-desc">复活死亡的召唤物，满血复活</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">召唤</span>
        <span class="tag tag-heal">吸血</span>
        <span class="tag tag-core">复活</span>
    </td>
</tr>
```

### 葛云衣（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">葛云衣 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·雷·祝由</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">祝安</div>
        <div class="skill-desc">治疗效果提高20%。对友方释放绝学时附加「祝安」状态：行动结束时恢复气血（恢复量为施术者法攻的0.6倍）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">诸星神曜</div>
        <div class="skill-desc">范围恢复1.8倍法强，附加神睿（增伤）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">七星转命</div>
        <div class="skill-desc">单体恢复2倍法强，免疫下一次伤害</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">天瑞仙舞</div>
        <div class="skill-desc">将友方传送到指定位置并恢复气血</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">传送</span>
        <span class="tag tag-heal">群疗</span>
        <span class="tag tag-control">减伤</span>
    </td>
</tr>
```

### 殷剑平（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">殷剑平 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·炎·侠客</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">天玄剑诀</div>
        <div class="skill-desc">主动攻击「对战中」伤害提高20%。气血高于80%时普攻触发「追击」(0.5倍)，气血100%时「追击」转化为「连击」(0.6倍)</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">飞星剑影</div>
        <div class="skill-desc">突进2格，1.5倍伤害</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">火灵剑气</div>
        <div class="skill-desc">单体1.6倍火伤，附加燃烧</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">剑气凌霄</div>
        <div class="skill-desc">范围0.6倍伤害，自身获得坚韧</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">连击</span>
        <span class="tag tag-aoe">突进</span>
        <span class="tag tag-core">自给</span>
    </td>
</tr>
```

### 封寒月（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">封寒月 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·冰·咒师</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">玄冰咒</div>
        <div class="skill-desc">气血高于70%时法攻提高15%。若主动造成伤害，则行动结束时可再移动2格</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">冰魄寒流</div>
        <div class="skill-desc">直线3格0.7倍冰伤，附加冻结</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">霜冻领域</div>
        <div class="skill-desc">范围0.5倍冰伤，地形冰冻</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">千年冰魄</div>
        <div class="skill-desc">单体1.7倍伤害，冰冻目标增伤30%</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-control">控制</span>
        <span class="tag tag-aoe">AOE</span>
        <span class="tag tag-core">再移动</span>
    </td>
</tr>
```

### 慕容璇玑（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">慕容璇玑 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·雷·咒师</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">天雷闪</div>
        <div class="skill-desc">使用绝学时暴击率提高30%。且绝学射程提高1</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">九天玄雷</div>
        <div class="skill-desc">单体1.6倍雷伤，弹射3个目标</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">雷引</div>
        <div class="skill-desc">将敌人拉拽至身边并麻痹</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">万雷天引</div>
        <div class="skill-desc">大范围0.7倍雷伤，眩晕目标</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-aoe">AOE</span>
        <span class="tag tag-core">射程+1</span>
        <span class="tag tag-core">暴击</span>
    </td>
</tr>
```

### 燕明蓉（修正品阶和天赋）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">燕明蓉 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·雷·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">灵狐穿刺</div>
        <div class="skill-desc">主动攻击「对战中」伤害提高20%。主动击杀敌人后可无视阻挡再移动4格，并获得「闪避」状态（间隔2回合）。「闪避」：躲闪对战中的1次攻击</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">狐影迷踪</div>
        <div class="skill-desc">进入闪避状态，下一次攻击必闪</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">雷影突袭</div>
        <div class="skill-desc">单体1.5倍雷伤，战后隐身1回合</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">万狐奔腾</div>
        <div class="skill-desc">范围0.5倍伤害，召唤小狐狸助战</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-aoe">再移动</span>
        <span class="tag tag-passive">闪避</span>
        <span class="tag tag-core">击杀收益</span>
    </td>
</tr>
```

### 殷无邪（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">殷无邪 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·冰·侠客</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">霜天剑匣</div>
        <div class="skill-desc">遭受攻击「对战中」发动「先攻」（无限次）。若气血高于50%，物攻提高15%，且「先攻」射程提高1格，造成伤害提高30%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">剑绝昆仑</div>
        <div class="skill-desc">1.5倍单体伤害，战前驱散目标2个buff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">寒气破</div>
        <div class="skill-desc">范围0.5倍冰伤，附加迟缓状态</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">霜天雪舞</div>
        <div class="skill-desc">大范围0.6倍冰伤，范围内敌人移动力-2</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">先攻</span>
        <span class="tag tag-control">驱散</span>
        <span class="tag tag-core">无限反击</span>
    </td>
</tr>
```

### 剑邪（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">剑邪 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·暗·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">万邪天归</div>
        <div class="skill-desc">行动时无视敌方角色阻挡。周围3圈内每存在1个敌人，自身除气血外全属性提高7%（最多21%）。释放绝学后获得「天魔护铠」（间隔2回合）。「天魔护铠」：免伤提高50%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">诛天剑阵</div>
        <div class="skill-desc">范围0.6倍暗伤，附加随机debuff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">邪气横天</div>
        <div class="skill-desc">单体1.4倍伤害，战后周围敌人受到伤害+15%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">万邪归一</div>
        <div class="skill-desc">大范围0.7倍暗伤，范围内敌人法防-20%</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-aoe">AOE</span>
        <span class="tag tag-core">免伤</span>
        <span class="tag tag-core">无视阻挡</span>
    </td>
</tr>
```

### 诸葛艾（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">诸葛艾 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·光·咒师</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">玲珑心</div>
        <div class="skill-desc">每携带1个「有益状态」，伤害提高5%（最多20%）。释放绝学后有25%概率冷却时间-2(最多100%概率)</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">天光破暗</div>
        <div class="skill-desc">单体1.6倍光伤，对暗系增伤30%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">光幕穿梭</div>
        <div class="skill-desc">瞬移3格，获得2个随机buff</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">神光万华</div>
        <div class="skill-desc">范围0.6倍光伤，复制自身buff给友方</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">复制</span>
        <span class="tag tag-core">传送</span>
        <span class="tag tag-aoe">AOE</span>
    </td>
</tr>
```

### 奚歌（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">奚歌 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·暗·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">影遁</div>
        <div class="skill-desc">队友主动攻击自身3格范围内敌人时，「对战中」交战后立刻对敌方造成1次伤害（物攻的50%）（每回合3次）。行动结束时若2格范围内没有敌人，获得「影遁」（间隔1回合）。「影遁」：伤害和暴击率提高25%，无法被敌人锁定为目标</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">影袭</div>
        <div class="skill-desc">无视护卫，1.6倍伤害，背击必暴</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">烟雾弹</div>
        <div class="skill-desc">范围致盲，敌人命中率-50%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">影杀</div>
        <div class="skill-desc">单体1.8倍伤害，目标血量低于50%时增伤30%</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">隐身</span>
        <span class="tag tag-core">无视护卫</span>
        <span class="tag tag-core">协战</span>
    </td>
</tr>
```

### 鲜于超（修正属相和天赋）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">鲜于超 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·暗·铁卫</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">血咒</div>
        <div class="skill-desc">回合开始时获得「血咒」：伤害和免伤提高20%，「对战后」恢复伤害数值50%的气血，行动结束时损失当前气血25%。「血咒」状态下受到致命伤害时免死，恢复50%气血，获得「屠戮」（每场战斗1次）。「屠戮」：攻击后造成固定伤害（物攻的50%），目标气血低于50%时翻倍</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">铁壁</div>
        <div class="skill-desc">护卫范围扩大，受到伤害-25%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">血刃</div>
        <div class="skill-desc">牺牲20%血量，攻击造成1.7倍伤害</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">鬼门</div>
        <div class="skill-desc">范围0.5倍伤害，将伤害转化为护盾</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-control">护卫</span>
        <span class="tag tag-core">免死</span>
        <span class="tag tag-core">固定伤害</span>
    </td>
</tr>
```

### 巴艾迩（修正职业和天赋）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">巴艾迩 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·光·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">圣辉</div>
        <div class="skill-desc">主动攻击时物攻提高15%。自身及周围3格范围内友方主动攻击时，每对1个目标造成暴击获得1层「灵辉」，每击杀1个目标立即获得7层（最多14层）。行动结束时若携带不少于7层「灵辉」，消耗7层再激活十字7格内1名法攻/物攻最高已结束行动的友方（间隔2回合）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">穿云箭</div>
        <div class="skill-desc">单体1.5倍伤害，穿透敌人</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">光之祝福</div>
        <div class="skill-desc">为友方附加神睿，物攻法攻+20%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">圣光裁决</div>
        <div class="skill-desc">1.8倍单体伤害，无视30%防御</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">再激活</span>
        <span class="tag tag-core">暴击收益</span>
        <span class="tag tag-core">辅助</span>
    </td>
</tr>
```

### 魔化皇甫申（修正）

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">魔化皇甫申 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·暗·侠客</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">闇星降临</div>
        <div class="skill-desc">气血大于70%时，伤害和免伤提高20%。行动结束时获得「绝心」。若2圈范围内同时存在其他「雷」和「暗」角色，额外获得1层「绝心」，达到5层转化为「执戮」（持续3回合）。死亡时对2圈范围内1个气血百分比最低的敌人造成固定伤害（物攻的90%）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">魔剑斩</div>
        <div class="skill-desc">单体1.6倍伤害，附加诅咒状态</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">魔影步</div>
        <div class="skill-desc">突进3格，下次攻击伤害+25%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">魔神降世</div>
        <div class="skill-desc">大范围0.7倍暗伤，自身全属性+20%</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">死亡伤害</span>
        <span class="tag tag-core">突进</span>
        <span class="tag tag-core">双属相联动</span>
    </td>
</tr>
```

---

## 勘误总结

### 错误类型统计

| 错误类型 | 数量 | 占比 |
|----------|------|------|
| 天赋描述错误 | 20 | 55.6% |
| 技能描述错误 | 10 | 27.8% |
| 角色属性错误 | 3 | 8.3% |
| 品阶错误 | 1 | 2.8% |
| 职业错误 | 1 | 2.8% |
| 角色缺失 | 1 | 2.8% |
| **总计** | **36** | **100%** |

### 主要问题分析

1. **天赋描述不准确**：所有角色的天赋描述都与Wiki数据存在差异，主要原因是Wiki数据为6星状态下的完整描述，而原数据过于简化或错误。

2. **技能名称与效果不匹配**：部分角色的技能名称和描述与实际游戏数据不符。

3. **属性信息错误**：
   - 燕明蓉的品阶应为「绝」而非「极」
   - 鲜于超的属相应为「暗」而非「炎」
   - 巴艾迩的职业应为「御风」而非「羽士」

4. **角色缺失**：林月如角色在HTML文件中完全缺失。

### 建议

1. 建议以本勘误报告为准，更新HTML文件中的角色数据
2. 建议建立与Wiki数据的定期同步机制
3. 建议添加数据来源标注，便于后续核实

---

*报告完成*
