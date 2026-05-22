import re

# Read the old ch04 file
with open('tutorial.html', 'r') as f:
    old = f.read()

# Helper: extract first occurrence of a pattern in a section
def extract_first(html, pattern):
    m = re.search(pattern, html, re.DOTALL)
    return m.group(0) if m else ''

# Helper: extract all canvas-related HTML blocks from a section
def extract_canvases(section_html):
    canvases = []
    for m in re.finditer(r'<canvas[^>]*>.*?</canvas>', section_html, re.DOTALL):
        canvases.append(m.group(0))
    # Also extract slider controls associated with canvases
    sliders = []
    for m in re.finditer(r'<div class="slider-control".*?</div>\s*</div>', section_html, re.DOTALL):
        sliders.append(m.group(0))
    return canvases, sliders

# Extract section content - we'll do this manually for each section
# Section 1: 光的直线传播
s1_start = old.find('<!-- ========== Section 1:')
s1_end = old.find('<!-- ========== Section 2:')
s1 = old[s1_start:s1_end]

# Section 2: 光的反射
s2_start = s1_end
s2_end = old.find('<!-- ========== Section 3:')
s2 = old[s2_start:s2_end]

# Section 3: 光的折射
s3_start = s2_end
s3_end = old.find('<!-- ========== Section 4:')
s3 = old[s3_start:s3_end]

# Section 4: 透镜与成像
s4_start = s3_end
s4_end = old.find('<!-- ========== Section 5:')
s4 = old[s4_start:s4_end]

# Section 5: 公式总结
s5_start = s4_end
s5 = old[s5_start:]

print(f"S1: {len(s1)} bytes")
print(f"S2: {len(s2)} bytes")
print(f"S3: {len(s3)} bytes")
print(f"S4: {len(s4)} bytes")
print(f"S5: {len(s5)} bytes")

# Extract real example items (not the duplicated ones at the end)
def extract_real_examples(section_html, section_num):
    """Extract example items that are NOT the duplicated '例题 N' ones at the end"""
    # Find all example-item blocks
    items = re.findall(r'<div class="example-item".*?</div>\s*</div>', section_html, re.DOTALL)
    real = []
    for item in items:
        if '例题 N：' in item:
            continue  # Skip duplicated template residue
        real.append(item)
    return real

e1 = extract_real_examples(s1, 1)
e2 = extract_real_examples(s2, 2)
e3 = extract_real_examples(s3, 3)
e4 = extract_real_examples(s4, 4)

print(f"\nReal examples:")
print(f"  S1: {len(e1)} items")
print(f"  S2: {len(e2)} items")
print(f"  S3: {len(e3)} items")
print(f"  S4: {len(e4)} items")

for i, ex in enumerate(e1[:2]):
    q = re.search(r'div class="q"\u003e(.+?)</div>', ex, re.DOTALL)
    if q:
        clean = re.sub(r'<[^>]+?>', '', q.group(1)).strip()[:80]
        print(f"    S1-{i+1}: {clean}")

# Extract canvas blocks
def extract_demo_boxes(section_html):
    """Extract demo-box blocks containing canvas"""
    demos = re.findall(r'<div class="demo-box">(.+?)</div>\s*</div>', section_html, re.DOTALL)
    # Filter to only those with canvas
    canvas_demos = []
    for d in demos:
        if '<canvas' in d or '>🧪' in d:
            canvas_demos.append(d)
    return canvas_demos

d1 = extract_demo_boxes(s1)
d2 = extract_demo_boxes(s2)
d3 = extract_demo_boxes(s3)
d4 = extract_demo_boxes(s4)

print(f"\nCanvas demos:")
print(f"  S1: {len(d1)} blocks")
print(f"  S2: {len(d2)} blocks")
print(f"  S3: {len(d3)} blocks")
print(f"  S4: {len(d4)} blocks")

# Extract real quiz questions (not placeholders)
def extract_real_quizzes(section_html):
    """Extract quiz blocks that are NOT placeholders"""
    quizzes = []
    # Find all quiz divs
    for m in re.finditer(r'<div id="q\d+".*?</div>\s*</div>', section_html, re.DOTALL):
        quiz = m.group(0)
        if '请根据本单元内容设计测试题' not in quiz:
            quizzes.append(quiz)
    return quizzes

q1 = extract_real_quizzes(s1)
q2 = extract_real_quizzes(s2)
q3 = extract_real_quizzes(s3)
q4 = extract_real_quizzes(s4)

print(f"\nReal quizzes:")
print(f"  S1: {len(q1)} questions")
print(f"  S2: {len(q2)} questions")
print(f"  S3: {len(q3)} questions")
print(f"  S4: {len(q4)} questions")

# Extract concept highlights and formulas
def extract_concepts(section_html):
    """Extract highlight and formula-box blocks"""
    highlights = re.findall(r'<div class="highlight">(.+?)</div>', section_html, re.DOTALL)
    formulas = re.findall(r'<div class="formula-box">(.+?)</div>', section_html, re.DOTALL)
    return highlights, formulas

h1, f1 = extract_concepts(s1)
h2, f2 = extract_concepts(s2)
h3, f3 = extract_concepts(s3)
h4, f4 = extract_concepts(s4)

print(f"\nConcepts:")
print(f"  S1: {len(h1)} highlights, {len(f1)} formulas")
print(f"  S2: {len(h2)} highlights, {len(f2)} formulas")
print(f"  S3: {len(h3)} highlights, {len(f3)} formulas")
print(f"  S4: {len(h4)} highlights, {len(f4)} formulas")

# Extract all JS functions from the file (excluding checkQ_*)
def extract_js_functions(content):
    """Extract JS function definitions"""
    funcs = {}
    # Find functions in script tags
    for m in re.finditer(r'function\s+(\w+)\s*\([^)]*\)\s*\{', content):
        name = m.group(1)
        if name.startswith('checkQ'):
            continue
        # Extract full function body
        start = m.start()
        # Find matching closing brace
        brace_count = 0
        i = content.find('{', start)
        if i == -1:
            continue
        brace_count = 1
        i += 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        funcs[name] = content[start:i]
    return funcs

js_funcs = extract_js_functions(old)
print(f"\nJS functions found: {list(js_funcs.keys())}")

# Also extract IIFE blocks for canvas
def extract_iife_scripts(content):
    """Extract (function(){...})() blocks"""
    iifes = []
    for m in re.finditer(r'\(function\(\)\{.*?\}\)\(\);', content, re.DOTALL):
        iifes.append(m.group(0))
    return iifes

iifes = extract_iife_scripts(old)
print(f"IIFE blocks: {len(iifes)}")

# Check section 5 for content
s5_real = s5[:5000]  # First 5000 chars
print(f"\nS5 preview (first 500 chars):")
print(s5_real[:500])
