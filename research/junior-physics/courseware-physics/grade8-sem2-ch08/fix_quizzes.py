import re

with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Quiz data for ch08 (7 units - 简单机械)
quiz_data = {
    'ch1': [  # 杠杆
        {'q': '杠杆的平衡条件是？', 'a': 'B', 'opts': [('A. F₁+F₂=L₁+L₂', '不对'), ('B. F₁L₁=F₂L₂', '正确！杠杆平衡条件'), ('C. F₁/L₁=F₂/L₂', '不对')]},
        {'q': '下列属于省力杠杆的是？', 'a': 'B', 'opts': [('A. 镊子', '费力杠杆'), ('B. 撬棍', '正确！动力臂>阻力臂，省力'), ('C. 天平', '等臂杠杆')]},
        {'q': '用撬棍撬石头，动力臂 1m，阻力臂 0.2m，阻力 500N，动力是？', 'a': 'B', 'opts': [('A. 2500 N', '反了，F₁=F₂L₂/L₁=500×0.2/1=100'), ('B. 100 N', '正确！F₁=500×0.2/1=100N'), ('C. 500 N', '不对')]},
    ],
    'ch2': [  # 滑轮
        {'q': '定滑轮的作用是？', 'a': 'B', 'opts': [('A. 省力', '不对，定滑轮不省力'), ('B. 改变力的方向', '正确！'), ('C. 省距离', '不对')]},
        {'q': '动滑轮可以省多少力？', 'a': 'B', 'opts': [('A. 全部力', '不对，理想情况省一半'), ('B. 一半力', '正确！动滑轮省一半力'), ('C. 四分之一', '不对')]},
        {'q': '滑轮组中，承担重物的绳子段数为 3，拉力是重物的？', 'a': 'B', 'opts': [('A. 3倍', '反了'), ('B. 1/3', '正确！F=G/n'), ('C. 一样', '不对')]},
    ],
    'ch3': [  # 轮轴
        {'q': '轮轴的实质是？', 'a': 'B', 'opts': [('A. 等臂杠杆', '不对'), ('B. 变形杠杆', '正确！轮轴是可以连续转动的杠杆'), ('C. 滑轮组合', '不对')]},
        {'q': '方向盘、门把手利用了？', 'a': 'A', 'opts': [('A. 轮轴', '正确！'), ('B. 定滑轮', '不对'), ('C. 动滑轮', '不对')]},
        {'q': '轮轴中，轮半径是轴半径的 4 倍，作用在轮上的力是轴上阻力的？', 'a': 'B', 'opts': [('A. 4倍', '反了'), ('B. 1/4', '正确！'), ('C. 一样', '不对')]},
    ],
    'ch4': [  # 斜面
        {'q': '斜面的作用是？', 'a': 'A', 'opts': [('A. 省力', '正确！斜面可以省力'), ('B. 省距离', '不对，费距离'), ('C. 改变方向', '不对')]},
        {'q': '盘山公路利用了？', 'a': 'A', 'opts': [('A. 斜面', '正确！'), ('B. 杠杆', '不对'), ('C. 轮轴', '不对')]},
        {'q': '斜面长 5m，高 1m，物体重 1000N，不计摩擦，沿斜面匀速向上推的力是？', 'a': 'B', 'opts': [('A. 1000 N', '不对，F=Gh/L=1000×1/5=200'), ('B. 200 N', '正确！F=Gh/L=200N'), ('C. 5000 N', '不对')]},
    ],
    'ch5': [  # 机械效率
        {'q': '机械效率的公式是？', 'a': 'B', 'opts': [('A. W总/W有', '反了'), ('B. W有/W总', '正确！η=W有/W总'), ('C. W有+W总', '不对')]},
        {'q': '机械效率总是？', 'a': 'A', 'opts': [('A. 小于1', '正确！因为总有额外功'), ('B. 等于1', '不可能，有额外功'), ('C. 大于1', '不可能')]},
        {'q': '提高滑轮组机械效率的方法是？', 'a': 'C', 'opts': [('A. 增加物重', '这不是主要方法'), ('B. 增加滑轮数量', '这会降低效率'), ('C. 减小摩擦和动滑轮重', '正确！')]},
    ],
    'ch6': [  # 功和功率
        {'q': '功的两个必要因素是？', 'a': 'B', 'opts': [('A. 力和时间', '不对'), ('B. 力和在力方向上的位移', '正确！W=Fs'), ('C. 力和速度', '不对')]},
        {'q': '功率的物理意义是？', 'a': 'B', 'opts': [('A. 做功的多少', '这是功'), ('B. 做功的快慢', '正确！功率表示做功快慢'), ('C. 做功的时间', '不对')]},
        {'q': '一台机器功率为 1000W，工作 10s 做功？', 'a': 'B', 'opts': [('A. 100 J', '不对，W=Pt=1000×10=10000'), ('B. 10000 J', '正确！'), ('C. 100000 J', '不对')]},
    ],
    'ch7': [  # 综合
        {'q': '使用任何机械都？', 'a': 'B', 'opts': [('A. 省力', '不一定'), ('B. 不省功', '正确！功的原理：使用任何机械都不省功'), ('C. 省距离', '不一定')]},
        {'q': '杠杆、滑轮、斜面共同的物理原理是？', 'a': 'C', 'opts': [('A. 能量守恒', '不是最直接的'), ('B. 质量守恒', '不对'), ('C. 功的原理', '正确！都不省功')]},
        {'q': '下列说法正确的是？', 'a': 'B', 'opts': [('A. 机械效率高的机械做功多', '不对，效率高不代表做功多'), ('B. 机械效率高的机械有用功占比大', '正确！'), ('C. 功率大的机械效率高', '不对，功率和效率是不同的概念')]},
    ],
}

