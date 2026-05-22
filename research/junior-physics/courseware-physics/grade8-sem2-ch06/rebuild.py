import re

# Read original file
with open('tutorial.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract each h2 section
titles = []
pos = 0
while True:
    h = content.find('<h2>', pos)
    if h == -1: break
    h_end = content.find('</h2>', h)
    titles.append((content[h+4:h_end], h, h_end))
    pos = h_end + 1

print(f'Found {len(titles)} h2 titles: {[t[0] for t in titles]}')

# Extract body content for each section
units = []
for i, (title, start, h2_end) in enumerate(titles):
    if i + 1 < len(titles):
        end = titles[i+1][1]
    else:
        end = content.find('</body>', start)
    
    section = content[start:end]
    body_start = section.find('</h2>') + 6
    body = section[body_start:].strip()
    
    # Remove old quiz placeholders
    body = re.sub(r'<h3>.*?随堂测验.*?</h3>\s*<div id="q[\d_]+".*?</div>\s*</div>\s*<div class="feedback" id="fb-[\d_]+"\s*></div>\s*</div>', '', body, flags=re.DOTALL)
    body = re.sub(r'<h3>.*?随堂测验.*?</h3>\s*<div id="q[\d_]+".*?</div>\s*</div>', '', body, flags=re.DOTALL)
    
    units.append({
        'title': title,
        'body': body
    })
    print(f'  {title}: body={len(body)} bytes')

# Now rebuild the full HTML
print('\nRebuilding...')

# CSS
CSS = '''<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
  --bg: #06080f;
  --panel: rgba(10, 14, 26, 0.9);
  --accent: #00f5d4;
  --accent2: #00bbf9;
  --danger: #ef476f;
  --warning: #ffd166;
  --success: #06d6a0;
  --grid: rgba(0, 245, 212, 0.08);
  --text: #c0c8d8;
  --text-dim: #586070;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

body::before {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
  pointer-events: none;
  z-index: 5;
}

#hud-grid {
  position: fixed; inset: 0;
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 1;
}

.corner-tl, .corner-tr, .corner-bl, .corner-br {
  position: fixed; width: 80px; height: 80px; z-index: 2; pointer-events: none;
}
.corner-tl { top: 10px; left: 10px; border-top: 2px solid var(--accent); border-left: 2px solid var(--accent); }
.corner-tr { top: 10px; right: 10px; border-top: 2px solid var(--accent); border-right: 2px solid var(--accent); }
.corner-bl { bottom: 10px; left: 10px; border-bottom: 2px solid var(--accent); border-left: 2px solid var(--accent); }
.corner-br { bottom: 10px; right: 10px; border-bottom: 2px solid var(--accent); border-right: 2px solid var(--accent); }

#app { position: relative; z-index: 10; max-width: 900px; margin: 0 auto; padding: 40px 20px; }

.title-bar {
  text-align: center;
  border-bottom: 1px solid var(--accent);
  padding-bottom: 16px;
  margin-bottom: 24px;
}
.title-bar h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: 32px; letter-spacing: 4px;
  color: var(--accent);
  text-shadow: 0 0 20px var(--accent), 0 0 40px var(--accent);
}
.title-bar .subtitle {
  font-size: 14px; color: var(--text-dim);
  margin-top: 8px; letter-spacing: 2px;
}

.progress-bar {
  display: flex; gap: 6px;
  margin-bottom: 32px;
  justify-content: center;
}
.progress-seg {
  width: 60px; height: 4px;
  background: rgba(88,96,112,0.3);
  border-radius: 2px;
  transition: all 0.3s;
}
.progress-seg.active { background: var(--accent); box-shadow: 0 0 10px var(--accent); }
.progress-seg.done { background: var(--success); }

.card {
  background: var(--panel);
  border: 1px solid rgba(0,245,212,0.2);
  border-radius: 8px;
  padding: 28px;
  margin-bottom: 20px;
  position: relative;
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(0,245,212,0.15);
  padding-bottom: 12px; margin-bottom: 16px;
}
.card-header h2 {
  font-family: 'Orbitron', sans-serif;
  font-size: 20px; color: var(--accent); margin: 0;
}
.chapter-num { font-size: 13px; color: var(--text-dim); letter-spacing: 1px; }
.card.hidden { display: none; }

.concept-box {
  background: rgba(6,8,15,0.6);
  border-left: 3px solid var(--accent);
  border-radius: 0 8px 8px 0;
  padding: 16px;
  margin: 16px 0;
}
.concept-box .label {
  font-size: 11px; color: var(--accent);
  text-transform: uppercase; letter-spacing: 2px;
  margin-bottom: 8px; font-family: 'Orbitron', sans-serif;
}
.concept-box p { margin: 8px 0; line-height: 1.7; }

.formula {
  background: rgba(0,245,212,0.05);
  border: 1px solid rgba(0,245,212,0.2);
  border-radius: 6px;
  padding: 12px 16px;
  margin: 12px 0;
  font-size: 16px;
  color: var(--accent);
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 10px rgba(0,245,212,0.3);
}

.example-list { margin: 20px 0; }
.example-item {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(0,245,212,0.15);
  border-radius: 6px;
  margin-bottom: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}
.example-item:hover { border-color: rgba(0,245,212,0.3); }
.example-item .q {
  padding: 12px 16px;
  font-size: 14px;
  display: flex; align-items: center; gap: 8px;
}
.example-item .a {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, padding 0.3s ease;
  padding: 0 16px;
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-dim);
}
.example-item.expanded .a {
  max-height: 500px;
  padding: 12px 16px 16px;
  border-top: 1px solid rgba(0,245,212,0.1);
}
.example-item .step {
  margin-top: 8px;
  padding: 8px 12px;
  background: rgba(0,245,212,0.05);
  border-left: 2px solid var(--accent);
  border-radius: 0 4px 4px 0;
  font-size: 12px;
  color: var(--text-dim);
}

.quiz-box {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(0,245,212,0.15);
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
}
.quiz-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  color: var(--accent);
  margin-bottom: 16px;
  letter-spacing: 1px;
}
.quiz-question { margin-bottom: 12px; font-size: 14px; line-height: 1.6; }
.quiz-options { display: flex; flex-direction: column; gap: 8px; }
.quiz-btn {
  text-align: left;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(0,245,212,0.2);
  color: var(--text);
  padding: 12px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  font-size: 14px;
}
.quiz-btn:hover { border-color: var(--accent); background: rgba(0,245,212,0.05); }
.quiz-btn.correct { border-color: var(--success); background: rgba(6,214,160,0.1); }
.quiz-btn.wrong { border-color: var(--danger); background: rgba(239,71,111,0.1); }
.quiz-btn:disabled { opacity: 0.6; cursor: default; }
.quiz-feedback {
  margin-top: 12px;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  min-height: 20px;
}

.anim-area {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(0,245,212,0.15);
  border-radius: 8px;
  padding: 20px;
  margin: 16px 0;
}

.btn {
  background: var(--accent);
  color: #000;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  margin: 4px;
  text-decoration: none;
  display: inline-block;
}
.btn:hover { box-shadow: 0 0 20px var(--accent); transform: translateY(-1px); }
.btn-ghost {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
}
.btn-ghost:hover { background: rgba(0,245,212,0.1); }
.btn-warn {
  background: rgba(255,209,102,0.1);
  border: 1px solid var(--warning);
  color: var(--warning);
}
.btn-warn:hover { background: rgba(255,209,102,0.2); box-shadow: 0 0 20px var(--warning); }

.btn-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  gap: 12px;
}

.footer-note {
  text-align: center;
  padding: 20px 0;
  color: var(--text-dim);
  font-size: 12px;
  letter-spacing: 1px;
}

.demo-box {
  background: rgba(0,0,0,0.3);
  border: 1px dashed rgba(0,245,212,0.3);
  border-radius: 8px;
  padding: 20px;
  margin: 16px 0;
  text-align: center;
}

.slider-control {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 0;
}
.slider-control input[type="range"] {
  flex: 1;
  accent-color: var(--accent);
}
.slider-control label {
  min-width: 100px;
  font-size: 14px;
}
.slider-control .value {
  min-width: 60px;
  text-align: right;
  color: var(--accent);
}

canvas { max-width: 100%; border-radius: 6px; display: block; margin: 0 auto; }

@media (max-width: 768px) {
  .title-bar h1 { font-size: 22px; }
  .card { padding: 18px; }
  .progress-seg { width: 50px; }
}
@media (max-width: 480px) {
  .title-bar h1 { font-size: 18px; letter-spacing: 2px; }
  .card { padding: 14px; }
  .card-header h2 { font-size: 16px; }
  .progress-seg { width: 36px; }
}
</style>'''

# Quiz data
quiz_data = {
    0: [
        {'q': '密度的国际单位是？', 'opts': [('A. kg/m³', True, '正确！'), ('B. g/cm³', False, '常用但非国际基本单位'), ('C. kg/m²', False, '这是面密度')]},
        {'q': '压强的定义是？', 'opts': [('A. F/S', True, '正确！'), ('B. F×S', False, '不对'), ('C. S/F', False, '反了')]},
        {'q': '液体压强公式是？', 'opts': [('A. ρgh', True, '正确！'), ('B. ρg/V', False, '不对'), ('C. ρVg', False, '这是浮力')]},
    ],
    1: [
        {'q': '质量 540g，体积 200cm³，密度是？', 'opts': [('A. 0.37', False, '算错了'), ('B. 2.7 g/cm³', True, '正确！540/200=2.7'), ('C. 108', False, '算错了')]},
        {'q': '水结冰后不变的是？', 'opts': [('A. 体积', False, '变大'), ('B. 密度', False, '变小'), ('C. 质量', True, '正确！')]},
        {'q': '1 g/cm³ = ? kg/m³', 'opts': [('A. 1', False, '少了'), ('B. 100', False, '少了'), ('C. 1000', True, '正确！')]},
    ],
    2: [
        {'q': '600N 的人，双脚面积 0.04m²，压强？', 'opts': [('A. 15', False, '单位错了'), ('B. 1500', False, '少了一个0'), ('C. 15000 Pa', True, '正确！')]},
        {'q': '增大压强的是？', 'opts': [('A. 坦克履带', False, '减小'), ('B. 刀刃磨薄', True, '正确！'), ('C. 宽带书包', False, '减小')]},
        {'q': '砖块怎么放压强最大？', 'opts': [('A. 平放', False, '面积最大'), ('B. 侧放', False, '中等'), ('C. 竖放', True, '正确！面积最小')]},
    ],
    3: [
        {'q': '20m 深海，海水压强约？', 'opts': [('A. 2060', False, '单位不对'), ('B. 20600', False, '单位不对'), ('C. 2.06×10⁵ Pa', True, '正确！')]},
        {'q': '同一深度液体压强特点？', 'opts': [('A. 与容器有关', False, '无关'), ('B. 各方向相等', True, '正确！'), ('C. 与总质量有关', False, '无关')]},
        {'q': '哪个孔喷水最远？', 'opts': [('A. 最上面', False, '压强小'), ('B. 中间', False, '中等'), ('C. 最下面', True, '正确！深度最大')]},
    ],
    4: [
        {'q': '标准大气压约？', 'opts': [('A. 1.01×10³', False, '指数错了'), ('B. 1.01×10⁵ Pa', True, '正确！'), ('C. 10.1', False, '差太多')]},
        {'q': '吸管吸饮料的原理？', 'opts': [('A. 嘴吸力', False, '不是'), ('B. 大气压', True, '正确！'), ('C. 自己流', False, '不是')]},
        {'q': '托里拆利管倾斜，水银柱高度？', 'opts': [('A. 变大', False, '不变'), ('B. 不变', True, '正确！'), ('C. 变小', False, '不变')]},
    ],
    5: [
        {'q': '2×10⁻³ m³ 浸没在水中，浮力？', 'opts': [('A. 2N', False, '少了'), ('B. 20N', True, '正确！'), ('C. 0.2N', False, '少了')]},
        {'q': '同木块放水/酒精，浮力？', 'opts': [('A. 水中大', False, '漂浮都等于G'), ('B. 一样大', True, '正确！'), ('C. 酒精大', False, '漂浮都等于G')]},
        {'q': '潜水艇浮沉方式？', 'opts': [('A. 改变重力', True, '正确！'), ('B. 改变V排', False, '不是'), ('C. 改变水密度', False, '不是')]},
    ],
    6: [
        {'q': '水中下沉的物体密度？', 'opts': [('A. ρ物<ρ水', False, '会上浮'), ('B. ρ物>ρ水', True, '正确！'), ('C. ρ物=ρ水', False, '会悬浮')]},
        {'q': '空气中10N，水中6N，浮力？', 'opts': [('A. 16N', False, '加法错了'), ('B. 4N', True, '正确！10-6=4'), ('C. 6N', False, '取错数')]},
        {'q': '同物体浸没水和煤油，浮力？', 'opts': [('A. 水中大', True, '正确！ρ大浮力大'), ('B. 一样', False, 'ρ不同'), ('C. 煤油大', False, 'ρ小')]},
    ],
}

# Build quiz HTML
def build_quiz(unit_idx, q_idx, q_data):
    opts_html = ''
    for letter, text, is_correct, fb in [('A', q_data['opts'][0][0], q_data['opts'][0][1], q_data['opts'][0][2]),
                                           ('B', q_data['opts'][1][0], q_data['opts'][1][1], q_data['opts'][1][2]),
                                           ('C', q_data['opts'][2][0], q_data['opts'][2][1], q_data['opts'][2][2])]:
        opts_html += f'<button class="quiz-btn" onclick="checkQuiz(this, {str(is_correct).lower()}, \'{fb}\')">{letter}. {text}</button>\n'
    
    return f'''<div class="quiz-box" id="ch{unit_idx}-quiz">
    <div class="quiz-title">🎯 随堂测验</div>
    <div class="quiz-question"><strong>Q{q_idx}.</strong> {q_data['q']}</div>
    <div class="quiz-options">
      {opts_html}
    </div>
    <div class="quiz-feedback" id="ch{unit_idx}-fb{q_idx}"></div>
  </div>'''

# Process each unit
unit_htmls = []
for i, unit in enumerate(units):
    title = unit['title']
    body = unit['body']
    
    # Build navigation
    if i == 0:
        nav = '<button class="btn" onclick="goTo(2)">下一单元 →</button>'
    elif i == len(units) - 1:
        nav = f'<button class="btn btn-ghost" onclick="goTo({i})">← 上一单元</button>\n    <a class="btn btn-warn" href="game.html">🎮 挑战模式 →</a>'
    else:
        nav = f'<button class="btn btn-ghost" onclick="goTo({i})">← 上一单元</button>\n    <button class="btn" onclick="goTo({i+2})">下一单元 →</button>'
    
    # Add quiz
    quizzes = quiz_data.get(i, [])
    quiz_html = ''
    for qi, q in enumerate(quizzes, 1):
        quiz_html += build_quiz(i+1, qi, q) + '\n'
    
    unit_html = f'''<div class="card" id="ch{i+1}">
  <div class="card-header">
    <h2>{title}</h2>
    <span class="chapter-num">第 {i+1} / {len(units)} 节</span>
  </div>
{body}
  {quiz_html}
  <div class="btn-row">
    {nav}
  </div>
</div>'''
    
    unit_htmls.append(unit_html)

# Build progress bar
progress_segs = '\n'.join([f'    <div class="progress-seg" data-idx="{j+1}"></div>' for j in range(len(units))])

# Assemble full HTML
html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>密度与压强分析中心 · 学习手册</title>
{CSS}
</head>
<body>
<div id="hud-grid"></div>
<div class="corner-tl"></div>
<div class="corner-tr"></div>
<div class="corner-bl"></div>
<div class="corner-br"></div>

<div id="app">
  <div class="title-bar">
    <h1>⚖️ 密度与压强分析中心</h1>
    <div class="subtitle">沪科版八年级物理 · 第6章 · 密度与压强</div>
  </div>
  
  <div class="progress-bar" id="progressBar">
    <div class="progress-seg active" data-idx="1"></div>
{progress_segs}
  </div>

{'\n'.join(unit_htmls)}

  <div class="footer-note">密度与压强分析中心 v1.0.0 · 物理基础实验室</div>
</div>

<script>
let currentCh = 1;
const totalCh = {len(units)};

function goTo(n) {{
  document.querySelectorAll('.card').forEach(c => c.classList.add('hidden'));
  const target = document.getElementById('ch' + n);
  if(target) {{ target.classList.remove('hidden'); target.scrollTop = 0; window.scrollTo(0,0); }}
  currentCh = n;
  updateProgress();
}}

function updateProgress() {{
  document.querySelectorAll('.progress-seg').forEach((seg, idx) => {{
    seg.classList.remove('active','done');
    if(idx + 1 < currentCh) seg.classList.add('done');
    else if(idx + 1 === currentCh) seg.classList.add('active');
  }});
}}

function checkQuiz(btn, isCorrect, msg) {{
  const box = btn.closest('.quiz-box');
  const fb = box.querySelector('.quiz-feedback');
  const opts = box.querySelectorAll('.quiz-btn');
  opts.forEach(o => {{ o.classList.remove('correct','wrong'); o.disabled = true; }});
  if(isCorrect) {{
    btn.classList.add('correct');
    if(fb) {{ fb.className = 'quiz-feedback ok'; fb.textContent = msg; }}
  }} else {{
    btn.classList.add('wrong');
    if(fb) {{ fb.className = 'quiz-feedback wrong'; fb.textContent = msg; }}
    opts.forEach(o => {{
      const onclick = o.getAttribute('onclick') || '';
      if(onclick.includes('checkQuiz(this, true')) {{
        o.classList.add('correct');
      }}
    }});
  }}
}}

document.addEventListener('DOMContentLoaded', function() {{
  updateProgress();
}});
</script>
</body>
</html>'''

# Validate
div_open = html.count('<div')
div_close = html.count('</div>')
print(f'Div: {div_open} open / {div_close} close')
print(f'Size: {len(html)} bytes')
print(f'Placeholder count: {html.count("请根据本单元内容设计测试题")}')

if div_open == div_close:
    with open('tutorial.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Wrote tutorial.html successfully!')
else:
    print(f'ERROR: div imbalance: {div_open - div_close}')
