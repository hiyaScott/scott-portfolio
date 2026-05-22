import re

with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all quiz blocks that still have placeholders
quiz_blocks = []
for m in re.finditer(r'<h3>🎯 随堂测验.*?</h3>', content):
    start = m.start()
    end = content.find('<h3>', start + 1)
    if end == -1:
        end = content.find('<div class="btn-row"', start)
    if end == -1:
        end = len(content)
    
    quiz_section = content[start:end]
    if '请根据本单元内容设计测试题' in quiz_section:
        quiz_blocks.append((start, end, quiz_section))

print(f'Found {len(quiz_blocks)} remaining quiz blocks')

# Extra questions for ch08
extra_questions = [
    {'q': '杠杆上，动力臂与阻力臂相等的是？', 'a': 'C', 'opts': [('A. 撬棍', '省力'), ('B. 镊子', '费力'), ('C. 天平', '正确！等臂杠杆')]},
    {'q': '定滑轮相当于？', 'a': 'A', 'opts': [('A. 等臂杠杆', '正确！'), ('B. 省力杠杆', '不对'), ('C. 费力杠杆', '不对')]},
    {'q': '动滑轮相当于动力臂是阻力臂几倍的杠杆？', 'a': 'B', 'opts': [('A. 1倍', '不对'), ('B. 2倍', '正确！'), ('C. 3倍', '不对')]},
    {'q': '斜面越平缓？', 'a': 'A', 'opts': [('A. 越省力', '正确！但费距离'), ('B. 越费力', '不对'), ('C. 不省力也不费力', '不对')]},
    {'q': '做同样的有用功，额外功越少，机械效率？', 'a': 'A', 'opts': [('A. 越高', '正确！'), ('B. 越低', '反了'), ('C. 不变', '不对')]},
    {'q': '功率大表示？', 'a': 'A', 'opts': [('A. 做功快', '正确！'), ('B. 做功多', '不一定，还要看时间'), ('C. 省力', '不对')]},
    {'q': '使用滑轮组时，承担重物的绳子段数越多？', 'a': 'C', 'opts': [('A. 越费距离', '反了'), ('B. 越费力', '反了'), ('C. 越省力', '正确！但费距离')]},
    {'q': '轮轴中，动力作用在轮上，轮半径越大？', 'a': 'A', 'opts': [('A. 越省力', '正确！'), ('B. 越费力', '不对'), ('C. 无影响', '不对')]},
    {'q': '两台机器，甲的功率是乙的2倍，则甲做功？', 'a': 'C', 'opts': [('A. 一定比乙多', '不一定，还要看时间'), ('B. 一定比乙少', '不对'), ('C. 不一定，要看时间', '正确！W=Pt')]},
    {'q': '关于功、功率、机械效率，正确的是？', 'a': 'C', 'opts': [('A. 功率大的机器做功多', '不一定'), ('B. 效率高的机器功率大', '无关'), ('C. 效率高的机器有用功占比大', '正确！')]},
    {'q': '用滑轮组提升重物，增加被提升物体的重量（不计摩擦），机械效率？', 'a': 'A', 'opts': [('A. 提高', '正确！有用功占比增大'), ('B. 降低', '不对'), ('C. 不变', '不对')]},
    {'q': '下列工具中，属于费力杠杆的是？', 'a': 'A', 'opts': [('A. 筷子', '正确！费力但省距离'), ('B. 起子', '省力'), ('C. 剪刀', '不一定')]},
    {'q': '斜面的机械效率一般？', 'a': 'B', 'opts': [('A. 大于1', '不可能'), ('B. 小于1', '正确！有摩擦额外功'), ('C. 等于1', '不可能，理想情况接近1')]},
    {'q': '功的单位是？', 'a': 'B', 'opts': [('A. 瓦特', '这是功率单位'), ('B. 焦耳', '正确！'), ('C. 牛顿', '这是力单位')]},
]

# Replace remaining quiz blocks
offset = 0
replaced = 0
for start, end, quiz_section in quiz_blocks:
    if replaced >= len(extra_questions):
        break
    
    q_data = extra_questions[replaced]
    
    opts_html = ''
    for letter, (text, fb) in [('A', q_data['opts'][0]), ('B', q_data['opts'][1]), ('C', q_data['opts'][2])]:
        is_correct = letter == q_data['a']
        opts_html += f'<button class="quiz-option" onclick="checkQuiz(this, {str(is_correct).lower()}, \'{fb}\')">{letter}. {text}</button>\n'
    
    new_quiz = f'''<h3>🎯 随堂测验 Q{replaced+1}</h3>
<div id="q_extra_{replaced+1}">
  <p><strong>Q{replaced+1}.</strong> {q_data['q']}</p>
  {opts_html}
  <div class="feedback" id="fb_extra_{replaced+1}"></div>
</div>'''
    
    actual_start = start + offset
    actual_end = end + offset
    content = content[:actual_start] + new_quiz + content[actual_end:]
    offset += len(new_quiz) - (end - start)
    replaced += 1

print(f'Replaced {replaced} more quizzes')

# Verify
ph = content.count('请根据本单元内容设计测试题')
print(f'Remaining placeholders: {ph}')

div_o = content.count('<div')
div_c = content.count('</div>')
print(f'Div: {div_o}/{div_c}')

with open('tutorial.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Saved!')
