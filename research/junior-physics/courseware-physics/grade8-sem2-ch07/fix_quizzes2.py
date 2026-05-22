import re

with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Quiz data for ch07 (6 units)
quiz_data = {
    'ch1': [  # 浮力基础
        {'q': '浸在液体中的物体受到的浮力方向是？', 'a': 'B', 'opts': [('A. 向下', '浮力方向始终竖直向上'), ('B. 竖直向上', '正确！浮力方向始终竖直向上。'), ('C. 与重力相反', '虽然常与重力相反，但准确说是竖直向上')]},
        {'q': '将石块浸入水中，弹簧测力计示数会？', 'a': 'B', 'opts': [('A. 变大', '不对，石块受到向上的浮力，示数应减小'), ('B. 变小', '正确！浮力向上托，测力计示数减小'), ('C. 不变', '不对，浸入液体后受到浮力')]},
        {'q': '同一物体浸没在水中和煤油中，浮力较大的是？', 'a': 'A', 'opts': [('A. 水中', '正确！水的密度大于煤油，V排相同，F浮=ρ液gV排，水中浮力大'), ('B. 煤油中', '不对，ρ水>ρ煤油'), ('C. 一样大', '不对，液体密度不同')]},
    ],
    'ch2': [  # 阿基米德原理
        {'q': '阿基米德原理的内容是？', 'a': 'B', 'opts': [('A. 浮力等于物体重力', '这是浮沉条件，不是阿基米德原理'), ('B. 浮力等于排开液体的重力', '正确！F浮=G排=ρ液gV排'), ('C. 浮力等于物体体积', '不对')]},
        {'q': '体积为 2×10⁻³ m³ 的铁球浸没在水中，受到的浮力是？', 'a': 'B', 'opts': [('A. 2 N', '不对，F浮=ρ水gV排=10³×10×2×10⁻³=20N'), ('B. 20 N', '正确！F浮=1.0×10³×10×2×10⁻³=20N'), ('C. 200 N', '不对')]},
        {'q': '物体排开的水重为 5 N，则物体受到的浮力为？', 'a': 'B', 'opts': [('A. 小于 5 N', '不对，阿基米德原理说浮力等于排开液体重力'), ('B. 5 N', '正确！F浮=G排=5N'), ('C. 大于 5 N', '不对')]},
    ],
    'ch3': [  # 浮沉条件
        {'q': '饺子煮熟后会浮起来，是因为？', 'a': 'B', 'opts': [('A. 质量变小了', '质量不变，是体积膨胀'), ('B. 体积变大，浮力变大', '正确！饺子内部气体膨胀，V排增大，浮力增大'), ('C. 重力变小了', '重力基本不变')]},
        {'q': '一个物体在水中下沉，说明它的密度与水的密度关系是？', 'a': 'B', 'opts': [('A. ρ物<ρ水', '不对，这会上浮'), ('B. ρ物>ρ水', '正确！物体密度大于液体密度时下沉'), ('C. ρ物=ρ水', '不对，这会悬浮')]},
        {'q': '潜水艇是通过改变什么来实现上浮和下潜的？', 'a': 'A', 'opts': [('A. 自身重力', '正确！通过充放水改变自身重力'), ('B. 排开水的体积', '不对，潜水艇体积不变'), ('C. 水的密度', '不对')]},
    ],
    'ch4': [  # 浮力应用
        {'q': '轮船从江河驶入大海，会？', 'a': 'B', 'opts': [('A. 沉下去一些', '不对，海水密度大，排开体积小'), ('B. 浮起来一些', '正确！ρ海水>ρ江水，F浮=G不变，V排减小'), ('C. 没有变化', '不对，液体密度变了')]},
        {'q': '密度计在不同液体中漂浮时，受到的浮力？', 'a': 'B', 'opts': [('A. 密度大的液体中浮力大', '不对，密度计始终漂浮，浮力都等于重力'), ('B. 都一样大', '正确！漂浮时F浮=G，密度计重力不变'), ('C. 密度小的液体中浮力大', '不对')]},
        {'q': '热气球上升的原理是？', 'a': 'A', 'opts': [('A. 加热后空气密度变小，浮力大于重力', '正确！热空气密度小于冷空气'), ('B. 加热后重力变小了', '不对，重力基本不变'), ('C. 热气球会自己飞', '不对')]},
    ],
    'ch5': [  # 综合练习
        {'q': '一个物体在空气中重 10 N，浸没在水中时测力计示数为 6 N，物体受到的浮力是？', 'a': 'B', 'opts': [('A. 16 N', '不对，10-6=4'), ('B. 4 N', '正确！F浮=G-F拉=10-6=4N'), ('C. 6 N', '不对')]},
        {'q': '木块在水中漂浮，铁块在水中下沉，比较它们受到的浮力？', 'a': 'C', 'opts': [('A. 木块浮力大', '不一定，要看V排'), ('B. 铁块浮力大', '不一定'), ('C. 无法确定，要看排开水的体积', '正确！F浮=ρgV排，要看V排')]},
        {'q': '把鸡蛋放入盐水中浮起来，逐渐加入清水，鸡蛋会？', 'a': 'B', 'opts': [('A. 继续浮着', '不对，液体密度减小'), ('B. 下沉', '正确！液体密度减小，当ρ液<ρ蛋时下沉'), ('C. 悬浮不动', '不对')]},
    ],
    'ch6': [  # 总结
        {'q': '关于浮力，下列说法正确的是？', 'a': 'B', 'opts': [('A. 浮力与物体浸没的深度有关', '不对，F浮=ρgV排，与深度无关'), ('B. 浮力与液体密度有关', '正确！F浮=ρ液gV排，ρ液越大浮力越大'), ('C. 浮力与物体密度有关', '不对，浮力与物体密度无关')]},
        {'q': '一个体积为 100 cm³ 的物体浸没在水中，受到的浮力是？', 'a': 'B', 'opts': [('A. 100 N', '不对，F浮=ρgV=10³×10×10⁻⁴=1N'), ('B. 1 N', '正确！100cm³=10⁻⁴m³，F浮=10³×10×10⁻⁴=1N'), ('C. 10 N', '不对')]},
        {'q': '物体浮沉的根本决定因素是？', 'a': 'C', 'opts': [('A. 物体的质量', '不是直接因素'), ('B. 物体的体积', '不是直接因素'), ('C. 物体与液体的密度关系', '正确！ρ物<ρ液上浮，ρ物>ρ液下沉')]},
    ],
}

