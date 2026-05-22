import re

with open('tutorial.html', 'r') as f:
    content = f.read()

# Quiz data for each unit (ch0-ch6, but ch0 and ch6 may have fewer)
quiz_data = {
    'ch0': [  # 实验简报 - keep fewer quizzes
        {
            'q': '密度的国际单位是？',
            'opts': [
                ('A. kg/m³', True, '正确！密度的国际单位是 kg/m³。'),
                ('B. g/cm³', False, 'g/cm³ 也是常用单位，但不是国际单位制基本单位。'),
                ('C. kg/m²', False, 'kg/m² 是面密度单位，不是体密度。')
            ]
        },
        {
            'q': '压强的定义是？',
            'opts': [
                ('A. 压力除以受力面积', True, '正确！p = F/S，压强等于压力除以受力面积。'),
                ('B. 压力乘以受力面积', False, '不对。压强 = F/S，不是 F×S。'),
                ('C. 受力面积除以压力', False, '不对。公式是 p = F/S。')
            ]
        },
        {
            'q': '液体压强的大小与什么因素有关？',
            'opts': [
                ('A. 液体密度和深度', True, '正确！p = ρgh，与液体密度和深度有关。'),
                ('B. 容器形状', False, '不对。液体压强与容器形状无关。'),
                ('C. 液体总质量', False, '不对。液体压强只与密度和深度有关。')
            ]
        }
    ],
    'ch1': [  # 密度
        {
            'q': '一块金属质量为 540 g，体积为 200 cm³，其密度是？',
            'opts': [
                ('A. 0.37 g/cm³', False, '不对。ρ = m/V = 540/200 = 2.7 g/cm³。'),
                ('B. 2.7 g/cm³', True, '正确！ρ = 540/200 = 2.7 g/cm³，这是铝的密度。'),
                ('C. 108 g/cm³', False, '不对。ρ = m/V = 540/200 = 2.7 g/cm³。')
            ]
        },
        {
            'q': '一杯水结成冰后，不变的是？',
            'opts': [
                ('A. 体积', False, '不对。水结冰体积会变大。'),
                ('B. 密度', False, '不对。冰的密度比水小。'),
                ('C. 质量', True, '正确！质量是物体的属性，状态变化时质量不变。')
            ]
        },
        {
            'q': '1 g/cm³ 等于多少 kg/m³？',
            'opts': [
                ('A. 1 kg/m³', False, '不对。1 g/cm³ = 1000 kg/m³。'),
                ('B. 100 kg/m³', False, '不对。1 g/cm³ = 1000 kg/m³。'),
                ('C. 1000 kg/m³', True, '正确！1 g/cm³ = 10³ kg/m³ = 1000 kg/m³。')
            ]
        }
    ],
    'ch2': [  # 压强
        {
            'q': '一个重 600 N 的人站在地面上，双脚与地面接触面积共 0.04 m²，他对地面的压强是？',
            'opts': [
                ('A. 15 Pa', False, '不对。p = F/S = 600/0.04 = 15000 Pa。'),
                ('B. 1500 Pa', False, '不对。p = F/S = 600/0.04 = 15000 Pa。'),
                ('C. 15000 Pa', True, '正确！p = 600/0.04 = 15000 Pa = 15 kPa。')
            ]
        },
        {
            'q': '下列事例中，属于增大压强的是？',
            'opts': [
                ('A. 坦克装有履带', False, '不对。履带增大受力面积，减小压强。'),
                ('B. 刀刃磨得很薄', True, '正确！刀刃磨薄减小受力面积，增大压强。'),
                ('C. 书包带做得较宽', False, '不对。宽带增大面积，减小压强。')
            ]
        },
        {
            'q': '将一块砖平放、侧放、竖放在水平地面上，哪种放法对地面压强最大？',
            'opts': [
                ('A. 平放', False, '不对。平放受力面积最大，压强最小。'),
                ('B. 侧放', False, '不对。竖放受力面积最小，压强最大。'),
                ('C. 竖放', True, '正确！竖放受力面积最小，p = F/S，压强最大。')
            ]
        }
    ],
    'ch3': [  # 液体压强
        {
            'q': '潜水员在海面下 20 m 处受到的液体压强约为多少？（ρ海水 ≈ 1.03×10³ kg/m³，g = 10 N/kg）',
            'opts': [
                ('A. 2060 Pa', False, '不对。p = ρgh = 1.03×10³×10×20 = 2.06×10⁵ Pa。'),
                ('B. 20600 Pa', False, '不对。p = 1.03×10³×10×20 = 2.06×10⁵ Pa。'),
                ('C. 2.06×10⁵ Pa', True, '正确！p = ρgh = 1.03×10³×10×20 = 2.06×10⁵ Pa。')
            ]
        },
        {
            'q': '关于液体压强，下列说法正确的是？',
            'opts': [
                ('A. 液体压强与容器形状有关', False, '不对。液体压强只与 ρ 和 h 有关，与容器形状无关。'),
                ('B. 同一深度，液体向各个方向压强相等', True, '正确！同一深度，液体向各个方向的压强相等。'),
                ('C. 液体压强与液体总质量有关', False, '不对。液体压强只与密度和深度有关。')
            ]
        },
        {
            'q': '如图所示，装有水的容器侧壁上有三个小孔，水从孔中喷出，喷得最远的是？',
            'opts': [
                ('A. 最上面的孔', False, '不对。深度越小，压强越小，喷得越近。'),
                ('B. 中间的孔', False, '不对。最下面的孔深度最大，压强最大。'),
                ('C. 最下面的孔', True, '正确！深度越大，液体压强越大，水喷得越远。')
            ]
        }
    ],
    'ch4': [  # 大气压强
        {
            'q': '标准大气压大约是多少？',
            'opts': [
                ('A. 1.01×10³ Pa', False, '不对。标准大气压约 1.01×10⁵ Pa。'),
                ('B. 1.01×10⁵ Pa', True, '正确！标准大气压 p₀ ≈ 1.01×10⁵ Pa。'),
                ('C. 10.1 Pa', False, '不对。标准大气压约 1.01×10⁵ Pa。')
            ]
        },
        {
            'q': '用吸管吸饮料时，饮料被吸入口中是因为？',
            'opts': [
                ('A. 嘴的吸力把饮料吸上来', False, '不对。嘴吸气时管内气压降低，是大气压把饮料压上来。'),
                ('B. 大气压的作用', True, '正确！吸气使管内气压降低，大气压把饮料压入嘴里。'),
                ('C. 饮料自己流上来', False, '不对。是大气压的作用。')
            ]
        },
        {
            'q': '托里拆利实验中，如果玻璃管倾斜，水银柱的竖直高度会？',
            'opts': [
                ('A. 变大', False, '不对。竖直高度不变，管内水银长度变长。'),
                ('B. 不变', True, '正确！竖直高度只与大气压有关，倾斜时高度不变，长度变长。'),
                ('C. 变小', False, '不对。竖直高度不变。')
            ]
        }
    ],
    'ch5': [  # 浮力
        {
            'q': '一个体积为 2×10⁻³ m³ 的物体浸没在水中，受到的浮力是多少？（ρ水 = 1.0×10³ kg/m³，g = 10 N/kg）',
            'opts': [
                ('A. 2 N', False, '不对。F浮 = ρgV排 = 10³×10×2×10⁻³ = 20 N。'),
                ('B. 20 N', True, '正确！F浮 = 1.0×10³×10×2×10⁻³ = 20 N。'),
                ('C. 0.2 N', False, '不对。F浮 = 20 N。')
            ]
        },
        {
            'q': '将同一木块分别放入水和酒精中（ρ酒精 < ρ水），木块静止后，受到的浮力关系是？',
            'opts': [
                ('A. 水中浮力大', False, '不对。木块在两种液体中都漂浮，浮力都等于重力。'),
                ('B. 一样大', True, '正确！漂浮时 F浮 = G，同一木块重力相同，浮力相同。'),
                ('C. 酒精中浮力大', False, '不对。漂浮时浮力都等于重力。')
            ]
        },
        {
            'q': '潜水艇是通过什么方式实现上浮和下潜的？',
            'opts': [
                ('A. 改变自身重力', True, '正确！潜水艇通过充放水改变自身重力来实现浮沉。'),
                ('B. 改变排开水的体积', False, '不对。潜水艇体积不变，V排不变，是通过改变自身重力。'),
                ('C. 改变水的密度', False, '不对。是通过改变自身重力。')
            ]
        }
    ],
    'ch6': [  # 综合实验
        {
            'q': '一个物体在水中下沉，说明它的密度与水的密度关系是？',
            'opts': [
                ('A. ρ物 < ρ水', False, '不对。ρ物 < ρ水时会漂浮。'),
                ('B. ρ物 > ρ水', True, '正确！物体密度大于液体密度时会下沉。'),
                ('C. ρ物 = ρ水', False, '不对。ρ物 = ρ水时会悬浮。')
            ]
        },
        {
            'q': '用弹簧测力计测得某物体在空气中的重力为 10 N，浸没在水中时测力计示数为 6 N，该物体受到的浮力是？',
            'opts': [
                ('A. 16 N', False, '不对。F浮 = G - F拉 = 10 - 6 = 4 N。'),
                ('B. 4 N', True, '正确！F浮 = G - F拉 = 10 N - 6 N = 4 N。'),
                ('C. 6 N', False, '不对。F浮 = G - F拉 = 4 N。')
            ]
        },
        {
            'q': '同一物体分别浸没在水和煤油中（ρ煤油 < ρ水），受到的浮力关系是？',
            'opts': [
                ('A. 水中浮力大', True, '正确！V排相同，ρ水 > ρ煤油，所以水中浮力大。'),
                ('B. 一样大', False, '不对。F浮 = ρ液gV排，V排相同，ρ大的浮力大。'),
                ('C. 煤油中浮力大', False, '不对。ρ水 > ρ煤油，水中浮力大。')
            ]
        }
    ]
}

