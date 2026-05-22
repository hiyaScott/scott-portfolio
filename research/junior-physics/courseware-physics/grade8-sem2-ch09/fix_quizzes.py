import re

with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Quiz data for ch09 (6 units with placeholders)
quiz_data = {
    'ch1': [  # 熔化与凝固
        {'q': '晶体熔化时的特点是？', 'a': 'B', 'opts': [('A. 温度不断升高', '不对，晶体熔化时温度不变'), ('B. 吸热但温度不变', '正确！晶体有固定熔点'), ('C. 放热', '不对，熔化吸热')]},
        {'q': '冰的熔点是 0℃，则 0℃的冰？', 'a': 'C', 'opts': [('A. 一定熔化', '不一定，还需要继续吸热'), ('B. 一定不熔化', '不一定'), ('C. 可能是固态、固液共存或液态', '正确！')]},
        {'q': '萘的熔点是 80.5℃，则 80.5℃的萘？', 'a': 'C', 'opts': [('A. 一定是固态', '不一定'), ('B. 一定是液态', '不一定'), ('C. 可能是固态、固液共存或液态', '正确！')]},
    ],
    'ch2': [  # 汽化与液化
        {'q': '水烧开后继续加热，温度会？', 'a': 'B', 'opts': [('A. 继续升高', '不对，沸腾时温度不变'), ('B. 保持不变', '正确！沸点时温度不变'), ('C. 降低', '不对')]},
        {'q': '影响蒸发快慢的因素不包括？', 'a': 'C', 'opts': [('A. 温度', '是影响因素'), ('B. 表面积', '是影响因素'), ('C. 质量', '不是影响因素')]},
        {'q': '夏天从冰箱拿出饮料，瓶外壁出现水珠，这是？', 'a': 'B', 'opts': [('A. 熔化', '不对'), ('B. 液化', '正确！空气中的水蒸气遇冷液化'), ('C. 凝华', '不对')]},
    ],
    'ch3': [  # 升华与凝华
        {'q': '冬天冰冻的衣服也会变干，这是？', 'a': 'A', 'opts': [('A. 升华', '正确！冰直接变成水蒸气'), ('B. 熔化', '不对'), ('C. 汽化', '不对')]},
        {'q': '霜的形成是？', 'a': 'C', 'opts': [('A. 凝固', '不对'), ('B. 液化', '不对'), ('C. 凝华', '正确！水蒸气直接变成固态')]},
        {'q': '用久了的灯泡内壁变黑，是因为钨丝？', 'a': 'C', 'opts': [('A. 熔化', '不对'), ('B. 汽化', '不对'), ('C. 先升华后凝华', '正确！钨丝升华后凝华在玻璃上')]},
    ],
    'ch4': [  # 熔化与凝固图像
        {'q': '晶体熔化图像的特点是？', 'a': 'B', 'opts': [('A. 温度一直上升', '非晶体特征'), ('B. 有一段水平线段', '正确！水平段表示熔化过程'), ('C. 温度先升后降', '不对')]},
        {'q': '从熔化图像的水平段可以得到？', 'a': 'B', 'opts': [('A. 比热容', '不是'), ('B. 熔点', '正确！水平段对应的温度就是熔点'), ('C. 沸点', '不对')]},
        {'q': '非晶体熔化图像的特点是？', 'a': 'A', 'opts': [('A. 温度一直上升', '正确！没有固定熔点'), ('B. 有水平线段', '晶体特征'), ('C. 温度不变', '不对')]},
    ],
    'ch5': [  # 汽化图像与沸腾
        {'q': '水沸腾的条件是？', 'a': 'C', 'opts': [('A. 达到 80℃', '不对，标准大气压下是 100℃'), ('B. 达到 100℃', '还需要继续吸热'), ('C. 达到沸点且继续吸热', '正确！')]},
        {'q': '水沸腾时，气泡上升过程中会？', 'a': 'A', 'opts': [('A. 变大', '正确！越往上压强越小，气泡膨胀'), ('B. 变小', '不对，那是沸腾前），('C. 不变', '不对')]},
        {'q': '高山上煮不熟鸡蛋，是因为？', 'a': 'B', 'opts': [('A. 温度太低', '不是温度低，是沸点低'), ('B. 气压低，沸点低', '正确！'), ('C. 火不够大', '不对')]},
    ],
    'ch6': [  # 综合与实验
        {'q': '下列现象中，属于液化的是？', 'a': 'C', 'opts': [('A. 冬天窗玻璃上的冰花', '凝华'), ('B. 湿衣服变干', '汽化'), ('C. 清晨草叶上的露珠', '正确！水蒸气液化')]},
        {'q': '把 0℃的冰放入 0℃的水中（周围气温也是 0℃），冰会？', 'a': 'C', 'opts': [('A. 全部熔化', '不能吸热'), ('B. 部分熔化', '不能吸热'), ('C. 不熔化', '正确！没有温度差，不能吸热')]},
        {'q': '关于物态变化，下列说法正确的是？', 'a': 'B', 'opts': [('A. 蒸发只在液体表面发生，沸腾只在内部发生', '沸腾在表面和内部都发生'), ('B. 蒸发和沸腾都是汽化现象', '正确！'), ('C. 晶体熔化时温度升高，非晶体熔化时温度不变', '说反了')]},
    ],
}

# Flatten all quiz data
all_quizzes = []
for card_id in ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6']:
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
