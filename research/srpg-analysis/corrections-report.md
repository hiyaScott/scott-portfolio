# 天地劫角色技能数据库勘误报告

**数据来源**: [B站天地劫WIKI](https://wiki.biligame.com/tdj/%E8%8B%B1%E7%81%B5%E5%9B%BE%E9%89%B4)  
**勘误时间**: 2026-03-17  
**勘误范围**: 天地劫：幽城再临部分 (前20位角色)  

---

## 严重错误（天赋完全错误）

### 1. 林月如 ❌❌❌

| 字段 | 当前错误数据 | 正确数据（6星） |
|------|-------------|----------------|
| **天赋** | 斩龙诀 - 攻击后20%概率再行动，最多2次 | **月影芳踪** - 攻击前每移动1格伤害提高5%(最多25%)。每造成1次伤害获得1层「气劲」，暴击额外获得1层。行动结束时若携带4层「气劲」，消耗所有气劲对周围菱形2格范围内1个敌人施加「晕眩」1回合。(间隔1回合触发) |
| **技能1** | 斩龙破 - 单体1.6倍雷伤，30%概率眩晕 | **一阳指** - 攻击敌人造成1.5倍伤害，暴击率+20%。成功击杀目标则额外获得2层「气劲」 |
| **技能2** | 御剑术 - 射程2格，1.4倍伤害 | **斩龙诀** - 对范围内敌人造成0.6倍伤害，施加「电流」状态(遭受暴击率+20%)，持续2回合 |
| **大招** | 斩龙诀·极 - 大范围0.7倍雷伤，暴击率+40% | **乾坤一掷** - 对范围内所有敌人造成0.7倍伤害，暴击率+20%，对被暴击目标施加「雷劫」状态。行动结束时若自身菱形2格内有友方单位，则替换为「晕眩」1回合。[气力技]消耗3点气力 |
| **标签** | 再动、眩晕、远程 | **气劲、移动增伤、眩晕、AOE、气力技** |

**问题分析**: 天赋描述完全错误，将技能名误作天赋，核心机制（气劲系统）完全缺失。

**数据来源**: https://wiki.biligame.com/tdj/林月如

---

## 中度错误（天赋描述不准确）

### 2. 冰璃 ⚠️

| 字段 | 当前数据 | 正确数据（6星） |
|------|---------|----------------|
| **天赋** | 幽冥剑引 - 主动攻击1.8倍伤害，击杀后再行动 | **幽冥剑引** - 每造成1次伤害获得1层「怒意」(上限2层)。行动结束时若本回合造成过伤害且「怒意」为2层，获得再行动(5格)，本次行动结束时消除「怒意」(间隔2回合)。「怒意」除气血外全属性提高10% |

**差异说明**: 
- 当前描述过于简化，遗漏了核心机制：
  - 需要2层「怒意」才能触发再动
  - 「怒意」提供属性加成
  - 有间隔CD（2回合）
  - 再行动后消除怒意

**数据来源**: https://wiki.biligame.com/tdj/冰璃

---

### 3. 曹沁 ⚠️

| 字段 | 当前数据 | 正确数据（6星） |
|------|---------|----------------|
| **天赋** | 劫焰誓杀 - 标记敌人，击杀后刷新所有技能CD | **劫焰誓杀** - 使用绝学后获得「流火」状态(物攻和暴击率提高20%，不可驱散)，持续1回合。闪避或主动击杀敌人后重置所有主动绝学的冷却时间(间隔3回合触发) |

**差异说明**:
- 遗漏「流火」状态描述（物攻+暴击率提升）
- 遗漏闪避也能刷新CD的机制
- 刷新CD有3回合间隔

**数据来源**: https://wiki.biligame.com/tdj/曹沁

---

## 待验证角色清单

以下角色需要从B站Wiki获取数据进行对比：

| 序号 | 角色名 | Wiki链接 | 状态 |
|------|--------|----------|------|
| 4 | 封铃笙 | https://wiki.biligame.com/tdj/封铃笙 | 待验证 |
| 5 | 黎幽 | https://wiki.biligame.com/tdj/黎幽 | 待验证 |
| 6 | 夏侯仪 | https://wiki.biligame.com/tdj/夏侯仪 | 待验证 |
| 7 | 古伦德 | https://wiki.biligame.com/tdj/古伦德 | 待验证 |
| 8 | 郸阴 | https://wiki.biligame.com/tdj/郸阴 | 待验证 |
| 9 | 葛云衣 | https://wiki.biligame.com/tdj/葛云衣 | 待验证 |
| 10 | 殷剑平 | https://wiki.biligame.com/tdj/殷剑平 | 待验证 |
| 11 | 封寒月 | https://wiki.biligame.com/tdj/封寒月 | 待验证 |
| 12 | 慕容璇玑 | https://wiki.biligame.com/tdj/慕容璇玑 | 待验证 |
| 13 | 燕明蓉 | https://wiki.biligame.com/tdj/燕明蓉 | 待验证 |
| 14 | 殷无邪 | https://wiki.biligame.com/tdj/殷无邪 | 待验证 |
| 15 | 剑邪 | https://wiki.biligame.com/tdj/剑邪 | 待验证 |
| 16 | 诸葛艾 | https://wiki.biligame.com/tdj/诸葛艾 | 待验证 |
| 17 | 奚歌 | https://wiki.biligame.com/tdj/奚歌 | 待验证 |
| 18 | 鲜于超 | https://wiki.biligame.com/tdj/鲜于超 | 待验证 |
| 19 | 巴艾迩 | https://wiki.biligame.com/tdj/巴艾迩 | 待验证 |
| 20 | 魔化皇甫申 | https://wiki.biligame.com/tdj/魔化皇甫申 | 待验证 |

---

## 修正后的HTML代码

### 林月如修正代码

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">林月如 <span class="tag tag-t1">T1</span></div>
        <div class="hero-meta">绝·雷·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">月影芳踪</div>
        <div class="skill-desc">移动增伤最高25%，攒4层「气劲」自动眩晕周围敌人（间隔1回合）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">一阳指</div>
        <div class="skill-desc">1.5倍伤害，暴击率+20%，击杀额外+2层气劲</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">斩龙诀</div>
        <div class="skill-desc">范围0.6倍伤害，施加「电流」（遭受暴击率+20%）</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">乾坤一掷</div>
        <div class="skill-desc">范围0.7倍伤害，暴击率+20%，被暴击者附加「雷劫」[气力技]</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">气劲</span>
        <span class="tag tag-core">移动增伤</span>
        <span class="tag tag-control">眩晕</span>
        <span class="tag tag-aoe">AOE</span>
    </td>
</tr>
```

### 冰璃修正代码

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">冰璃 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·冰·侠客</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">幽冥剑引</div>
        <div class="skill-desc">造成伤害获得「怒意」2层后，获得再行动(5格)，间隔2回合。「怒意」全属性+10%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">冰华飞刺</div>
        <div class="skill-desc">突进3格，对路径敌人造成1.2倍伤害</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">灭剑血胧</div>
        <div class="skill-desc">单体1.5倍伤害，战后吸血30%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">霜天剑斩</div>
        <div class="skill-desc">范围0.5倍冰伤，附加迟缓</div>
    </td>
    <td class="tags-cell">
        <span class="tag tag-core">再动</span>
        <span class="tag tag-core">爆发</span>
        <span class="tag tag-aoe">突进</span>
    </td>
</tr>
```

### 曹沁修正代码

```html
<tr>
    <td class="hero-cell">
        <div class="hero-name">曹沁 <span class="tag tag-t0">T0</span></div>
        <div class="hero-meta">绝·炎·御风</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">劫焰誓杀</div>
        <div class="skill-desc">使用绝学获得「流火」(物攻/暴击+20%)。闪避或击杀后重置所有技能CD，间隔3回合</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">追心影刃</div>
        <div class="skill-desc">无视护卫，1.6倍伤害，目标每debuff增伤10%</div>
    </td>
    <td class="skill-cell">
        <div class="skill-name">炎舞斩</div>
        <div class="skill-desc">单体1.4倍火伤，附加燃烧</div>
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

---

## 勘误建议

### 1. 短期措施
- [ ] 立即修正林月如数据（天赋完全错误）
- [ ] 更新冰璃、曹沁天赋描述（增加细节）
- [ ] 批量验证剩余15位角色的数据

### 2. 长期措施
- [ ] 建立定期勘误机制（每季度对照Wiki检查一次）
- [ ] 添加勘误提交入口到网页
- [ ] 在页面底部添加数据来源声明

---

## 附录：数据来源

所有正确数据均来自：
- B站天地劫WIKI: https://wiki.biligame.com/tdj/
- 具体角色页链接见上文

**注意**: Wiki数据基于6星满练度状态描述。
