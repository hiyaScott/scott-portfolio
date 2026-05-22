# Assemble ch05 complete HTML
import sys

# Read parts
exec(open('part1.py').read())
exec(open('part2.py').read())
exec(open('extracted_data.py').read())

# HTML header
html_head = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>力学分析中心 · 学习手册 — 力与运动</title>
''' + css + '''
</head>
<body>
<div id="hud-grid"></div>
<div class="corner-tl"></div>
<div class="corner-tr"></div>
<div class="corner-bl"></div>
<div class="corner-br"></div>

<div id="app">
  <div class="title-bar">
    <h1>💪 力学分析中心</h1>
    <div class="subtitle">沪科版八年级物理 · 第5章 · 力与运动</div>
  </div>
  
  <div class="progress-bar" id="progressBar">
    <div class="progress-seg active" data-idx="1"></div>
    <div class="progress-seg" data-idx="2"></div>
    <div class="progress-seg" data-idx="3"></div>
    <div class="progress-seg" data-idx="4"></div>
    <div class="progress-seg" data-idx="5"></div>
    <div class="progress-seg" data-idx="6"></div>
  </div>
'''

# JS template functions
js_template = '''
let currentCh = 1;
const totalCh = 6;

function goTo(n) {
  document.querySelectorAll('.card').forEach(c => c.classList.add('hidden'));
  const target = document.getElementById('ch' + n);
  if(target) { target.classList.remove('hidden'); target.scrollTop = 0; window.scrollTo(0,0); }
  currentCh = n;
  updateProgress();
}

function updateProgress() {
  document.querySelectorAll('.progress-seg').forEach((seg, idx) => {
    seg.classList.remove('active','done');
    if(idx + 1 < currentCh) seg.classList.add('done');
    else if(idx + 1 === currentCh) seg.classList.add('active');
  });
}

function checkQuiz(btn, isCorrect, msg) {
  const box = btn.closest('.quiz-box');
  const fb = box.querySelector('.quiz-feedback');
  const opts = box.querySelectorAll('.quiz-btn');
  opts.forEach(o => { o.classList.remove('correct','wrong'); o.disabled = true; });
  if(isCorrect) {
    btn.classList.add('correct');
    if(fb) { fb.className = 'quiz-feedback ok'; fb.textContent = msg; }
  } else {
    btn.classList.add('wrong');
    if(fb) { fb.className = 'quiz-feedback wrong'; fb.textContent = msg; }
    opts.forEach(o => {
      const onclick = o.getAttribute('onclick') || '';
      if(onclick.includes('checkQuiz(this, true') || onclick.includes("checkQuiz(this, true")) {
        o.classList.add('correct');
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
  updateProgress();
});
'''

# Extract JS body from js_funcs
js_body = ''
for name in ['drawMotion', 'setForceDemo', 'drawForce', 'drawGravity', 'drawSpring', 'setInertia', 'drawInertia', 'draw']:
    if name in js_funcs and js_funcs[name]:
        js_body += '\n' + js_funcs[name] + '\n'

html_foot = '''
  <div class="footer-note">力学分析中心 v1.0.0 · 物理基础实验室</div>
</div>

<script>
''' + js_body + js_template + '''
</script>
</body>
</html>
'''

# Assemble
full_html = html_head + '\n' + unit1 + '\n' + unit2 + '\n' + unit3 + '\n' + unit4 + '\n' + unit5 + '\n' + unit6 + '\n' + html_foot

# Validate
div_open = full_html.count('<div')
div_close = full_html.count('</div>')
print(f"Full HTML: {len(full_html)} bytes")
print(f"Div open: {div_open}, Div close: {div_close}")

if div_open != div_close:
    print(f"WARNING: div imbalance! Diff = {div_open - div_close}")
    sys.exit(1)

with open('tutorial.html', 'w') as f:
    f.write(full_html)

print("Wrote tutorial.html successfully!")
print(f"  checkQuiz calls: {full_html.count('checkQuiz(')}")
print(f"  goTo calls: {full_html.count('goTo(')}")
print(f"  Canvas elements: {full_html.count('<canvas')}")
print(f"  Example items: {full_html.count('class=\"example-item\"')}")
print(f"  Quiz questions: {full_html.count('class=\"quiz-question\"')}")