# Find all quiz blocks and replace them
# Pattern: <h3>🎯 随堂测验 Qn</h3> + <div id="q_x_y"> ... </div>
quiz_pattern = r'<h3>🎯 随堂测验 Q\d+</h3>\s*<div id="q_\d+_\d+"\s*>(.*?</div>)\s*</div>'

# Find all matches
matches = list(re.finditer(quiz_pattern, content, re.DOTALL))
print(f'Found {len(matches)} quiz blocks')

# Group by card - need to determine which card each quiz belongs to
# Use position to determine card
for m in matches[:3]:
    print(f'  Pos {m.start()}: {m.group(0)[:100]}...')

# Since we can't easily group by card, let's just replace all quizzes sequentially
# We have 30 quizzes (6 units × 5 quizzes each)
all_quizzes = []
for card_id in ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6']:
    quizzes = quiz_data.get(card_id, [])
    all_quizzes.extend(quizzes)

print(f'Total quiz data: {len(all_quizzes)}')

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
    
    # Replace
    start = m.start() + offset
    end = m.end() + offset
    new_content = new_content[:start] + new_quiz + new_content[end:]
    offset += len(new_quiz) - (m.end() - m.start())
    replaced += 1

print(f'Replaced {replaced} quizzes')

# Check placeholders
ph = new_content.count('请根据本单元内容设计测试题')
print(f'Remaining placeholders: {ph}')

# Save
with open('tutorial.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Saved!')
