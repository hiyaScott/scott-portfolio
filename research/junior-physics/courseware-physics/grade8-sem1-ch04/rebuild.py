import re

# Read the old ch04 file
with open('tutorial.html', 'r') as f:
    old = f.read()

# ========== EXTRACT REAL CONTENT FROM EACH SECTION ==========

def extract_section(content, section_num):
    """Extract a section by number"""
    if section_num < 5:
        start = content.find(f'<!-- ========== Section {section_num}:')
        end = content.find(f'<!-- ========== Section {section_num+1}:')
    else:
        start = content.find(f'<!-- ========== Section {section_num}:')
        end = len(content)
    return content[start:end]

s1 = extract_section(old, 1)
s2 = extract_section(old, 2)
s3 = extract_section(old, 3)
s4 = extract_section(old, 4)
s5 = extract_section(old, 5)

# Extract highlights (concept boxes)
def get_highlights(section):
    return re.findall(r'<div class="highlight"[^>]*>(.+?)</div>', section, re.DOTALL)

# Extract formula boxes
def get_formulas(section):
    return re.findall(r'<div class="formula-box"[^>]*>(.+?)</div>', section, re.DOTALL)

# Extract demo boxes (canvas + slider + buttons)
def get_demos(section):
    return re.findall(r'<div class="demo-box"[^>]*>(.+?)</div>\s*</div>', section, re.DOTALL)

# Extract quiz blocks that are NOT placeholders
def get_real_quizzes(section):
    quizzes = []
    for m in re.finditer(r'<div id="q\d+"[^>]*>(.+?)</div>\s*</div>', section, re.DOTALL):
        quiz = m.group(0)
        if '请根据本单元内容设计测试题' not in quiz:
            quizzes.append(quiz)
    return quizzes

# Extract example-item blocks (skip template residue with "例题 N")
def get_examples(section):
    items = []
    for m in re.finditer(r'<div class="example-item"[^>]*>(.+?)</div>\s*</div>', section, re.DOTALL):
        item = m.group(0)
        if '例题 N：' in item:
            continue
        items.append(item)
    return items

# Extract paragraph text that looks like example solutions
def get_example_texts(section):
    """Extract <h3>✏️ 例题</h3> followed by highlight and p"""
    texts = []
    for m in re.finditer(r'<h3>✏️ 例题 \d+</h3>\s*(<div class="highlight"[^>]*>.+?</div>)\s*<p><strong>解：</strong>(.+?)</p>', section, re.DOTALL):
        texts.append((m.group(1), m.group(2)))
    return texts

h1 = get_highlights(s1)
h2 = get_highlights(s2)
h3 = get_highlights(s3)
h4 = get_highlights(s4)
h5 = get_highlights(s5)

f1 = get_formulas(s1)
f2 = get_formulas(s2)
f3 = get_formulas(s3)
f4 = get_formulas(s4)
f5 = get_formulas(s5)

d1 = get_demos(s1)
d2 = get_demos(s2)
d3 = get_demos(s3)
d4 = get_demos(s4)

q1 = get_real_quizzes(s1)
q2 = get_real_quizzes(s2)
q3 = get_real_quizzes(s3)
q4 = get_real_quizzes(s4)

ex1 = get_examples(s1)
ex2 = get_examples(s2)
ex3 = get_examples(s3)
ex4 = get_examples(s4)

print(f"S1: {len(h1)} highlights, {len(f1)} formulas, {len(d1)} demos, {len(q1)} quizzes, {len(ex1)} examples")
print(f"S2: {len(h2)} highlights, {len(f2)} formulas, {len(d2)} demos, {len(q2)} quizzes, {len(ex2)} examples")
print(f"S3: {len(h3)} highlights, {len(f3)} formulas, {len(d3)} demos, {len(q3)} quizzes, {len(ex3)} examples")
print(f"S4: {len(h4)} highlights, {len(f4)} formulas, {len(d4)} demos, {len(q4)} quizzes, {len(ex4)} examples")
print(f"S5: {len(h5)} highlights, {len(f5)} formulas")

# Extract real quiz questions and answers from checkQ* functions
def extract_quiz_details(section, func_prefix):
    """Extract quiz question text and correct answer from a section"""
    # Find the quiz block
    for m in re.finditer(rf'<div id="{func_prefix}"[^>]*>(.+?)</div>\s*</div>', section, re.DOTALL):
        quiz_html = m.group(0)
        # Extract question text
        q_text = re.search(r'<p><strong>Q\d+\.</strong>\s*(.+?)</p>', quiz_html)
        question = q_text.group(1) if q_text else ''
        
        # Extract options
        options = re.findall(r'<button[^>]*>(.+?)</button>', quiz_html)
        
        # Extract correct answer from the onclick
        correct = re.search(rf"checkQ\d+\(this,'([ABC])'\)", quiz_html)
        correct_ans = correct.group(1) if correct else 'A'
        
        return question, options, correct_ans
    return '', [], 'A'

