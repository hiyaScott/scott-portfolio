import re

with open('tutorial.html', 'r') as f:
    old = f.read()

# Extract JS functions
def extract_js_function(content, func_name):
    pattern = rf'function\s+{func_name}\s*\([^)]*\)\s*\{{'
    m = re.search(pattern, content)
    if not m:
        return ''
    start = m.start()
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

js_funcs = {}
func_names = ['drawMotion', 'setForceDemo', 'drawForce', 'drawGravity', 'drawSpring', 'setInertia', 'drawInertia', 'draw']
for name in func_names:
    js_funcs[name] = extract_js_function(old, name)

# Extract section highlights
def extract_section(content, n):
    start = content.find(f'<!-- ========== Section {n}:')
    if n < 6:
        end = content.find(f'<!-- ========== Section {n+1}:')
    else:
        end = len(content)
    return content[start:end]

def get_highlights(section):
    return re.findall(r'<div class="highlight"[^>]*>(.+?)</div>', section, re.DOTALL)

highlights = {}
for i in range(1, 7):
    s = extract_section(old, i)
    highlights[i] = get_highlights(s)

# Save extracted data
with open('extracted_data.py', 'w') as f:
    f.write('js_funcs = {\n')
    for name, code in js_funcs.items():
        f.write(f'    "{name}": """{code}""",\n')
    f.write('}\n\n')
    f.write('highlights = {\n')
    for i, hls in highlights.items():
        f.write(f'    {i}: [\n')
        for hl in hls:
            f.write(f'        """{hl}""",\n')
        f.write(f'    ],\n')
    f.write('}\n')

print("Extracted JS functions:", [k for k, v in js_funcs.items() if v])
print("Extracted highlights:")
for i, hls in highlights.items():
    print(f"  Section {i}: {len(hls)} highlights")

# Extract canvas IDs per section
canvas_map = {}
for i in range(1, 7):
    s = extract_section(old, i)
    canvas_map[i] = re.findall(r'id="(\w+Canvas)"', s)
    print(f"  Section {i} canvases: {canvas_map[i]}")
