# Assemble complete ch04 HTML from parts
import sys

# Read CSS + Unit 1 from rebuild.py
with open('rebuild.py', 'r') as f:
    rebuild_py = f.read()

# Extract CSS and unit1 from rebuild.py
# CSS starts after "css = '''" and ends before "'''"
css_start = rebuild_py.find("css = '''")
css_end = rebuild_py.find("\n'''", css_start) + 4
# Actually need to find the triple-quoted string properly
# The CSS ends at the first ''' after the style tag
style_end = rebuild_py.find('</style>\n''\'', css_start)
if style_end == -1:
    style_end = rebuild_py.find("</style>'''", css_start)
css_str = rebuild_py[css_start + 9:style_end + 9]

# Extract unit1 - it starts after "unit1 = '''" 
unit1_start = rebuild_py.find("unit1 = '''")
# Find the end - it's before "# Continue with other units"
unit1_end = rebuild_py.find("# Continue with other units", unit1_start)
unit1_str = rebuild_py[unit1_start + 11:unit1_end].strip().rstrip("'\"")

# Read units 2-5
exec(open('units_data.py').read())
# Read JS functions
exec(open('js_funcs.py').read())

# Build HTML header
html_head = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>光学分析中心 · 学习手册 — 光</title>
<style>
''' + css_str + '''
</style>
</head>
<body>
<div id="hud-grid"></div>
<div class="corner-tl"></div>
<div class="corner-tr"></div>
<div class="corner-bl"></div>
<div class="corner-br"></div>

<div id="app">
  <div class="title-bar">
    <h1>🔦 光学分析中心</h1>
    <div class="subtitle">沪科版八年级物理 · 第4章 · 光的世界</div>
  </div>
  
  <div class="progress-bar" id="progressBar">
    <div class="progress-seg active" data-idx="1"></div>
    <div class="progress-seg" data-idx="2"></div>
    <div class="progress-seg" data-idx="3"></div>
    <div class="progress-seg" data-idx="4"></div>
    <div class="progress-seg" data-idx="5"></div>
  </div>
'''

# Build HTML footer with JS
# Extract JS functions from js_funcs dict
js_body = ''
for name in ['drawShadow', 'setEclipse', 'drawEclipse', 'setReflect', 'drawReflect', 'drawMirror', 'setMedium', 'drawRefract', 'drawPrism', 'drawLens']:
    if name in js_funcs and js_funcs[name]:
        js_body += '\n' + js_funcs[name] + '\n'

# Add IIFE blocks
if 'iife_reflectlaw' in js_funcs and js_funcs['iife_reflectlaw']:
    js_body += '\n' + js_funcs['iife_reflectlaw'] + '\n'
if 'iife_lens' in js_funcs and js_funcs['iife_lens']:
    js_body += '\n' + js_funcs['iife_lens'] + '\n'

# Add template functions
js_template = '''
let currentCh = 1;
const totalCh = 5;

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
    // Highlight correct answer
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

html_foot = '''
  <div class="footer-note">光学分析中心 v1.0.0 · 物理基础实验室</div>
</div>

<script>
''' + js_body + js_template + '''
</script>
</body>
</html>
'''

# Assemble full HTML
full_html = html_head + '\n' + unit1_str + '\n' + unit2 + '\n' + unit3 + '\n' + unit4 + '\n' + unit5 + '\n' + html_foot

# Count divs
div_open = full_html.count('<div')
div_close = full_html.count('</div>')

print(f"Full HTML: {len(full_html)} bytes")
print(f"Div open: {div_open}, Div close: {div_close}")

if div_open != div_close:
    print(f"WARNING: div imbalance! Diff = {div_open - div_close}")
    sys.exit(1)

# Write file
with open('tutorial.html', 'w') as f:
    f.write(full_html)

print("Wrote tutorial.html successfully!")

# Quick validation
print(f"\nValidation:")
print(f"  checkQuiz calls: {full_html.count('checkQuiz(')}")
print(f"  goTo calls: {full_html.count('goTo(')}")
print(f"  Canvas elements: {full_html.count('<canvas')}")
print(f"  Example items: {full_html.count('class=\"example-item\"')}")
print(f"  Quiz questions: {full_html.count('class=\"quiz-question\"')}")