# Extract all quiz details
quiz_data = []
for i, (section, prefix) in enumerate([(s1, 'q1'), (s2, 'q2'), (s3, 'q3'), (s4, 'q4')]):
    q, opts, ans = extract_quiz_details(section, prefix)
    quiz_data.append((q, opts, ans))
    print(f"\nQuiz {i+1}: {q[:60]}...")
    print(f"  Options: {len(opts)}")
    print(f"  Correct: {ans}")

# Extract JS functions for canvas interactions
def extract_js_function(content, func_name):
    """Extract a complete JS function by name"""
    pattern = rf'function\s+{func_name}\s*\([^)]*\)\s*\{{'
    m = re.search(pattern, content)
    if not m:
        return ''
    start = m.start()
    # Find matching brace
    brace_count = 0
    i = content.find('{', start)
    if i == -1:
        return ''
    brace_count = 1
    i += 1
    while i < len(content) and brace_count > 0:
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
        i += 1
    return content[start:i]

# Extract IIFE canvas scripts
def extract_iife_by_canvas(content, canvas_id):
    """Extract IIFE that references a specific canvas"""
    for m in re.finditer(r'\(function\(\)\{.*?\}\)\(\);', content, re.DOTALL):
        iife = m.group(0)
        if canvas_id in iife:
            return iife
    return ''

js_funcs = {}
func_names = ['drawShadow', 'setEclipse', 'drawEclipse', 'setReflect', 'drawReflect', 'drawMirror', 'setMedium', 'drawRefract', 'drawPrism', 'drawLens']
for name in func_names:
    js_funcs[name] = extract_js_function(old, name)

# Extract IIFE scripts for reflectLawCanvas and lensCanvas (duplicate IDs)
iife_reflectlaw = extract_iife_by_canvas(old, 'reflectLawCanvas')
iife_lens = extract_iife_by_canvas(old, 'lensCanvas')

print(f"\nJS functions extracted: {[k for k,v in js_funcs.items() if v]}")
print(f"IIFE reflectLaw: {'YES' if iife_reflectlaw else 'NO'}")
print(f"IIFE lens: {'YES' if iife_lens else 'NO'}")

# ========== BUILD NEW HTML ==========

