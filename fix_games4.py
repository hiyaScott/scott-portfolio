import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 1. 修改方块效果: rgb(250,250,250), alpha 0.6→1.0
content = content.replace('rgba(252, 252, 252,', 'rgba(250, 250, 250,')
content = content.replace(
    'const alpha = 0.8 + (this.scale - 1) * 1.0;  // scale 1→1.2, alpha 0.8→1.0',
    'const alpha = 0.6 + (this.scale - 1) * 2.0;  // scale 1→1.2, alpha 0.6→1.0'
)
content = content.replace('// ALPHA: base 0.8 → hover 1.0', '// ALPHA: base 0.6 → hover 1.0')

# 2. 修复导航链接颜色
content = content.replace(
    '.nav-link {\n            color: rgba(255, 255, 255, 0.9);',
    '.nav-link {\n            color: rgba(255, 255, 255, 0.95);'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')