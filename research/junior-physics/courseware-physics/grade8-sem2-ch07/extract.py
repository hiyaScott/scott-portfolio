import re

# Read original CH07
with open('/root/.openclaw/workspace/portfolio-blog/research/junior-physics/courseware-physics/grade8-sem2-ch07/tutorial.html') as f:
    orig = f.read()

# Extract canvas scripts
canvas_scripts = []
for m in re.finditer(r'<script>\(function\(\)[^<]*?</script>', orig, re.DOTALL):
    s = m.group(0)
    if 'getElementById' in s:
        canvas_scripts.append(s)

print(f"Found {len(canvas_scripts)} canvas scripts")
for i, s in enumerate(canvas_scripts):
    ids = re.findall(r"getElementById\('([^']+)'\)", s)
    print(f"  Script {i+1}: canvas ids = {ids}")