# CSS - use template base with optical theme colors (yellow/orange)
css = '''<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

:root {
  --bg: #06080f;
  --panel: rgba(10, 14, 26, 0.9);
  --accent: #fcee0a;
  --accent2: #ff6b35;
  --danger: #ef476f;
  --warning: #ffd166;
  --success: #06d6a0;
  --grid: rgba(252, 238, 10, 0.08);
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

/* Scanlines */
body::before {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 4px);
  pointer-events: none;
  z-index: 5;
}

/* HUD Grid */
#hud-grid {
  position: fixed; inset: 0;
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 1;
}

/* Corners */
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
  display: flex; gap: 8px;
  margin-bottom: 32px;
  justify-content: center;
}
.progress-seg {
  width: 80px; height: 4px;
  background: rgba(88,96,112,0.3);
  border-radius: 2px;
  transition: all 0.3s;
}
.progress-seg.active { background: var(--accent); box-shadow: 0 0 10px var(--accent); }
.progress-seg.done { background: var(--success); }

.card {
  background: var(--panel);
  border: 1px solid rgba(252,238,10,0.2);
  border-radius: 8px;
  padding: 28px;
  margin-bottom: 20px;
  position: relative;
}
.card-header {
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(252,238,10,0.15);
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
  background: rgba(252,238,10,0.05);
  border: 1px solid rgba(252,238,10,0.2);
  border-radius: 6px;
  padding: 12px 16px;
  margin: 12px 0;
  font-size: 16px;
  color: var(--accent);
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  text-shadow: 0 0 10px rgba(252,238,10,0.3);
}

.example-list { margin: 20px 0; }
.example-item {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(252,238,10,0.15);
  border-radius: 6px;
  margin-bottom: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s;
}
.example-item:hover { border-color: rgba(252,238,10,0.3); }
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
  border-top: 1px solid rgba(252,238,10,0.1);
}
.example-item .step {
  margin-top: 8px;
  padding: 8px 12px;
  background: rgba(252,238,10,0.05);
  border-left: 2px solid var(--accent);
  border-radius: 0 4px 4px 0;
  font-size: 12px;
  color: var(--text-dim);
}

.quiz-box {
  background: rgba(0,0,0,0.3);
  border: 1px solid rgba(252,238,10,0.15);
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
  border: 1px solid rgba(252,238,10,0.2);
  color: var(--text);
  padding: 12px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  font-size: 14px;
}
.quiz-btn:hover { border-color: var(--accent); background: rgba(252,238,10,0.05); }
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
  border: 1px solid rgba(252,238,10,0.15);
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
.btn-ghost:hover { background: rgba(252,238,10,0.1); }
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

/* Slider controls */
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

/* Old demo-box style for canvas areas */
.demo-box {
  background: rgba(0,0,0,0.3);
  border: 1px dashed rgba(252,238,10,0.3);
  border-radius: 8px;
  padding: 20px;
  margin: 16px 0;
  text-align: center;
}

/* Formula box for old style */
.formula-box {
  background: rgba(6,8,15,0.8);
  border: 1px solid var(--accent);
  border-radius: 6px;
  padding: 16px;
  margin: 16px 0;
  text-align: center;
  font-size: 16px;
  color: var(--accent);
  text-shadow: 0 0 10px rgba(252,238,10,0.3);
}

/* Quiz option old style compatibility */
.quiz-option {
  display: block;
  width: 100%;
  text-align: left;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(252,238,10,0.2);
  color: var(--text);
  padding: 12px 16px;
  margin: 8px 0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: inherit;
  font-size: 14px;
}
.quiz-option:hover { border-color: var(--accent); background: rgba(252,238,10,0.05); }
.quiz-option.correct { border-color: var(--success); background: rgba(6,214,160,0.1); }
.quiz-option.wrong { border-color: var(--danger); background: rgba(239,71,111,0.1); }

/* Feedback old style compatibility */
.feedback {
  padding: 12px;
  border-radius: 6px;
  margin-top: 12px;
  font-size: 14px;
  display: none;
}
.feedback.ok { background: rgba(6,214,160,0.1); border: 1px solid var(--success); color: var(--success); display: block; }
.feedback.wrong { background: rgba(239,71,111,0.1); border: 1px solid var(--danger); color: var(--danger); display: block; }

/* Navigation old style compatibility */
.nav-bottom {
  position: fixed;
  bottom: 0; left: 0; right: 0;
  background: rgba(6,8,15,0.95);
  border-top: 1px solid var(--accent);
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
  backdrop-filter: blur(10px);
}
.nav-bottom a {
  color: var(--accent);
  text-decoration: none;
  font-size: 14px;
}
.nav-bottom .enter-game {
  background: var(--accent);
  color: #000;
  padding: 8px 20px;
  border-radius: 4px;
  text-decoration: none;
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
}

canvas { max-width: 100%; border-radius: 6px; display: block; margin: 0 auto; }

@media (max-width: 768px) {
  .title-bar h1 { font-size: 22px; }
  .card { padding: 18px; }
  .progress-seg { width: 50px; }
  .nav-bottom { flex-direction: column; gap: 8px; padding: 10px 16px; }
}
@media (max-width: 480px) {
  .title-bar h1 { font-size: 18px; letter-spacing: 2px; }
  .card { padding: 14px; }
  .card-header h2 { font-size: 16px; }
  .progress-seg { width: 36px; }
}
</style>'''

# ========== UNIT CONTENT ==========