# Function to build new quiz HTML
def build_quiz(card_id, quiz_num, quiz_data):
    q_text = quiz_data['q']
    opts = quiz_data['opts']
    
    html = f'''<div id="q{card_id[1:]}_{quiz_num}">
      <p><strong>Q{quiz_num}.</strong> {q_text}</p>'''
    
    for letter, text, is_correct, feedback in [('A', opts[0][0], opts[0][1], opts[0][2]),
                                                  ('B', opts[1][0], opts[1][1], opts[1][2]),
                                                  ('C', opts[2][0], opts[2][1], opts[2][2])]:
        html += f'''
      <button class="quiz-option" onclick="checkQuiz(this, {str(is_correct).lower()}, '{feedback}')">{letter}. {text}</button>'''
    
    html += f'''
      <div class="feedback" id="fb-{card_id[1:]}_{quiz_num}"></div>
    </div>'''
    
    return html

# Replace quizzes in each card
for card_id in ['ch0', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6']:
    card_start = content.find(f'id="{card_id}"')
    card_end = content.find(f'id="ch', card_start + 1)
    if card_end == -1:
        card_end = len(content)
    
    # Find quiz section in this card (starts with <h3>🎯 随堂测验)
    quiz_start = content.find('<h3>🎯 随堂测验', card_start)
    if quiz_start == -1 or quiz_start >= card_end:
        print(f'{card_id}: No quiz section found')
        continue
    
    # Find the end of quiz section (next <div class="btn-row"> or card end)
    quiz_end = content.find('<div class="btn-row"', quiz_start)
    if quiz_end == -1:
        quiz_end = card_end
    
    # Build new quiz HTML
    quizzes = quiz_data.get(card_id, [])
    if not quizzes:
        print(f'{card_id}: No quiz data')
        continue
    
    new_quiz_html = f'    <h3>🎯 随堂测验</h3>\n'
    for i, q in enumerate(quizzes, 1):
        new_quiz_html += build_quiz(card_id, i, q) + '\n'
    
    # Replace
    old_section = content[quiz_start:quiz_end]
    content = content[:quiz_start] + new_quiz_html + content[quiz_end:]
    
    print(f'{card_id}: Replaced {len(old_section)} bytes with {len(new_quiz_html)} bytes')

# Write result
with open('tutorial.html', 'w') as f:
    f.write(content)

print(f"\nFinal file size: {len(content)} bytes")
print(f"Placeholder count: {content.count('请根据本单元内容设计测试题')}")
print(f"checkQuiz calls: {content.count('checkQuiz(')}")
