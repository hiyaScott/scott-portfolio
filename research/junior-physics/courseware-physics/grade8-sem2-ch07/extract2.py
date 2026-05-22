import re

with open('/root/.openclaw/workspace/portfolio-blog/research/junior-physics/courseware-physics/grade8-sem2-ch07/tutorial.html') as f:
    orig = f.read()

# Find all canvas scripts by looking for canvas elements and their following scripts
canvas_ids = re.findall(r'id="([^"]+Canvas)"', orig)
print(f"Canvas IDs: {canvas_ids}")

# Extract scripts that reference these canvas ids
scripts = []
for cid in canvas_ids:
    # Find script that contains getElementById(cid)
    pattern = rf'<script>.*?getElementById\([\'"]{cid}[\'"]\).*?</script>'
    matches = re.findall(pattern, orig, re.DOTALL)
    for m in matches:
        scripts.append((cid, m))
        print(f"\n--- {cid} script (len={len(m)}) ---")
        print(m[:500])

print(f"\nTotal scripts found: {len(scripts)}")