# UNIT 1: 光的直线传播
unit1 = '''<div class="card" id="ch1">
  <div class="card-header">
    <h2>🔦 光的直线传播</h2>
    <span class="chapter-num">第 1 / 5 节</span>
  </div>

  <div class="concept-box">
    <div class="label">核心概念</div>
    <p>光在<strong>同种均匀介质</strong>中沿直线传播。这是光学实验室行动的第一法则——路径最短，速度最快。</p>
    <div class="formula">光速 c = 3 × 10⁸ m/s = 300,000 km/s</div>
    <p>光从太阳到地球只需约 <strong>8 分钟</strong>。</p>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">📐 影子形成原理</div>
    <p style="font-size:13px;color:var(--text-dim);margin-bottom:12px;">当光遇到不透明物体时，被阻挡的区域形成<strong>影子</strong>。影子的大小与光源位置和物体位置有关。</p>
    <div class="demo-box">
      <canvas id="shadowCanvas" width="600" height="250"></canvas>
      <div class="slider-control">
        <label>太阳高度角</label>
        <input type="range" id="sunAngle" min="10" max="80" value="45">
        <span class="value" id="sunAngleVal">45°</span>
      </div>
      <p style="font-size:12px;color:var(--text-dim);margin-top:8px">拖动滑块改变太阳角度，观察影子长度变化</p>
    </div>
  </div>

  <div class="anim-area">
    <div style="font-size:16px;margin-bottom:12px;">🌑 日食与月食</div>
    <div class="demo-box">
      <canvas id="eclipseCanvas" width="600" height="200"></canvas>
      <div style="margin-top:10px">
        <button class="btn" onclick="setEclipse('solar')">☀️ 日食</button>
        <button class="btn btn-ghost" onclick="setEclipse('lunar')">🌙 月食</button>
      </div>
    </div>
    <p style="font-size:13px;color:var(--text-dim);margin-top:8px;">
      <strong>日食</strong>：月球运行到太阳和地球之间，月球的影子落在地球上。<br>
      <strong>月食</strong>：地球运行到太阳和月球之间，地球的影子落在月球上。
    </p>
  </div>

  <div class="example-list">
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 1：一棵树高 3m，太阳光与地面成 30° 角，求树影长度。</div>
      <div class="a">
        <strong>解：</strong>tan 30° = 树高 / 影长 → 影长 = 3 / tan 30° ≈ 3 / 0.577 ≈ <strong style="color:var(--success)">5.2 m</strong>
        <div class="step">利用直角三角形的三角函数关系，tan = 对边/邻边</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 2：太阳光与地面成 60° 角，一棵树的影长为 5 m，求树高。</div>
      <div class="a">
        <strong>解：</strong>tan 60° = 树高 / 影长 = h / 5<br>
        h = 5 × tan 60° = 5 × 1.732 ≈ <strong style="color:var(--success)">8.66 m</strong>
        <div class="step">利用直角三角形的三角函数关系</div>
      </div>
    </div>
    <div class="example-item" onclick="this.classList.toggle('expanded')">
      <div class="q">📌 例题 3：小明身高 1.6 m，站在路灯下，路灯高 4 m，小明距离路灯底部 3 m，求小明影子的长度。</div>
      <div class="a">
        <strong>解：</strong>设影长为 x。利用相似三角形：<br>
        4 / (3+x) = 1.6 / x<br>
        4x = 1.6(3+x) → 4x = 4.8 + 1.6x → 2.4x = 4.8 → x = <strong style="color:var(--success)">2 m</strong>
        <div class="step">路灯-地面-影子形成大三角形，人-地面-影子形成小三角形，两者相似</div>
      </div>
    </div>
  </div>

  <div class="quiz-box" id="ch1-quiz">
    <div class="quiz-title">🎯 随堂测验 — 光的直线传播</div>
    <div class="quiz-question"><strong>Q1.</strong> 光在真空中的传播速度约为？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！光速 c = 3×10⁸ m/s，是宇宙极限速度。')">A. 3 × 10⁸ m/s</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。340 m/s 是空气中的声速，不是光速。')">B. 340 m/s</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。3×10⁵ m/s 太小，应该是 3×10⁸ m/s。')">C. 3 × 10⁵ m/s</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb1"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q2.</strong> 下列现象中，不能用光的直线传播解释的是？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。影子就是光被物体阻挡形成的，是直线传播的结果。')">A. 影子的形成</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。日食是月球挡住太阳光，是直线传播的结果。')">B. 日食</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！彩虹是光的折射和色散形成的，不是直线传播。')">C. 彩虹</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb2"></div>

    <div class="quiz-question" style="margin-top:16px;"><strong>Q3.</strong> 太阳光与地面成 45° 角，一根 2m 高的电线杆影长约为？</div>
    <div class="quiz-options">
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。tan 45° = 1，影长 = 2 / 1 = 2m。')">A. 1 m</button>
      <button class="quiz-btn" onclick="checkQuiz(this, true, '正确！tan 45° = 1，影长 = 2÷1 = 2m。')">B. 2 m</button>
      <button class="quiz-btn" onclick="checkQuiz(this, false, '不对。tan 45° = 1，不是 0.5。')">C. 4 m</button>
    </div>
    <div class="quiz-feedback" id="ch1-fb3"></div>
  </div>

  <div class="btn-row">
    <button class="btn" onclick="goTo(2)">下一单元 →</button>
  </div>
</div>'''

# Continue with other units and JS... (will be appended)
print("Part 1 generated")
print(f"CSS length: {len(css)} bytes")
print(f"Unit 1 length: {len(unit1)} bytes")