# Flatten all quiz data
all_quizzes = []
for card_id in ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7']:
    quizzes = quiz_data.get(card_id, [])
    all_quizzes.extend(quizzes)

print(f'Total quiz data: {len(all_quizzes)}')

# Find all quiz blocks with placeholders
quiz_pattern = r'<h3>🎯 随堂测验 Q\d+</h3>\s*<div id="q_\d+_\d+"\s*>(.*?</div>)\s*</div>'
matches = list(re.finditer(quiz_pattern, content, re.DOTALL))
print(f'Found {len(matches)} quiz blocks')

# Replace each quiz block
new_content = content
offset = 0
replaced = 0

for i, m in enumerate(matches):
    if i >= len(all_quizzes):
        break
    
    q_data = all_quizzes[i]
    
    # Build new quiz HTML
    opts_html = ''
    for letter, (text, fb) in [('A', q_data['opts'][0]), ('B', q_data['opts'][1]), ('C', q_data['opts'][2])]:
        is_correct = letter == q_data['a']
        opts_html += f'<button class="quiz-option" onclick="checkQuiz(this, {str(is_correct).lower()}, \'{fb}\')">{letter}. {text}</button>\n'
    
    new_quiz = f'''<h3>🎯 随堂测验 Q{(i%3)+1}</h3>
<div id="q_{i//3}_{(i%3)+1}">
  <p><strong>Q{(i%3)+1}.</strong> {q_data['q']}</p>
  {opts_html}
  <div class="feedback" id="fb_{i//3}_{(i%3)+1}"></div>
</div>'''
    
    start = m.start() + offset
    end = m.end() + offset
    new_content = new_content[:start] + new_quiz + new_content[end:]
    offset += len(new_quiz) - (m.end() - m.start())
    replaced += 1

print(f'Replaced {replaced} quizzes')

# Check placeholders
ph = new_content.count('请根据本单元内容设计测试题')
print(f'Remaining placeholders: {ph}')

# Fix div imbalance
div_o = new_content.count('<div')
div_c = new_content.count('</div>')
diff = div_c - div_o

if diff > 0:
    body_end = new_content.rfind('</body>')
    for _ in range(diff):
        last_div = new_content.rfind('</div>', 0, body_end)
        if last_div > 0:
            new_content = new_content[:last_div] + new_content[last_div+6:]
            body_end = new_content.rfind('</body>')
    print(f'Removed {diff} extra closing divs')

# Recount
div_o = new_content.count('<div')
div_c = new_content.count('</div>')
print(f'Div: {div_o}/{div_c}')

with open('tutorial.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Saved!')
