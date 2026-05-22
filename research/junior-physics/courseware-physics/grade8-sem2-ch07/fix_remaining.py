import re

with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all quiz blocks that still have placeholders
# Pattern: h3 + div with quiz content containing placeholder
quiz_blocks = []
for m in re.finditer(r'<h3>🎯 随堂测验.*?</h3>', content):
    start = m.start()
    # Find the end of this quiz block - look for next h3 or </div class="btn-row"
    end = content.find('<h3>', start + 1)
    if end == -1:
        end = content.find('<div class="btn-row"', start)
    if end == -1:
        end = len(content)
    
    quiz_section = content[start:end]
    if '请根据本单元内容设计测试题' in quiz_section:
        quiz_blocks.append((start, end, quiz_section))

print(f'Found {len(quiz_blocks)} quiz blocks with placeholders')

# Simple replacement: replace all placeholders with actual questions
# We need 12 more questions
extra_questions = [
    # ch1 extra (if any)
    {'q': '关于浮力方向，正确的是？', 'a': 'B', 'opts': [('A. 与重力方向相同', '不对'), ('B. 竖直向上', '正确！'), ('C. 指向液体表面', '不对')]},
    {'q': '物体在水中受到的浮力与什么有关？', 'a': 'C', 'opts': [('A. 物体质量', '不是直接因素'), ('B. 物体密度', '不是直接因素'), ('C. 排开水的体积', '正确！F浮=ρgV排')]},
    # ch2 extra
    {'q': '将铁块和铝块浸没在水中，体积相同，浮力？', 'a': 'C', 'opts': [('A. 铁块大', '不对，V排相同'), ('B. 铝块大', '不对，V排相同'), ('C. 一样大', '正确！V排相同，F浮相同')]},
    {'q': '一个物体排开 2 kg 的水，受到的浮力约为？', 'a': 'B', 'opts': [('A. 2 N', '不对，G=mg=2×10=20N'), ('B. 20 N', '正确！F浮=G排=20N'), ('C. 0.2 N', '不对')]},
    # ch3 extra
    {'q': '把橡皮泥捏成小船后能浮在水面，是因为？', 'a': 'A', 'opts': [('A. 排开水的体积变大，浮力变大', '正确！'), ('B. 重力变小了', '不对'), ('C. 水的密度变大了', '不对')]},
    {'q': '鱼通过什么方式在水中上浮和下潜？', 'a': 'B', 'opts': [('A. 改变自身重力', '不是'), ('B. 改变鱼鳔体积', '正确！改变V排'), ('C. 改变水的密度', '不对')]},
    # ch4 extra
    {'q': '轮船的排水量是指？', 'a': 'B', 'opts': [('A. 轮船排开水的体积', '接近，但通常指质量'), ('B. 轮船满载时排开水的质量', '正确！'), ('C. 轮船自身的质量', '不对')]},
    {'q': '潜水艇在水面下潜行时，受到的浮力？', 'a': 'C', 'opts': [('A. 逐渐变大', '不对，V排不变'), ('B. 逐渐变小', '不对'), ('C. 不变', '正确！潜行时V排不变')]},
    # ch5 extra
    {'q': '一个物体在液体中悬浮，说明？', 'a': 'B', 'opts': [('A. ρ物<ρ液', '不对，这会上浮'), ('B. ρ物=ρ液', '正确！'), ('C. ρ物>ρ液', '不对，这会下沉')]},
    {'q': '用弹簧测力计测浮力的方法叫？', 'a': 'A', 'opts': [('A. 称重法', '正确！F浮=G-F拉'), ('B. 排水法', '这是测体积的方法'), ('C. 平衡法', '不对')]},
    # ch6 extra
    {'q': '浮力产生的原因是？', 'a': 'C', 'opts': [('A. 液体对物体的吸引力', '不对'), ('B. 物体的重力', '不对'), ('C. 液体对物体上下表面的压力差', '正确！')]},
    {'q': '一艘轮船从长江驶入东海，浮力会？', 'a': 'B', 'opts': [('A. 变大', '不对，始终漂浮F浮=G'), ('B. 不变', '正确！重力不变'), ('C. 变小', '不对')]},
]

# Replace each remaining quiz block
offset = 0
replaced = 0
for start, end, quiz_section in quiz_blocks:
    if replaced >= len(extra_questions):
        break
    
    q_data = extra_questions[replaced]
    
    # Build new quiz HTML
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
    
    # Replace
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
