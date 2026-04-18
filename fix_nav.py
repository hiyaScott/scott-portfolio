import re

with open('research/max-home/games.html', 'r') as f:
    content = f.read()

# 修复导航链接 active/hover 颜色为白色
content = content.replace(
    '.nav-link:hover, .nav-link.active { color: #333; }',
    '.nav-link:hover, .nav-link.active { color: #fff; font-weight: 400; }'
)

with open('research/max-home/games.html', 'w') as f:
    f.write(content)

print('Done')